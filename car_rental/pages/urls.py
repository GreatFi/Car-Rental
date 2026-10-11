from django.urls import path
from . import views

# urls for the pages app
urlpatterns = [
    path("", view=views.home, name="home"),
]