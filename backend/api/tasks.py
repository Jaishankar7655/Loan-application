from celery import shared_task
import pandas as pd
from .models import Customer, Loan
import os
from datetime import datetime

@shared_task
def ingest_customer_data():
    file_path = 'customer_data.xlsx'
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return "File not found"
    
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error reading excel: {e}")
        return str(e)

    # Columns: Customer ID, First Name, Last Name, Age, Phone Number, Monthly Salary, Approved Limit
    
    count = 0
    for _, row in df.iterrows():
        try:
            Customer.objects.update_or_create(
                customer_id=row['Customer ID'],
                defaults={
                    'first_name': row['First Name'],
                    'last_name': row['Last Name'],
                    'age': row['Age'],
                    'phone_number': str(row['Phone Number']),
                    'monthly_salary': row['Monthly Salary'],
                    'approved_limit': row['Approved Limit'],
                }
            )
            count += 1
        except Exception as e:
            print(f"Error processing customer row {row.get('Customer ID')}: {e}")
            continue
            
    return f"Ingested {count} customers"

@shared_task
def ingest_loan_data():
    file_path = 'loan_data.xlsx'
    if not os.path.exists(file_path):
        return "File not found"

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        return str(e)
    # customer id, loan id, loan amount, tenure, interest rate, monthly repayment (emi), EMIs paid on Time, start date, end date
    
    count = 0
    for _, row in df.iterrows():
        try:
            customer_id = row['Customer ID']
            try:
                customer = Customer.objects.get(customer_id=customer_id)
            except Customer.DoesNotExist:
                print(f"Customer {customer_id} not found for loan {row['Loan ID']}")
                continue

            Loan.objects.update_or_create(
                loan_id=row['Loan ID'],
                defaults={
                    'customer': customer,
                    'loan_amount': row['Loan Amount'],
                    'tenure': row['Tenure'],
                    'interest_rate': row['Interest Rate'],
                    'monthly_repayment': row['Monthly payment'],
                    'emis_paid_on_time': row['EMIs paid on Time'],
                    'start_date': row['Date of Approval'],
                    'end_date': row['End Date']
                }
            )
            count += 1
        except Exception as e:
            print(f"Error processing loan row {row.get('Loan ID')}: {e}")
            continue
            
    return f"Ingested {count} loans"
