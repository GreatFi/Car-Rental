from django.urls import path
from . import views
urlpatterns = [
    path("", view=views.car_page, name="car_page"),
    path("<int:vehicle_id>/", view=views.car_details, name="car_details"),
]