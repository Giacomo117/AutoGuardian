import geopy
import geopy.distance
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Contact(models.Model):
    """
    Model to store contact information.
    """
    phoneNumber = models.CharField(default=None, max_length=20)


class User(AbstractUser):
    """
    Custom user model extending AbstractUser.

    Attributes:
        vehicles (ManyToManyField): Vehicles associated with the user.
        contacts (ManyToManyField): Contacts associated with the user for alerts.
    """
    vehicles = models.ManyToManyField('Vehicle', related_name='owners')
    contacts = models.ManyToManyField('Contact', related_name='alert_contacts')


class Vehicle(models.Model):
    """
    Model to store vehicle information.

    Attributes:
        id (IntegerField): Primary key for the vehicle.
        latitude (FloatField): Latitude coordinate of the vehicle.
        longitude (FloatField): Longitude coordinate of the vehicle.
        smoke (FloatField): Smoke level detected by the vehicle.
        temperature (FloatField): Temperature recorded by the vehicle.
    """
    id = models.IntegerField(primary_key=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    smoke = models.FloatField(default=0)
    temperature = models.FloatField(default=0)
    last_update = models.TimeField(default=timezone.now)
    humidity = models.FloatField(default=0)

    def get_vehicles_in_range(self, radius):
        """
        Returns all vehicles within a certain radius from this alert.

        Args:
            radius (float): The radius within which to search for vehicles (in kilometers).

        Returns:
            list: A list containing the vehicles within the specified radius.
        """

        vehicles_in_range = []
        for vehicle in Vehicle.objects.exclude(pk=self.id):
            vehicle_point = (vehicle.latitude, vehicle.longitude)
            distance = geopy.distance.geodesic((self.latitude, self.longitude), vehicle_point).kilometers
            if distance <= radius:
                vehicles_in_range.append(vehicle)

        return vehicles_in_range


class Alert(models.Model):
    """
    Model to store alert information.

    Attributes:
        sender (ForeignKey): Vehicle sending the alert.
        receivers (ManyToManyField): Vehicles receiving the alert.
        latitude (FloatField): Latitude coordinate of the alert.
        longitude (FloatField): Longitude coordinate of the alert.
        smoke (FloatField): Smoke level detected by the alert.
        temperature (FloatField): Temperature recorded by the alert.
        date (DateTimeField): Date and time when the alert was created.
        recent (BooleanField): Flag indicating if the alert is recent or not.
    """

    sender = models.ForeignKey(Vehicle, related_name='alerts_sent', on_delete=models.CASCADE)
    receivers = models.ManyToManyField(Vehicle, related_name='alerts_received', default=None)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    smoke = models.FloatField(default=0)
    temperature = models.FloatField(default=0)
    date = models.DateTimeField(default=timezone.now)
    recent = models.BooleanField(default=0)
    humidity = models.FloatField(default=0)
    s = models.BooleanField(default=0)
    t = models.BooleanField(default=0)
    u = models.BooleanField(default=0)

    def check_neighboring_vehicles(self, radius, threshold_percentage=0):
        """
        Check neighboring vehicles for similar temperature and smoke values.

        Args:
            radius (float): The radius within which to search for neighboring vehicles (in kilometers).
            threshold_percentage (float): The percentage threshold for similarity comparison.

        Returns:
            bool: True if neighboring vehicles have similar values, False otherwise.
        """
        alert_point = (self.latitude, self.longitude)

        for vehicle in Vehicle.objects.exclude(pk=self.sender.id):
            vehicle_point = (vehicle.latitude, vehicle.longitude)
            distance = geopy.distance.geodesic(alert_point, vehicle_point).kilometers
            if distance <= radius:
                temperature_difference = abs((vehicle.temperature - self.temperature) / self.temperature) * 100
                smoke_difference = abs((vehicle.smoke - self.smoke) / self.smoke) * 100
                if temperature_difference <= threshold_percentage or smoke_difference <= threshold_percentage:
                    return True

        return False

    def get_vehicles_in_range(self, radius):
        """
        Returns all vehicles within a certain radius from this alert.

        Args:
            radius (float): The radius within which to search for vehicles (in kilometers).

        Returns:
            list: A list containing the vehicles within the specified radius.
        """

        vehicles_in_range = []
        for vehicle in Vehicle.objects.exclude(pk=self.sender.id):
            vehicle_point = (vehicle.latitude, vehicle.longitude)
            distance = geopy.distance.geodesic((self.latitude, self.longitude), vehicle_point).kilometers
            if distance <= radius:
                vehicles_in_range.append(vehicle)

        return vehicles_in_range
