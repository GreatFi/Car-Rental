from django.urls import path
from . import views
urlpatterns = [
    path("", view=views.car_page, name="car_page")

]