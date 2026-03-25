"""
Transport models - Bus routes and vehicle management.
"""
from django.db import models
from apps.core.models import TimeStampedModel, ActiveModel


class Route(TimeStampedModel, ActiveModel):
    """Bus route details."""
    route_number = models.CharField(max_length=20, unique=True)
    route_name = models.CharField(max_length=200)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    distance_km = models.DecimalField(max_digits=6, decimal_places=2)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['route_number']
        verbose_name = 'Route'
        verbose_name_plural = 'Routes'

    def __str__(self):
        return f"Route {self.route_number}: {self.route_name}"


class Stop(TimeStampedModel):
    """Bus stop details."""
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stops')
    stop_name = models.CharField(max_length=100)
    stop_order = models.PositiveIntegerField()
    pickup_time = models.TimeField(blank=True, null=True)
    drop_time = models.TimeField(blank=True, null=True)

    class Meta:
        ordering = ['route', 'stop_order']
        verbose_name = 'Stop'
        verbose_name_plural = 'Stops'

    def __str__(self):
        return f"{self.route.route_number} - {self.stop_name}"


class Vehicle(TimeStampedModel, ActiveModel):
    """Vehicle/Bus details."""
    vehicle_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=50, default='Bus')
    capacity = models.PositiveIntegerField(default=50)
    driver_name = models.CharField(max_length=100)
    driver_phone = models.CharField(max_length=15)
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True, related_name='vehicles')

    class Meta:
        ordering = ['vehicle_number']
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'

    def __str__(self):
        return f"{self.vehicle_number} - {self.driver_name}"


class TransportAssignment(TimeStampedModel):
    """Student transport assignment."""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    student = models.OneToOneField('students.Student', on_delete=models.CASCADE, related_name='transport')
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    pickup_stop = models.ForeignKey(Stop, on_delete=models.CASCADE, related_name='pickups')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    class Meta:
        verbose_name = 'Transport Assignment'
        verbose_name_plural = 'Transport Assignments'

    def __str__(self):
        return f"{self.student.roll_number} - Route {self.route.route_number}"