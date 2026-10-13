from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    path("", views.history, name="history"),
    path("book/<int:vehicle_id>/", views.book, name="book"),
]