import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.tasks import ingest_customer_data, ingest_loan_data

print("=" * 60)
print("CREDIT APPROVAL SYSTEM - DATA INGESTION")
print("=" * 60)

print("\n📊 Loading customer data from customer_data.xlsx...")
result1 = ingest_customer_data()
print(f"✅ {result1}")

print("\n💰 Loading loan data from loan_data.xlsx...")
result2 = ingest_loan_data()
print(f"✅ {result2}")

print("\n" + "=" * 60)
print("VERIFICATION")
print("=" * 60)

from api.models import Customer, Loan

total_customers = Customer.objects.count()
total_loans = Loan.objects.count()

print(f"\n📈 Total Customers in Database: {total_customers}")
print(f"📈 Total Loans in Database: {total_loans}")

if total_customers > 0:
    sample_customer = Customer.objects.first()
    print(f"\n👤 Sample Customer:")
    print(f"   - Name: {sample_customer.first_name} {sample_customer.last_name}")
    print(f"   - ID: {sample_customer.customer_id}")
    print(f"   - Approved Limit: ₹{sample_customer.approved_limit:,}")
    print(f"   - Monthly Salary: ₹{sample_customer.monthly_salary:,}")
    
    customer_loans = sample_customer.loans.all()
    print(f"   - Number of Loans: {customer_loans.count()}")

print("\n" + "=" * 60)
print("✅ DATA INGESTION COMPLETE!")
print("=" * 60)
print("\nYou can now use the credit approval system with historical data.")
print("The credit scoring algorithm will use this data to make decisions.\n")
