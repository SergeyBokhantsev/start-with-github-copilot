"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball training and games",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Tennis skills development and friendly matches",
        "schedule": "Wednesdays and Saturdays, 3:00 PM - 4:30 PM",
        "max_participants": 16,
        "participants": ["james@mergington.edu", "lucy@mergington.edu"]
    },
    "Drama Club": {
        "description": "Theater performances and acting workshops",
        "schedule": "Tuesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["sarah@mergington.edu"]
    },
    "Digital Art Class": {
        "description": "Learn digital illustration and graphic design",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 4:45 PM",
        "max_participants": 18,
        "participants": ["grace@mergington.edu", "noah@mergington.edu"]
    },
    "Science Club": {
        "description": "Explore scientific experiments and research projects",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["ryan@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and critical thinking skills",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 14,
        "participants": ["maya@mergington.edu", "ethan@mergington.edu"]
    }
}


# Business Logic Functions (testable, separate from endpoints)

def get_all_activities():
    """Get all available activities with their details"""
    return activities


def signup_student(activity_name: str, email: str):
    """
    Sign up a student for an activity.
    
    Args:
        activity_name: Name of the activity
        email: Student email address
        
    Raises:
        KeyError: If activity does not exist
        ValueError: If student is already signed up or other validation fails
    """
    # Validate activity exists
    if activity_name not in activities:
        raise KeyError(f"Activity '{activity_name}' not found")
    
    activity = activities[activity_name]
    
    # Validate student is not already signed up
    if email in activity["participants"]:
        raise ValueError(f"Student {email} is already signed up for {activity_name}")
    
    # Add student
    activity["participants"].append(email)


def cancel_student_signup(activity_name: str, email: str):
    """
    Cancel a student's signup for an activity.
    
    Args:
        activity_name: Name of the activity
        email: Student email address
        
    Raises:
        KeyError: If activity does not exist
        ValueError: If student is not signed up for the activity
    """
    # Validate activity exists
    if activity_name not in activities:
        raise KeyError(f"Activity '{activity_name}' not found")
    
    activity = activities[activity_name]
    
    # Check if student is registered
    if email not in activity["participants"]:
        raise ValueError(f"Student {email} is not signed up for {activity_name}")
    
    # Remove student
    activity["participants"].remove(email)


# API Endpoints

@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    """Get all available activities"""
    return get_all_activities()


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    try:
        signup_student(activity_name, email)
        return {"message": f"Signed up {email} for {activity_name}"}
    except KeyError:
        raise HTTPException(status_code=404, detail="Activity not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/activities/{activity_name}/cancel")
def cancel_activity_signup(activity_name: str, email: str):
    """Cancel a student's registration for an activity"""
    try:
        cancel_student_signup(activity_name, email)
        return {"message": f"Unregistered {email} from {activity_name}"}
    except KeyError:
        raise HTTPException(status_code=404, detail="Activity not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
