from django.db import models
from datetime import timedelta
from django.utils import timezone
# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    FUEL_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('Electric', 'Electric'),
        ('Hybrid', 'Hybrid'),
    ]

    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='vehicles')
    name = models.CharField(max_length=150)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    model_year = models.PositiveSmallIntegerField()
    seats = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to='vehicles/')
    image_2 = models.ImageField(upload_to="vehicles/", blank=True)
    image_3 = models.ImageField(upload_to="vehicles/", blank=True)
    image_4 = models.ImageField(upload_to="vehicles/", blank=True)
    image_5 = models.ImageField(upload_to="vehicles/", blank=True)
    features = models.TextField(blank=True, help_text="One feature per line")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand.name} {self.name}"


    @property
    def features_list(self):
        # splits the textarea into a clean list for the template
        return [f.strip() for f in self.features.splitlines() if f.strip()]

    def is_available_for(self, start, end, exclude=None):
        # a booking clashes if it starts before our end AND ends after our start;
        # strict < and > allow same-day handover (one leaves, next arrives)
        clashes = self.bookings.filter(
            status__in=["pending", "confirmed"],  # cancelled bookings don't block
            start_date__lt=end,
            end_date__gt=start,
        )
        if exclude:
            clashes = clashes.exclude(pk=exclude)  # ignore itself when re-checking
        return not clashes.exists()

    @property
    def is_available_today(self):
        today = timezone.localdate()
        return self.is_available_for(today, today + timedelta(days=1))

    @property
    def is_available(self):
        return self.is_available_today  # the badge on the cards uses this

    @property
    def gallery_images(self):
        photos = (self.image, self.image_2, self.image_3, self.image_4, self.image_5)
        return [photo for photo in photos if photo]