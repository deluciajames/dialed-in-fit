# Dialed In Fitness - Setup Instructions

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

## Installation

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies

```bash
cd ../frontend
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

The backend uses SQLite by default (no additional setup needed).
A `.env` file is optional but can be created for custom configuration.

```bash
cd ../backend
cp .env.example .env
```

## Running the Application

### Option 1: Using the Startup Script (Easiest)

From the project root:

```bash
# Make the script executable (first time only)
chmod +x start.sh

# Run the script
./start.sh
```

This will:
1. Start the backend API on http://localhost:8000
2. Start the frontend on http://localhost:8501
3. Open both in your browser

### Option 2: Manual Startup

**Terminal 1 - Start Backend:**
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Terminal 2 - Start Frontend:**
```bash
cd frontend
streamlit run Home.py
```

The app will be available at: http://localhost:8501

## First-Time Setup

1. **Create Your First Plan**
   - Navigate to the "Plan" page
   - Click "Create/Edit Plan" tab
   - Fill in your targets
   - Save your plan

2. **Log Your First Day**
   - Go to the "Today" page
   - Enter your daily metrics
   - Submit the log

3. **View Your Dashboard**
   - Return to the Home page
   - See your Dialed In Score!

## Database

The app uses SQLite by default, which creates a file `dialed_in.db` in the backend directory.

To reset the database:
```bash
cd backend
rm dialed_in.db
# Restart the backend - it will create a fresh database
```

## Troubleshooting

### Port Already in Use

If port 8000 or 8501 is already in use:

**Backend:**
```bash
uvicorn app.main:app --reload --port 8001
```
Then update `API_BASE_URL` in `frontend/api_client.py` to `http://localhost:8001`

**Frontend:**
```bash
streamlit run Home.py --server.port 8502
```

### Connection Errors

Make sure the backend is running before starting the frontend.
Check the terminal for any error messages.

### Import Errors

Make sure you're in the correct directory and have installed all requirements:
```bash
# For backend
cd backend
pip install -r requirements.txt

# For frontend
cd frontend
pip install -r requirements.txt
```

## Development Notes

### API Documentation

When the backend is running, visit http://localhost:8000/docs for interactive API documentation (Swagger UI).

### Project Structure

```
dialed-in-fitness/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── api/            # API routes
│   │   ├── core/           # Scoring engine
│   │   └── main.py         # FastAPI app
│   └── requirements.txt
│
├── frontend/               # Streamlit frontend
│   ├── pages/             # Page files
│   ├── api_client.py      # API client
│   ├── Home.py            # Dashboard
│   └── requirements.txt
│
└── README.md
```

## Next Steps (Phase 2 Features)

- Screenshot processing for data entry
- CSV import for historical data
- More advanced correlation reports
- API integrations (MyFitnessPal, etc.)

## Support

For issues or questions, check:
1. Backend logs in the terminal running uvicorn
2. Frontend logs in the terminal running streamlit
3. API docs at http://localhost:8000/docs
