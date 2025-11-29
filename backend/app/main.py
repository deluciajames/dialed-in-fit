from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api import plans, logs, dashboard

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Dialed In Fitness API",
    description="API for comprehensive fitness tracking with intelligent scoring",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(plans.router)
app.include_router(logs.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Dialed In Fitness API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
