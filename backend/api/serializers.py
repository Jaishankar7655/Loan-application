from rest_framework import serializers
from .models import Customer, Loan

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customer_id', 'first_name', 'last_name', 'phone_number', 'monthly_salary', 'approved_limit', 'current_debt', 'age']

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['loan_id', 'customer', 'loan_amount', 'tenure', 'interest_rate', 'monthly_repayment', 'emis_paid_on_time', 'start_date', 'end_date']

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    monthly_income = serializers.IntegerField(source='monthly_salary')
    name = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'age', 'monthly_income', 'phone_number', 'name', 'customer_id', 'approved_limit']
        read_only_fields = ['customer_id', 'approved_limit', 'name']

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class LoanEligibilitySerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.FloatField()
    interest_rate = serializers.FloatField()
    tenure = serializers.IntegerField()

class CreateLoanSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.FloatField()
    interest_rate = serializers.FloatField()
    tenure = serializers.IntegerField()

class ViewLoanSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    
    class Meta:
        model = Loan
        fields = ['loan_id', 'customer', 'loan_amount', 'interest_rate', 'monthly_repayment', 'tenure']

class ViewLoansSerializer(serializers.ModelSerializer):
    repayments_left = serializers.SerializerMethodField()
    monthly_installment = serializers.FloatField(source='monthly_repayment')
    
    class Meta:
        model = Loan
        fields = ['loan_id', 'loan_amount', 'interest_rate', 'monthly_installment', 'repayments_left']

    def get_repayments_left(self, obj):
        # Assuming tenure - emis_paid_on_time? Or based on date?
        # Prompt doesn't specify how to calculate repayments left.
        # "No of EMIs left".
        # Assuming tenure is total months.
        return obj.tenure - obj.emis_paid_on_time
