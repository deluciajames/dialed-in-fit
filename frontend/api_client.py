import requests
import os
from typing import Dict, List, Optional
from datetime import date

# API base URL - Render's service discovery provides just the hostname,
# so we add https:// if no scheme is present
_raw_api_url = os.getenv("API_BASE_URL", "http://localhost:8000")
if _raw_api_url and not _raw_api_url.startswith("http"):
    API_BASE_URL = f"https://{_raw_api_url}"
else:
    API_BASE_URL = _raw_api_url


class APIClient:
    """Client for interacting with the Dialed In Fitness API."""
    
    def __init__(self, user_id: int = 1):
        """Initialize API client with a user ID."""
        self.user_id = user_id
        self.base_url = API_BASE_URL
    
    # Plan endpoints
    def create_plan(self, plan_data: Dict) -> Dict:
        """Create a new plan."""
        response = requests.post(
            f"{self.base_url}/plans/",
            json=plan_data,
            params={"user_id": self.user_id}
        )
        response.raise_for_status()
        return response.json()
    
    def get_active_plan(self) -> Optional[Dict]:
        """Get the currently active plan."""
        try:
            response = requests.get(
                f"{self.base_url}/plans/active",
                params={"user_id": self.user_id}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise
    
    def get_all_plans(self) -> List[Dict]:
        """Get all plans for the user."""
        response = requests.get(
            f"{self.base_url}/plans/",
            params={"user_id": self.user_id}
        )
        response.raise_for_status()
        return response.json()
    
    def update_plan(self, plan_id: int, plan_data: Dict) -> Dict:
        """Update an existing plan."""
        response = requests.put(
            f"{self.base_url}/plans/{plan_id}",
            json=plan_data,
            params={"user_id": self.user_id}
        )
        response.raise_for_status()
        return response.json()
    
    # Daily log endpoints
    def create_daily_log(self, log_data: Dict) -> Dict:
        """Create a new daily log."""
        response = requests.post(
            f"{self.base_url}/logs/",
            json=log_data,
            params={"user_id": self.user_id}
        )
        response.raise_for_status()
        return response.json()
    
    def get_daily_log_by_date(self, log_date: date) -> Optional[Dict]:
        """Get a daily log by date."""
        try:
            response = requests.get(
                f"{self.base_url}/logs/date/{log_date.isoformat()}",
                params={"user_id": self.user_id}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise
    
    def update_daily_log(self, log_id: int, log_data: Dict) -> Dict:
        """Update an existing daily log."""
        response = requests.put(
            f"{self.base_url}/logs/{log_id}",
            json=log_data,
            params={"user_id": self.user_id}
        )
        response.raise_for_status()
        return response.json()
    
    def get_daily_logs(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[Dict]:
        """Get daily logs, optionally filtered by date range."""
        params = {"user_id": self.user_id}
        if start_date:
            params["start_date"] = start_date.isoformat()
        if end_date:
            params["end_date"] = end_date.isoformat()
        
        response = requests.get(
            f"{self.base_url}/logs/",
            params=params
        )
        response.raise_for_status()
        return response.json()
    
    # Dashboard endpoints
    def get_dashboard(self, period: str = "7d") -> Dict:
        """Get dashboard data for a time period."""
        response = requests.get(
            f"{self.base_url}/dashboard/",
            params={"user_id": self.user_id, "period": period}
        )
        response.raise_for_status()
        return response.json()
    
    def get_score_color(self, score: float) -> Dict:
        """Get color coding for a score."""
        response = requests.get(
            f"{self.base_url}/dashboard/score-color",
            params={"score": score}
        )
        response.raise_for_status()
        return response.json()
