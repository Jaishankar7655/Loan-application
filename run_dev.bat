@echo off
echo Starting Credit Approval System Development Environment...

echo Starting Backend (Django)...
start cmd /k "cd backend && venv\Scripts\activate && python manage.py runserver 0.0.0.0:8000"

echo Starting Celery Worker...
start cmd /k "cd backend && venv\Scripts\activate && celery -A core worker -l info --pool=sole"

echo Starting Frontend (Vite)...
start cmd /k "cd frontend && npm run dev"

echo All services started!
echo Backend: http://127.0.0.1:8000
echo Frontend: http://localhost:5173
pause
