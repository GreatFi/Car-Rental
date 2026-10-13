from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings"
    )
    vehicle = models.ForeignKey(
        "vehicles.Vehicle", on_delete=models.PROTECT, related_name="bookings"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    # editable=False keeps it out of forms and the admin; we set it in save()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        ordering = ["-created_at"]

    @property
    def days(self):
        return (self.end_date - self.start_date).days

    def clean(self):
        # runs through forms, or when you call full_clean() yourself
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValidationError("End date must be after the start date.")
            if self.status != self.Status.CANCELLED and not self.vehicle.is_available_for(
                self.start_date, self.end_date, exclude=self.pk
            ):
                raise ValidationError("This car is not available for those dates.")

    def save(self, *args, **kwargs):
        if self._state.adding:
            # price is frozen at booking time, so later price changes don't alter it
            self.total_price = self.days * self.vehicle.price_per_day
        super().save(*args, **kwargs)