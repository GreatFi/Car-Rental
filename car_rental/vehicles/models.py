from django.db import models

# Create your models here.
from django.db import models


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
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand.name} {self.name}"