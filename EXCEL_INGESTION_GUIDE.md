# Excel Data Ingestion Guide

## Overview
The Credit Approval System includes a data ingestion feature that processes Excel files containing historical customer and loan data. This is essential for the credit scoring algorithm to work properly, as it needs past data to calculate credit scores.

## Excel Files

### 1. customer_data.xlsx
Located in the root directory, contains:
- **Customer ID** - Unique identifier
- **First Name** - Customer's first name
- **Last Name** - Customer's last name
- **Age** - Customer's age
- **Phone Number** - Contact number
- **Monthly Salary** - Monthly income
- **Approved Limit** - Credit limit (calculated as 36 × monthly salary)
- **Current Debt** - Total outstanding debt

### 2. loan_data.xlsx
Located in the root directory, contains:
- **Customer ID** - Links to customer
- **Loan ID** - Unique loan identifier
- **Loan Amount** - Principal amount
- **Tenure** - Loan duration in months
- **Interest Rate** - Annual interest rate
- **Monthly Payment** - EMI amount
- **EMIs Paid on Time** - Number of on-time payments
- **Date of Approval** - Loan start date
- **End Date** - Loan maturity date

## How It Works

### Architecture
```
Excel Files → Pandas → Celery Background Tasks → Django Models → Database
```

1. **Pandas** reads the Excel files
2. **Celery tasks** process data in the background
3. **Django ORM** saves data to the database
4. **Credit scoring algorithm** uses this data for calculations

### Code Flow

**Step 1: Management Command**
```bash
python manage.py ingest_data
```

**Step 2: Celery Tasks Triggered**
- `ingest_customer_data()` - Processes customer_data.xlsx
- `ingest_loan_data()` - Processes loan_data.xlsx

**Step 3: Data Processing**
- Reads Excel using `pandas.read_excel()`
- Iterates through rows
- Uses `update_or_create()` to avoid duplicates
- Handles errors gracefully

## How to Run Data Ingestion

### Method 1: Using Celery (Recommended for Production)

**Step 1: Start Redis** (if not already running)
```bash
# Windows (using WSL or Redis for Windows)
redis-server

# Or use Docker
docker run -d -p 6379:6379 redis
```

**Step 2: Start Celery Worker**
```bash
cd backend
venv\Scripts\activate
celery -A core worker -l info --pool=solo
```

**Step 3: Run Ingestion Command**
```bash
# In a new terminal
cd backend
venv\Scripts\activate
python manage.py ingest_data
```

You'll see output like:
```
Starting ingestion...
Triggered customer ingestion task: abc123-def456
Triggered loan ingestion task: xyz789-uvw012
```

**Step 4: Check Celery Worker Terminal**
You'll see the tasks being processed:
```
[INFO] Task api.tasks.ingest_customer_data[abc123] succeeded: 'Ingested 500 customers'
[INFO] Task api.tasks.ingest_loan_data[xyz789] succeeded: 'Ingested 2000 loans'
```

### Method 2: Synchronous (For Testing/Development)

If you don't want to set up Celery, you can modify the command to run synchronously:

**Create a simple script:** `backend/load_data.py`
```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.tasks import ingest_customer_data, ingest_loan_data

print("Loading customer data...")
result1 = ingest_customer_data()
print(result1)

print("Loading loan data...")
result2 = ingest_loan_data()
print(result2)

print("Done!")
```

**Run it:**
```bash
cd backend
venv\Scripts\activate
python load_data.py
```

## Verifying Data Ingestion

### Check via Django Shell
```bash
cd backend
venv\Scripts\activate
python manage.py shell
```

```python
from api.models import Customer, Loan

# Check customer count
print(f"Total customers: {Customer.objects.count()}")

# Check loan count
print(f"Total loans: {Loan.objects.count()}")

# View a sample customer
customer = Customer.objects.first()
print(f"Customer: {customer.first_name} {customer.last_name}")
print(f"Approved Limit: {customer.approved_limit}")

# View their loans
loans = customer.loans.all()
print(f"Number of loans: {loans.count()}")
```

### Check via API
```bash
# Get customer loans (replace 1 with actual customer_id)
curl http://127.0.0.1:8000/view-loans/1
```

## Why Excel Data is Important

The credit scoring algorithm uses historical data to calculate:

1. **Repayment History (40%)** - Uses `EMIs paid on Time` from loan_data.xlsx
2. **Loan Count (20%)** - Counts total loans per customer
3. **Current Year Activity (20%)** - Checks loans from loan_data.xlsx with recent dates
4. **Approved Volume (20%)** - Sums total loan amounts

**Without this data:**
- New customers get a default score
- Credit decisions may be less accurate
- The system can't demonstrate its full capabilities

## Troubleshooting

### "File not found" Error
**Solution:** Ensure Excel files are in the `backend/` directory (same level as `manage.py`)

```bash
# Check file location
cd backend
ls *.xlsx
# Should show: customer_data.xlsx  loan_data.xlsx
```

If files are in the root directory, copy them:
```bash
copy ..\customer_data.xlsx .
copy ..\loan_data.xlsx .
```

### "Celery worker not running" Error
**Solution:** Start the Celery worker first (see Method 1 above)

### Column Name Mismatch
**Solution:** The code expects exact column names. If your Excel has different names, update `api/tasks.py`:

```python
# Example: If your Excel has "CustomerID" instead of "Customer ID"
customer_id=row['CustomerID']  # Update this
```

### Redis Connection Error
**Solution:** 
- Install Redis or use SQLite as broker (not recommended for production)
- Or use Method 2 (synchronous) for development

## File Locations
```
Task-alemeno/
├── customer_data.xlsx          # Customer data (root or backend/)
├── loan_data.xlsx              # Loan data (root or backend/)
└── backend/
    ├── api/
    │   ├── tasks.py           # Celery tasks for ingestion
    │   └── management/
    │       └── commands/
    │           └── ingest_data.py  # Management command
    └── manage.py
```

## Summary

**Quick Steps:**
1. Ensure Excel files are in `backend/` directory
2. Start Celery worker: `celery -A core worker -l info --pool=solo`
3. Run ingestion: `python manage.py ingest_data`
4. Verify: Check Django admin or use API endpoints

The data will be used automatically by the credit scoring algorithm when you check loan eligibility!
