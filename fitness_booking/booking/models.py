from django.db import models


class FitnessClass(models.Model):
    name = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    instructor = models.CharField(max_length=100)
    total_slots = models.PositiveIntegerField()
    available_slots = models.PositiveIntegerField()

    class Meta:
        db_table = "fitness_class"
        verbose_name = "Fitness Class"
        verbose_name_plural = "Fitness Classes"

    def __str__(self):
        return f"Fitness Class - {self.id}"


class Booking(models.Model):
    fitness_class_id = models.ForeignKey(FitnessClass, on_delete=models.PROTECT)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "booking"
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    def __str__(self):
        return f"Booking - {self.id}"
