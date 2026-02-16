# Credit Approval System - Complete Guide

A full-stack credit approval system built with Django (Backend) and React (Frontend) that processes loan applications based on credit scoring algorithms.

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Running from Scratch](#running-from-scratch)
- [API Documentation](#api-documentation)
- [Excel Data Ingestion](#excel-data-ingestion)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

## Project Overview

This system allows users to register, check loan eligibility, and manage loans. It features a sophisticated credit scoring engine that uses historical data to make lending decisions.

### Key Features
- **Smart Credit Limits**: Automatically calculated based on salary.
- **Credit Scoring**: 0-100 score based on past repayment history and loan volume.
- **Tiered Interest Rates**: Adjusts rates based on creditworthiness.
- **Background Processing**: Handles large data imports asynchronously.
- **Modern Dashboard**: View all loan details in a responsive interface.

## Tech Stack

**Backend:**
- Django 4+ & Django REST Framework
- Celery (Background Tasks) with Redis
- PostgreSQL / SQLite (configured for easy local dev)
- Pandas (Excel Processing)

**Frontend:**
- React 18, Vite, Tailwind CSS 3.4
- Axios for API communication
- Lucide React for icons

## Prerequisites

Before starting, ensure you have:
- **Python 3.9+** installed
- **Node.js 16+** installed
- **Redis** installed (optional, needed only for background tasks)

## Quick Start

The fastest way to run the application on Windows:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Jaishankar7655/Loan-application.git
   cd Task-alemeno
   ```

2. **Run the all-in-one script**:
   - Double-click `run_dev.bat`
   - Or run in terminal: `.\run_dev.bat`

This will start the Backend (Port 8000), Frontend (Port 5173/5174), and Celery Worker automatically.

## Running from Scratch

If you prefer to run components manually or are on Mac/Linux:

### 1. Backend Setup
```bash
cd backend
python -m venv venv

# Activate Virtual Environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```
Backend will be available at: `http://127.0.0.1:8000`

### 2. Frontend Setup
Open a new terminal:
```bash
cd frontend
npm install
npm run dev
```
Frontend will be available at: `http://localhost:5173`

### 3. Celery Worker (Optional)
Required for background data ingestion. Open a new terminal:
```bash
cd backend
venv\Scripts\activate
celery -A core worker -l info --pool=solo
```

## API Documentation

The backend provides the following REST endpoints:

### 1. Register Customer
**POST** `/register`
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "age": 30,
  "monthly_income": 50000,
  "phone_number": "1234567890"
}
```
**Response**: Returns `customer_id` and calculated `approved_limit`.

### 2. Check Eligibility
**POST** `/check-eligibility`
```json
{
  "customer_id": 1,
  "loan_amount": 100000,
  "interest_rate": 10,
  "tenure": 12
}
```
**Response**: Returns approval status, corrected interest rate, and monthly installment.

### 3. Create Loan
**POST** `/create-loan`
```json
{
  "customer_id": 1,
  "loan_amount": 100000,
  "interest_rate": 12,
  "tenure": 12
}
```
**Response**: Returns `loan_id` and confirmation message.

### 4. View Loans
- **GET** `/view-loan/{loan_id}`: Details of a specific loan.
- **GET** `/view-loans/{customer_id}`: List of all loans for a customer.

## Excel Data Ingestion

The system uses historical data from Excel files to calculate credit scores.

### Files
- **`customer_data.xlsx`**: Historical customer profiles.
- **`loan_data.xlsx`**: Past loan repayment history.

### How to Load Data

**Method 1: Simple Script (Recommended for Dev)**
We have provided a script to easily load data without setting up Celery.
```bash
cd backend
venv\Scripts\activate
python load_excel_data.py
```

**Method 2: Background Task (Production)**
Requires Redis and Celery worker running.
```bash
cd backend
venv\Scripts\activate
python manage.py ingest_data
```

### Verification
After loading, you can verify data in the Django Admin or by checking the database:
```bash
python manage.py shell
>>> from api.models import Customer
>>> Customer.objects.count()
```

## Project Structure

```
backend/
├── api/             # Main application logic
├── core/            # Project settings
├── load_excel_data.py # Data loading script
└── requirements.txt # Python dependencies
frontend/
├── src/
│   ├── components/  # React components (Register, Dashboard)
│   └── App.jsx      # Main frontend logic
└── tailwind.config.js
customer_data.xlsx   # Sample data
loan_data.xlsx       # Sample data
run_dev.bat          # Quick start script
```

## Troubleshooting

- **CORS Errors**: If you see CORS errors in the browser console, ensure the backend is running on `127.0.0.1:8000`. We have configured CORS to allow requests from `localhost:5173` and `localhost:5174`.
- **"Module not defined" in Frontend**: This usually means an issue with `postcss.config.js`. Ensure it is named `postcss.config.cjs` if the project is ESM.
- **Database Locked**: If using SQLite, close any other programs accessing the database file.
