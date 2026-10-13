from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from vehicles.models import Vehicle

from .forms import BookingForm
from .models import Booking


@login_required  # guests are sent to login, then back here via ?next=
def book(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    # pre-built booking so Booking.clean() can see the user and vehicle
    booking = Booking(user=request.user, vehicle=vehicle)

    if request.method == "POST":
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()  # total_price is calculated in Booking.save()
            messages.success(request, "Booking received. It is pending confirmation.")
            return redirect("bookings:history")  # redirect after POST stops resubmits
    else:
        form = BookingForm(instance=booking)

    return render(request, "bookings/book.html", {"form": form, "vehicle": vehicle})


@login_required
def history(request):
    # only the logged-in user's bookings; select_related avoids a query per row
    bookings = request.user.bookings.select_related("vehicle")
    return render(request, "bookings/history.html", {"bookings": bookings})