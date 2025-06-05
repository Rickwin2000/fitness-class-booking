import pytest
from django.urls import reverse
from rest_framework import status
from django.utils import timezone

from booking.models import FitnessClass, Booking
from booking.tests.confest import api_client, fitness_class


@pytest.mark.django_db
class TestBookingAPI:

    def test_successful_booking(self, api_client, fitness_class):
        fitness_class_data = {
            "available_slots": 5
        }
        fitness_class_instance = fitness_class(data=fitness_class_data)
        url = reverse('book')
        data = {
            "fitness_class_id": fitness_class_instance.id,
            "client_name": "Elon",
            "client_email": "test@example.com"
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        response_json = response.json()["data"]
        assert response_json["client_email"] == "test@example.com"
        assert response_json["fitness_class_id"] ==  fitness_class_instance.id
        fitness_class_instance.refresh_from_db()
        assert fitness_class_instance.available_slots == 4
    
    def test_booking_required_fields_validation(self, api_client):
        url = reverse('book')
        data = {}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_json = response.json()["errors"]
    
        assert "client_name" in response_json
        assert response_json["client_name"] == ["This field is required."]

        assert "client_email" in response_json
        assert response_json["client_email"] == ["This field is required."]

        assert "fitness_class_id" in response_json
        assert response_json["fitness_class_id"] == ["This field is required."]
    
    def test_booking_invalid_class_and_email(self, api_client):
        url = reverse('book')
        invalid_class_id = 100
        data = {
            "fitness_class_id": invalid_class_id,
            "client_email": "test"
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_json = response.json()["errors"]

        assert "fitness_class_id" in response_json
        assert f"Invalid pk \"{invalid_class_id}\" - object does not exist." in response_json["fitness_class_id"]

        assert "client_email" in response_json
        assert "Enter a valid email address." in response_json["client_email"]

    def test_booking_same_user_twice(self, api_client, fitness_class):
        fitness_class_data = {
            "available_slots": 5
        }
        fitness_class_instance = fitness_class(data=fitness_class_data)
        url = reverse('book')
        data = {
            "fitness_class_id": fitness_class_instance.id,
            "client_name": "Elon",
            "client_email": "test@example.com"
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_json = response.json()["errors"]        
        assert "you are already registered for this class" in str(response_json).lower()

    def test_booking_past_class(self, api_client, fitness_class):
        fitness_class_data = {
            "datetime": timezone.now() - timezone.timedelta(days=1)
        }
        fitness_class_instance = fitness_class(data=fitness_class_data)
        url = reverse('book')
        data = {
            "fitness_class_id": fitness_class_instance.id,
            "client_email": "late@example.com"
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_json = response.json()["errors"] 
        assert "only upcoming classes can be booked" in str(response_json).lower()

    def test_booking_no_slots(self, api_client, fitness_class):
        fitness_class_data = {
            "available_slots": 0
        }
        fitness_class_instance = fitness_class(data=fitness_class_data)
    
        url = reverse('book')
        data = {
            "fitness_class_id": fitness_class_instance.id,
            "client_email": "full@example.com"
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_json = response.json()["errors"] 
        assert "no available slots for this class." in str(response_json).lower()
