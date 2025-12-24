@echo off
REM FilePassword Backend Development Start Script for Windows

echo Starting FilePassword Backend Development Environment...

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -e ".[dev]"

REM Start services with Docker Compose
echo Starting Docker services...
docker-compose up -d db redis rabbitmq minio

REM Wait for services to be ready
echo Waiting for services to be ready...
timeout /t 15 /nobreak

REM Run database migrations
echo Running database migrations...
alembic upgrade head

REM Start the application
echo Starting FastAPI application...
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
