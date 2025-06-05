from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from booking.models import FitnessClass, Booking
from booking.serializers import FitnessClassSerializer, BookingSerializer


class FitnessClassList(generics.ListAPIView):
    today = timezone.now()
    queryset = FitnessClass.objects.filter(datetime__gt=today)
    serializer_class = FitnessClassSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class BookClass(APIView):
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save()
            return Response({
                "success": True,
                "message": "Booking successful.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "success": False,
            "message": "Booking failed due to invalid input.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class BookingList(generics.ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        email = self.request.query_params.get('client_email')
        if not email:
            return Booking.objects.none()
        return Booking.objects.filter(client_email=email)
