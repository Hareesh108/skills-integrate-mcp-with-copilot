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
              description="API for viewing and signing up for extracurricular activities and managing clubs/committees")

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
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
    }
}

# In-memory club/committee database
clubs = {
    "Chess Club": {
        "description": "Chess enthusiasts club for tournaments and learning.",
        "members": ["michael@mergington.edu", "daniel@mergington.edu"],
        "activities": ["Chess Club"]
    },
    "Art Club": {
        "description": "Artistic expression through painting and drawing.",
        "members": ["amelia@mergington.edu", "harper@mergington.edu"],
        "activities": ["Art Club"]
    },
    "Drama Committee": {
        "description": "Organizes drama performances and events.",
        "members": ["ella@mergington.edu", "scarlett@mergington.edu"],
        "activities": ["Drama Club"]
    }
}

# --- Club/Committee Endpoints ---
from typing import List, Optional
from fastapi import Body

@app.get("/clubs")
def get_clubs():
    """Get all clubs/committees"""
    return clubs

@app.get("/clubs/{club_name}")
def get_club(club_name: str):
    """Get details of a specific club/committee"""
    if club_name not in clubs:
        raise HTTPException(status_code=404, detail="Club not found")
    return clubs[club_name]

@app.post("/clubs")
def create_club(
    name: str = Body(...),
    description: str = Body(...),
    activities_list: Optional[List[str]] = Body(default=[]),
    members: Optional[List[str]] = Body(default=[])
):
    """Create a new club/committee"""
    if name in clubs:
        raise HTTPException(status_code=400, detail="Club already exists")
    clubs[name] = {
        "description": description,
        "members": members,
        "activities": activities_list
    }
    return {"message": f"Club '{name}' created."}

@app.post("/clubs/{club_name}/add_member")
def add_member_to_club(club_name: str, email: str = Body(...)):
    """Add a member to a club/committee"""
    if club_name not in clubs:
        raise HTTPException(status_code=404, detail="Club not found")
    if email in clubs[club_name]["members"]:
        raise HTTPException(status_code=400, detail="Member already in club")
    clubs[club_name]["members"].append(email)
    return {"message": f"Added {email} to {club_name}"}

@app.delete("/clubs/{club_name}/remove_member")
def remove_member_from_club(club_name: str, email: str):
    """Remove a member from a club/committee"""
    if club_name not in clubs:
        raise HTTPException(status_code=404, detail="Club not found")
    if email not in clubs[club_name]["members"]:
        raise HTTPException(status_code=400, detail="Member not in club")
    clubs[club_name]["members"].remove(email)
    return {"message": f"Removed {email} from {club_name}"}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove student
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
