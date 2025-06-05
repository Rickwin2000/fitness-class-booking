import pytest
from django.urls import reverse
from rest_framework import status

from booking.tests.confest import api_client, fitness_class, booking


@pytest.mark.django_db
class TestBookingListAPI:

    def test_list_empty_bookings(self, api_client):
        url = reverse('bookings')
        response = api_client.get(url)
        response_json = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response_json, list)
        assert len(response_json) == 0

    def test_list_booking(self, api_client, booking):
        url = reverse('bookings')
        email = "elon@gmail.com"
        data = {
            "client_email": email
        }
        booking(data=data)

        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()
        assert isinstance(response_json, list)
        assert len(response_json) == 0

        response = api_client.get(url, {"client_email": email})
        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()
        assert isinstance(response_json, list)
        assert len(response_json) >= 1
        assert all(val["client_email"] == email for val in response_json)