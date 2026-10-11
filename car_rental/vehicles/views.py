from django.shortcuts import render

# Create your views here.

# view for the car list page
def car_page(request):
    return render(request, 'vehicles/cars_page.html')