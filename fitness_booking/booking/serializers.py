from rest_framework import serializers
from django.utils import timezone
from django.db import transaction

from booking.models import FitnessClass, Booking


class FitnessClassSerializer(serializers.ModelSerializer):
    datetime = serializers.SerializerMethodField()

    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'datetime', 'instructor', 'available_slots']

    def get_datetime(self, obj):
        return timezone.localtime(obj.datetime).isoformat()


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ['id', 'booked_at']

    def validate_fitness_class_id(self, fitness_class_id):
        today = timezone.now()

        if fitness_class_id and fitness_class_id.datetime < today:
            raise serializers.ValidationError("Only upcoming classes can be booked")

        if fitness_class_id and fitness_class_id.available_slots <= 0:
            raise serializers.ValidationError("No available slots for this class.")
        
        return fitness_class_id
    
    def validate_client_email(self, client_email):
        fitness_class_id = self.initial_data.get("fitness_class_id")
        if (
            fitness_class_id 
            and client_email
            and Booking.objects.filter(client_email=client_email, fitness_class_id=fitness_class_id).exists()
        ):
            raise serializers.ValidationError("You are already registered for this class")
        return client_email

    @transaction.atomic
    def create(self, validated_data):
        fitness_class = validated_data.get('fitness_class_id')
        booking = Booking.objects.create(**validated_data)

        fitness_class.available_slots -= 1
        fitness_class.save()
        return booking
