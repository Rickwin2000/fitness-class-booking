from django.urls import path
from booking import views

urlpatterns = [
    path('classes/', views.FitnessClassList.as_view(), name='classes'),
    path('book/', views.BookClass.as_view(), name='book'),
    path('bookings/', views.BookingList.as_view(), name='bookings'),
]
