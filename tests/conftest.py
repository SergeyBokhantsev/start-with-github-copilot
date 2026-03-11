"""
Test configuration and fixtures for FastAPI application tests.

Provides:
- TestClient fixture for making requests to the FastAPI app
- Activity reset between tests to ensure test isolation
"""

import pytest
from fastapi.testclient import TestClient
from copy import deepcopy
import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


# Initial activities state - single source of truth
INITIAL_ACTIVITIES_STATE = {
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


@pytest.fixture
def client():
    """
    Fixture providing a TestClient for the FastAPI application.
    
    Yields:
        TestClient: A test client for making HTTP requests to the app
    """
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities_state():
    """
    Fixture that resets the activities state before each test to ensure isolation.
    
    This is automatically used for every test without explicit inclusion.
    Uses deepcopy to ensure mutable objects (lists) are not shared between tests.
    Yields control back to the test, then cleans up afterwards.
    """
    # Setup: Reset activities to initial state before each test
    #Use deepcopy to avoid sharing mutable list objects
    activities.clear()
    activities.update(deepcopy(INITIAL_ACTIVITIES_STATE))
    
    # Test runs here
    yield
    
    # Teardown: Reset again after test (not strictly necessary but clean)
    activities.clear()
    activities.update(deepcopy(INITIAL_ACTIVITIES_STATE))


@pytest.fixture
def activity_names():
    """
    Fixture providing list of activity names from INITIAL_ACTIVITIES_STATE.
    
    Returns:
        list: Activity names in order
    """
    return list(INITIAL_ACTIVITIES_STATE.keys())


def get_activity_by_index(index: int) -> str:
    """
    Helper function to get activity name by index.
    
    Args:
        index: 0-based index of the activity
        
    Returns:
        str: Activity name at the given index
    """
    return list(INITIAL_ACTIVITIES_STATE.keys())[index]


@pytest.fixture
def get_activity():
    """
    Fixture providing a function to get activity names by index.
    
    Returns:
        function: get_activity_by_index function
    """
    return get_activity_by_index


@pytest.fixture
def expected_activity_count():
    """Fixture providing the expected number of activities."""
    return len(INITIAL_ACTIVITIES_STATE)


@pytest.fixture
def expected_activity_names():
    """Fixture providing the expected activity names."""
    return set(INITIAL_ACTIVITIES_STATE.keys())
