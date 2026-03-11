"""
Tests for the student cancellation endpoint.

Tests the POST /activities/{activity_name}/cancel endpoint to ensure proper
validation, error handling, and successful cancellation behavior.

Pattern: Arrange-Act-Assert (AAA)
"""

import pytest


class TestCancellationEndpoint:
    """Tests for the POST /activities/{activity_name}/cancel endpoint"""
    
    def test_cancel_success(self, client, get_activity):
        """
        Test successful student cancellation from an activity.
        
        Arrange: Use a student already signed up for first activity
        Act: Make POST request to cancel endpoint
        Assert: Response status is 200 and confirmation message is returned
        """
        # Arrange
        activity_name = get_activity(0)
        email = "michael@mergington.edu"  # Already signed up per conftest
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/cancel",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        assert email in response.json()["message"]
    
    
    def test_cancel_removes_student_from_participants(self, client, get_activity):
        """
        Test that cancellation actually removes the student from activity.
        
        Arrange: Identify a signed-up student
        Act: Cancel student signup, then fetch activities
        Assert: Student email is no longer in activity's participants list
        """
        # Arrange
        activity_name = get_activity(8)
        email = "maya@mergington.edu"  # Already signed up per conftest
        
        # Verify student is initially registered
        initial_activities = client.get("/activities").json()
        assert email in initial_activities[activity_name]["participants"]
        
        # Act - Cancel signup
        response = client.post(
            f"/activities/{activity_name}/cancel",
            params={"email": email}
        )
        
        # Act - Verify student was removed
        final_activities = client.get("/activities").json()
        
        # Assert
        assert response.status_code == 200
        assert email not in final_activities[activity_name]["participants"]
    
    
    def test_cancel_activity_not_found(self, client):
        """
        Test cancellation fails with 404 when activity doesn't exist.
        
        Arrange: Create test data with invalid activity name and student email
        Act: Make POST request with non-existent activity
        Assert: Response status is 404 with appropriate error message
        """
        # Arrange
        activity_name = "Fictional Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/cancel",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    
    def test_cancel_student_not_signed_up(self, client, get_activity):
        """
        Test cancellation fails when student is not signed up.
        
        Arrange: Use a student not signed up for the activity (different from conftest)
        Act: Try to cancel a non-existent signup
        Assert: Response status is 400 with appropriate error message
        """
        # Arrange
        activity_name = get_activity(2)
        email = "notregistered@mergington.edu"  # Not signed up per conftest
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/cancel",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"].lower()
    
    
    def test_cancel_then_signup_again(self, client, get_activity):
        """
        Test that a student can re-sign up after canceling.
        
        Arrange: Use an already-registered student
        Act: Cancel signup, then sign up again
        Assert: Both operations succeed with correct status codes
        """
        # Arrange
        activity_name = get_activity(2)
        email = "john@mergington.edu"  # Already signed up per conftest
        
        # Verify initial state
        initial_activities = client.get("/activities").json()
        assert email in initial_activities[activity_name]["participants"]
        
        # Act - Cancel
        cancel_response = client.post(
            f"/activities/{activity_name}/cancel",
            params={"email": email}
        )
        
        # Act - Re-signup
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert cancel_response.status_code == 200
        assert signup_response.status_code == 200
        
        # Verify student is back in activity
        final_activities = client.get("/activities").json()
        assert email in final_activities[activity_name]["participants"]
    
    
    def test_cancel_multiple_students_from_same_activity(self, client, get_activity):
        """
        Test canceling multiple students from the same activity independently.
        
        Arrange: Identify multiple signed-up students in an activity
        Act: Cancel each student one by one
        Assert: Each cancellation succeeds; other students remain
        """
        # Arrange
        activity_name = get_activity(0)
        email1 = "michael@mergington.edu"  # Signed up per conftest
        email2 = "daniel@mergington.edu"   # Signed up per conftest
        
        # Act - Cancel first student
        response1 = client.post(
            f"/activities/{activity_name}/cancel",
            params={"email": email1}
        )
        
        # Act - Cancel second student
        response2 = client.post(
            f"/activities/{activity_name}/cancel",
            params={"email": email2}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify both are removed
        final_activities = client.get("/activities").json()
        assert email1 not in final_activities[activity_name]["participants"]
        assert email2 not in final_activities[activity_name]["participants"]
    
    
    def test_cancel_student_from_multiple_activities(self, client, get_activity):
        """
        Test canceling the same student from different activities.
        
        Arrange: Sign student up for two activities, then cancel from one
        Act: Cancel from first activity, then cancel from second
        Assert: Both cancellations succeed; student removed from both
        """
        # Arrange
        email = "multicanceler@mergington.edu"
        activity1 = get_activity(1)
        activity2 = get_activity(4)
        
        # First, sign up for both activities
        client.post(f"/activities/{activity1}/signup", params={"email": email})
        client.post(f"/activities/{activity2}/signup", params={"email": email})
        
        # Act - Cancel from first activity
        response1 = client.post(
            f"/activities/{activity1}/cancel",
            params={"email": email}
        )
        
        # Act - Cancel from second activity
        response2 = client.post(
            f"/activities/{activity2}/cancel",
            params={"email": email}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify student is removed from both
        final_activities = client.get("/activities").json()
        assert email not in final_activities[activity1]["participants"]
        assert email not in final_activities[activity2]["participants"]
    
    
    def test_cancel_empty_email(self, client, get_activity):
        """
        Test cancellation with empty email parameter.
        
        Arrange: Prepare request with empty email string
        Act: Make POST request with empty email
        Assert: Response indicates error since empty email is not enrolled
        """
        # Arrange
        activity_name = get_activity(7)
        email = ""
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/cancel",
            params={"email": email}
        )
        
        # Assert
        # Empty string was never signed up, so cancellation should fail with 400
        assert response.status_code == 400
