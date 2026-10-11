from django.shortcuts import render
from vehicles.models import Brand, Vehicle

# Create your views here.
# view for the home page
def home(request):
    return render(request, 'home.html', {
        'brands': Brand.objects.all(),
        'vehicles': Vehicle.objects.select_related('brand')[:6],
    })

