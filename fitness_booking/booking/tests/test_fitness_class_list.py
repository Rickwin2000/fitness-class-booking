import pytest
from django.urls import reverse
from rest_framework import status
from django.utils import timezone

from booking.tests.confest import api_client, fitness_class


@pytest.mark.django_db
class TestFitnessClassAPI:

    def test_list_empty_fitness_class(self, api_client, fitness_class):
        url = reverse('classes')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
        assert len(response.json()) == 0

    def test_list_fitness_class(self, api_client, fitness_class):
        url = reverse('classes')
        fitness_class()
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
        assert len(response.json()) >= 1
    
    def test_list_future_fitness_class(self, api_client, fitness_class):
        today = timezone.now()
        url = reverse('classes')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert all(val.datetime > today for val in response.json())
    
    def test_list_past_fitness_class(self, api_client, fitness_class):
        name = "Elon"
        data = {
            "datetime": timezone.now() - timezone.timedelta(days=1),
            "name": name
        }
        fitness_class(data=data)
        url = reverse('classes')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert all(val["name"] != name for val in response.json())
       