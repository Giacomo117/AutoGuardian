from django.urls import path

from REST.views import *

urlpatterns = [
    path('vehicles/', VehiclesAPI.as_view(), name='vehicle-api'),
    # Endpoint to get all vehicles or create a new one
    path('vehicles/<int:vehicle_id>/', VehiclesAPI.as_view(), name='vehicle-api-id'),
    # Endpoint to get, update or delete a specific vehicle by its ID
    path('alerts/', AlertsAPI.as_view(), name='alert-api'),
    # Endpoint to get all alerts or create a new one
    path('contacts/<int:vehicle_id>', UserAPI.as_view()),
    # Endpoint to get contacts related to a specific vehicle
    path('neighboring-vehicles/<int:vehicle_id>/', NeighboringVehiclesAPI.as_view(), name='neighboring-vehicles-api'),
    # Endpoint to get neighboring vehicles given a vehicle ID
]
