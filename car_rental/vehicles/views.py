from django.shortcuts import render
from .models import Vehicle
# Create your views here.

# view for the car list page
def car_page(request):
    vehicles = Vehicle.objects.select_related('brand')
    return render(request, 'vehicles/cars_page.html', {'vehicles': vehicles})


def car_details(request, vehicle_id):
    vehicle = Vehicle.objects.select_related('brand').get(id=vehicle_id)
    return render(request, 'vehicles/car_details.html', {'vehicle': vehicle})