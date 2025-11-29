# Dialed In Fitness Tracker

A comprehensive fitness tracking application that provides a unified "Dialed In Score" based on your nutrition, training, sleep, and wellness metrics.

## Project Structure

```
dialed-in-fitness/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── api/            # API routes
│   │   ├── core/           # Core logic (scoring engine)
│   │   └── database.py     # Database connection
│   ├── alembic/            # Database migrations
│   └── requirements.txt
│
├── frontend/               # Streamlit frontend
│   ├── pages/             # Streamlit pages
│   ├── components/        # Reusable components
│   └── requirements.txt
│
└── README.md
```

## Tech Stack

**Backend:**
- FastAPI (REST API)
- PostgreSQL (Database)
- SQLAlchemy (ORM)
- Alembic (Migrations)

**Frontend:**
- Streamlit (UI Framework)
- Plotly (Charts)
- Requests (API calls)

## Setup Instructions

### Prerequisites
- Python 3.11+
- PostgreSQL

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
# Configure DATABASE_URL in .env
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
pip install -r requirements.txt
streamlit run Home.py
```

## Features (Phase 1)

- ✅ Daily logging (nutrition, workouts, wellness)
- ✅ Dialed In Score calculation
- ✅ Plan creation and management
- ✅ Four core correlation reports
- ✅ Historical trend tracking

## Coming Soon (Phase 2)

- 📸 Screenshot processing
- 📊 CSV import
- 🔍 Advanced correlation analysis
