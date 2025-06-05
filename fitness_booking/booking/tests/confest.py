import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from booking.models import FitnessClass, Booking


@pytest.fixture
def fitness_class():
    def _create_fitness_class(data=None):
        payload = {
            "name": "Yoga",
            "datetime": timezone.now() + timezone.timedelta(days=1),
            "instructor": "John",
            "total_slots": 10,
            "available_slots": 5,
        }
        if data:
            payload.update(data)
        return FitnessClass.objects.create(**payload)
    return _create_fitness_class

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def booking(fitness_class):
    def _create_booking(data=None):
        fitness_class_instance = fitness_class()
        payload = {
            "client_name": "Jane Doe",
            "client_email": "jane@example.com",
            "fitness_class_id": fitness_class_instance,
        }
        if data:
            payload.update(data)
        return Booking.objects.create(**payload)
    return _create_booking