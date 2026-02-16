from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Customer, Loan
from .serializers import (
    CustomerRegistrationSerializer, 
    LoanEligibilitySerializer, 
    CreateLoanSerializer, 
    ViewLoanSerializer,
    ViewLoansSerializer
)
import math
from datetime import date, timedelta

# Helper for EMI calculation
def calculate_emi(principal, rate, tenure):
    # rate is annual interest rate
    if rate == 0:
        return principal / tenure
    r = rate / 12 / 100
    emi = principal * r * ((1 + r)**tenure) / (((1 + r)**tenure) - 1)
    return emi

# Helper for Credit Score
def calculate_credit_score(customer_id):
    customer = Customer.objects.get(customer_id=customer_id)
    loans = Loan.objects.filter(customer=customer)
    
    # i. Past Loans paid on time
    paid_on_time_count = sum(l.emis_paid_on_time for l in loans)
    total_tenure = sum(l.tenure for l in loans)
    
    # ii. No of loans taken in past
    loan_count = loans.count()
    
    # iii. Loan activity in current year
    current_year = date.today().year
    current_year_loans = loans.filter(start_date__year=current_year).count()
    
    # iv. Loan approved volume
    total_loan_amount = sum(l.loan_amount for l in loans)
    
    # Heuristic Formula (out of 100):
    # Base score
    score = 0
    
    # More repaid on time -> Higher score
    # Normalized: If paid_on_time / tenure > 0.8 => +40 points
    if total_tenure > 0:
        repayment_ratio = paid_on_time_count / total_tenure
        score += repayment_ratio * 40
    else:
        score += 20 # New customer default?
        
    # More loans in past (showing history) => +20 points max
    score += min(loan_count * 5, 20)
    
    # Loan activity in current year. Too many might be bad? Or good?
    # Prompt lists it as component. Let's say moderate is good.
    # Actually prompt says "check loan eligibility based on credit score".
    # I'll add points for activity.
    score += min(current_year_loans * 5, 20)
    
    # Approved volume. Higher volume approved in past implies trust?
    if total_loan_amount > 1000000:
        score += 20
    elif total_loan_amount > 100000:
        score += 10
        
    # Cap at 100
    score = min(score, 100)
    
    # Rule: If sum of current loans > approved limit, credit score = 0
    current_loans_amount = sum(l.loan_amount for l in loans if l.end_date >= date.today())
    if current_loans_amount > customer.approved_limit:
        score = 0
        
    return score

@api_view(['POST'])
def register_customer(request):
    data = request.data
    # Calculate approved limit
    # 36 * monthly_salary (rounded to nearest lakh)
    monthly_salary = data.get('monthly_income')
    if not monthly_salary:
        return Response({"error": "monthly_income is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    limit_raw = 36 * int(monthly_salary)
    # Round to nearest lakh: round(x / 100000) * 100000
    approved_limit = round(limit_raw / 100000) * 100000
    
    # Add to payload
    data_copy = data.copy()
    data_copy['approved_limit'] = approved_limit
    data_copy['monthly_salary'] = monthly_salary # Map income to salary
    
    serializer = CustomerRegistrationSerializer(data=data_copy)
    if serializer.is_valid():
        serializer.save(approved_limit=approved_limit)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def check_eligibility(request):
    serializer = LoanEligibilitySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    customer_id = data['customer_id']
    loan_amount = data['loan_amount']
    interest_rate = data['interest_rate']
    tenure = data['tenure']
    
    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
    
    credit_score = calculate_credit_score(customer_id)
    
    approval = False
    corrected_interest_rate = interest_rate
    
    # Logic
    if credit_score > 50:
        approval = True
    elif 50 >= credit_score > 30:
        if interest_rate > 12:
            approval = True
        else:
            approval = True
            corrected_interest_rate = 12.0
    elif 30 >= credit_score > 10:
        if interest_rate > 16:
            approval = True
        else:
            approval = True
            corrected_interest_rate = 16.0
            
    # Sum of all current EMIs > 50% of monthly salary
    current_loans = Loan.objects.filter(customer=customer, end_date__gte=date.today())
    current_emis = sum(l.monthly_repayment for l in current_loans)
    
    # Proposed EMI
    proposed_emi = calculate_emi(loan_amount, corrected_interest_rate, tenure)
    
    if (current_emis + proposed_emi) > (0.5 * customer.monthly_salary):
        approval = False
        
    response_data = {
        "customer_id": customer_id,
        "approval": approval,
        "interest_rate": interest_rate,
        "corrected_interest_rate": corrected_interest_rate,
        "tenure": tenure,
        "monthly_installment": proposed_emi
    }
    
    return Response(response_data)

@api_view(['POST'])
def create_loan(request):
    serializer = CreateLoanSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    data = serializer.validated_data
    customer_id = data['customer_id']
    loan_amount = data['loan_amount']
    interest_rate = data['interest_rate']
    tenure = data['tenure']
    
    # Re-run eligibility check logic (simplified)
    # Ideally should call the check_eligibility logic but returning boolean
    
    # For now, implementing logic again or assuming valid if passed?
    # Prompt says "Process a new loan based on eligibility."
    # So we must check eligibility again.
    
    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return Response({"message": "Customer not found", "loan_approved": False, "loan_id": None}, status=status.HTTP_404_NOT_FOUND)

    credit_score = calculate_credit_score(customer_id)
    approval = False
    final_interest_rate = interest_rate
    
    if credit_score > 50:
        approval = True
    elif 50 >= credit_score > 30:
        if interest_rate <= 12:
            final_interest_rate = 12.0
        approval = True
    elif 30 >= credit_score > 10:
        if interest_rate <= 16:
            final_interest_rate = 16.0
        approval = True
    else:
        approval = False
        
    current_loans = Loan.objects.filter(customer=customer, end_date__gte=date.today())
    current_emis = sum(l.monthly_repayment for l in current_loans)
    monthly_installment = calculate_emi(loan_amount, final_interest_rate, tenure)
    
    if (current_emis + monthly_installment) > (0.5 * customer.monthly_salary):
        approval = False
        
    if approval:
        loan = Loan.objects.create(
            customer=customer,
            loan_amount=loan_amount,
            tenure=tenure,
            interest_rate=final_interest_rate,
            monthly_repayment=monthly_installment,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=tenure*30) # approx
        )
        return Response({
            "loan_id": loan.loan_id,
            "customer_id": customer_id,
            "loan_approved": True,
            "message": "Loan Approved",
            "monthly_installment": monthly_installment
        }, status=status.HTTP_201_CREATED)
    else:
        return Response({
            "loan_id": None,
            "customer_id": customer_id,
            "loan_approved": False,
            "message": "Loan not approved due to low credit score or high existing debt",
            "monthly_installment": 0
        }, status=status.HTTP_200_OK)

@api_view(['GET'])
def view_loan(request, loan_id):
    try:
        loan = Loan.objects.get(loan_id=loan_id)
    except Loan.DoesNotExist:
        return Response({"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ViewLoanSerializer(loan)
    return Response(serializer.data)

@api_view(['GET'])
def view_loans(request, customer_id):
    loans = Loan.objects.filter(customer__customer_id=customer_id)
    serializer = ViewLoansSerializer(loans, many=True)
    return Response(serializer.data)
