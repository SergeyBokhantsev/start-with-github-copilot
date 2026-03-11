"""
Tests for the student signup endpoint.

Tests the POST /activities/{activity_name}/signup endpoint to ensure proper
validation, error handling, and successful signup behavior.

Pattern: Arrange-Act-Assert (AAA)
"""

import pytest


class TestSignupEndpoint:
    """Tests for the POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_success(self, client, get_activity):
        """
        Test successful student signup for an activity.
        
        Arrange: Create test data with valid activity and new student email
        Act: Make POST request to signup endpoint
        Assert: Response status is 200 and confirmation message is returned
        """
        # Arrange
        activity_name = get_activity(0)
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert email in response.json()["message"]
    
    
    def test_signup_adds_student_to_participants(self, client, get_activity):
        """
        Test that signup actually adds the student to activity participants.
        
        Arrange: Get initial activity state, prepare new student email
        Act: Sign up student, then fetch activities
        Assert: Student email appears in activity's participants list
        """
        # Arrange
        activity_name = get_activity(1)
        email = "neowstudent@mergington.edu"
        
        # Act - Sign up
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Act - Verify student was added
        activities = client.get("/activities").json()
        
        # Assert
        assert response.status_code == 200
        assert email in activities[activity_name]["participants"]
    
    
    def test_signup_activity_not_found(self, client):
        """
        Test signup fails with 404 when activity doesn't exist.
        
        Arrange: Create test data with invalid activity name
        Act: Make POST request with non-existent activity
        Assert: Response status is 404 with appropriate error message
        """
        # Arrange
        activity_name = "Non-existent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    
    def test_signup_duplicate_student(self, client, get_activity):
        """
        Test signup fails when student is already signed up.
        
        Arrange: Use an already-registered student in first activity
        Act: Try to sign up the same student again
        Assert: Response status is 400 with duplicate signup error
        """
        # Arrange
        activity_name = get_activity(0)
        email = "michael@mergington.edu"  # Already signed up per conftest
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()
    
    
    def test_signup_multiple_students_for_same_activity(self, client, get_activity):
        """
        Test that multiple different students can sign up for the same activity.
        
        Arrange: Prepare two different student emails
        Act: Sign up first student, then second student
        Assert: Both signups succeed with status 200
        """
        # Arrange
        activity_name = get_activity(4)
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        
        # Act - First signup
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email1}
        )
        
        # Act - Second signup
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email2}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify both are in participants
        activities = client.get("/activities").json()
        assert email1 in activities[activity_name]["participants"]
        assert email2 in activities[activity_name]["participants"]
    
    
    def test_signup_student_can_join_multiple_activities(self, client, get_activity):
        """
        Test that the same student can sign up for different activities.
        
        Arrange: Prepare one student email and two activities
        Act: Sign up student for activity 1, then activity 2
        Assert: Both signups succeed and student appears in both activities
        """
        # Arrange
        email = "versatile@mergington.edu"
        activity1 = get_activity(6)
        activity2 = get_activity(7)
        
        # Act - Sign up for first activity
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"email": email}
        )
        
        # Act - Sign up for second activity
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify student is in both activities
        activities = client.get("/activities").json()
        assert email in activities[activity1]["participants"]
        assert email in activities[activity2]["participants"]
    
    
    def test_signup_empty_email(self, client, get_activity):
        """
        Test signup with empty email parameter.
        
        Arrange: Prepare request with empty email string
        Act: Make POST request with empty email
        Assert: Empty email string is technically allowed (no validation in current app)
        """
        # Arrange
        activity_name = get_activity(8)
        email = ""
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        # Current app allows empty string (no email validation)
        # This test documents that behavior
        assert response.status_code == 200
