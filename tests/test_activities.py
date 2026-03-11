"""
Tests for the activities listing endpoint.

Tests the GET /activities endpoint to ensure it returns all available activities
with correct structure and data.

Pattern: Arrange-Act-Assert (AAA)
"""

import pytest


class TestActivitiesEndpoint:
    """Tests for the GET /activities endpoint"""
    
    def test_get_all_activities_returns_success(self, client, expected_activity_count):
        """
        Test that GET /activities returns status 200 and all activities.
        
        Arrange: Create test client
        Act: Make GET request to /activities
        Assert: Response status is 200 and contains expected number of activities
        """
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == expected_activity_count
    
    
    def test_activities_response_contains_expected_fields(self, client):
        """
        Test that each activity has all required fields.
        
        Arrange: Create test client
        Act: Make GET request to /activities
        Assert: Each activity has description, schedule, max_participants, participants
        """
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert - Check structure of each activity
        required_fields = ["description", "schedule", "max_participants", "participants"]
        for activity_name, activity_data in data.items():
            assert all(field in activity_data for field in required_fields), \
                f"Activity '{activity_name}' missing required fields"
    
    
    def test_activities_contains_chess_club(self, client):
        """
        Test that Chess Club activity is in the list.
        
        Arrange: Create test client
        Act: Make GET request to /activities
        Assert: Chess Club exists in activities
        """
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert "Chess Club" in data
        assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
    
    
    def test_activities_contains_all_default_activities(self, client, expected_activity_names):
        """
        Test that all default activities are present.
        
        Arrange: Create test client
        Act: Make GET request to /activities
        Assert: All expected activity names are in response
        """
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert set(data.keys()) == expected_activity_names
    
    
    def test_activities_have_participants_list(self, client):
        """
        Test that each activity has a participants list.
        
        Arrange: Create test client
        Act: Make GET request to /activities
        Assert: All activities have participants as a list
        """
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["participants"], list), \
                f"Activity '{activity_name}' participants should be a list"
