# Quick Start Guide - Credit Approval System

## ✅ Current Status
Both servers are **RUNNING** and **READY TO USE**:
- 🟢 **Backend**: http://127.0.0.1:8000 (Django + DRF + CORS enabled)
- 🟢 **Frontend**: http://localhost:5173 (React + Tailwind CSS v3.4.1)

## 🚀 Access the Application
Simply open your browser and navigate to:
**http://localhost:5173**

## 📋 Available Features

### 1. Register New Customer
- Navigate to `/register`
- Fill in customer details
- System automatically calculates credit limit (36 × monthly salary)

### 2. Check Loan Eligibility
- Navigate to `/check-eligibility`
- Enter customer ID and loan details
- Get instant approval decision with corrected interest rate

### 3. View Customer Loans
- Navigate to `/dashboard`
- Enter customer ID
- View all active loans with EMI details

## 🔧 API Endpoints (Backend)
All endpoints are accessible at `http://127.0.0.1:8000/`

- `POST /register` - Register new customer
- `POST /check-eligibility` - Check loan eligibility
- `POST /create-loan` - Create new loan
- `GET /view-loan/{loan_id}` - View specific loan
- `GET /view-loans/{customer_id}` - View all customer loans

## 📊 Data Ingestion
To load the Excel data (`customer_data.xlsx` and `loan_data.xlsx`):

1. Open a new terminal
2. Navigate to backend:
   ```bash
   cd backend
   venv\Scripts\activate
   ```
3. Run the ingestion command:
   ```bash
   python manage.py ingest_data
   ```

## 🧪 Testing
Run unit tests:
```bash
cd backend
venv\Scripts\activate
python manage.py test api
```

## 🛑 Stopping the Servers
Press `Ctrl+C` in each terminal window running the servers.

## 📁 Project Structure
```
Task-alemeno/
├── backend/          # Django REST API
│   ├── api/         # Main application
│   ├── core/        # Django settings
│   └── db.sqlite3   # Database
├── frontend/        # React application
│   └── src/         # Source code
├── docker-compose.yml
└── README.md
```

## 🐛 Troubleshooting

**Frontend shows unstyled content:**
- Ensure `postcss.config.cjs` exists (not `.js`)
- Check Tailwind CSS is v3.4.1

**Backend CORS errors:**
- Verify `django-cors-headers` is installed
- Check `CORS_ALLOWED_ORIGINS` in settings.py

**Database errors:**
- Run migrations: `python manage.py migrate`

For detailed documentation, see [README.md](README.md)
