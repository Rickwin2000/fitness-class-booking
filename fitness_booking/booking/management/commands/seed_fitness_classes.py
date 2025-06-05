import random
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from booking.models import FitnessClass


class Command(BaseCommand):
    help = 'Seed the database with sample FitnessClass data if not already present.'

    def handle(self, *args, **kwargs):
        instructors = ['Alice', 'Bob', 'Charlie', 'Diana']
        class_names = ['Yoga', 'Zumba', 'HIIT', 'Pilates', 'Cardio Blast']
        created_count = 0

        for _ in range(10):
            name = random.choice(class_names)
            instructor = random.choice(instructors)

            day_offset = random.randint(-10, 10)
            hour = random.randint(6, 19)
            datetime_val = datetime.now().replace(hour=hour, minute=0, second=0, microsecond=0) + timedelta(days=day_offset)

            total_slots = random.randint(10, 30)
            available_slots = random.randint(0, total_slots)

            obj, created = FitnessClass.objects.get_or_create(
                name=name,
                datetime=datetime_val,
                instructor=instructor,
                defaults={
                    'total_slots': total_slots,
                    'available_slots': available_slots,
                }
            )

            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Seed complete. {created_count} new fitness classes created."))
