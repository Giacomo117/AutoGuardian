from django.http import Http404, HttpResponse
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView

from REST.models import Vehicle, Alert
from REST.serializers import VehicleSerializer, AlertSerializer


def get_vehicle_object(vehicle_id):
    """Get a vehicle object by its ID.

    Args:
        vehicle_id (int): The ID of the vehicle to retrieve.

    Raises:
        Http404: If the vehicle with the specified ID does not exist.

    Returns:
        Vehicle: The vehicle object.
    """
    try:
        return Vehicle.objects.get(id=vehicle_id)
    except Vehicle.DoesNotExist:
        raise Http404


class VehiclesAPI(APIView):
    """API endpoint for handling vehicle instances."""

    def get(self, request, vehicle_id=None):
        """Handle GET requests.

        Args:
            request: The request object.
            vehicle_id (int, optional): The ID of the vehicle to retrieve.

        Returns:
            JsonResponse: JSON response containing vehicle data.
        """
        if vehicle_id is not None:
            vehicle = get_vehicle_object(vehicle_id)
            serializer = VehicleSerializer(vehicle)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        else:
            vehicles = Vehicle.objects.all()
            serializer = VehicleSerializer(vehicles, many=True)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    def put(self, request, vehicle_id):
        """Handle PUT requests.

        Args:
            request: The request object.
            vehicle_id (int): The ID of the vehicle to update.

        Returns:
            HttpResponse: HTTP response indicating success or failure.
        """
        vehicle = get_vehicle_object(vehicle_id)
        serializer = VehicleSerializer(vehicle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            vehicle.last_update = timezone.now()
            return HttpResponse(status=status.HTTP_200_OK)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, vehicle_id):
        """Handle DELETE requests.

        Args:
            request: The request object.
            vehicle_id (int): The ID of the vehicle to delete.

        Returns:
            HttpResponse: HTTP response indicating success or failure.
        """
        try:
            vehicle = get_vehicle_object(vehicle_id)
            vehicle.delete()
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        except:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """Handle POST requests.

        Args:
            request: The request object.

        Returns:
            HttpResponse: HTTP response indicating success or failure.
        """
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(status=status.HTTP_201_CREATED)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


class AlertsAPI(APIView):

    def get(self, request):
        """Handle GET requests.

        Args:
            request: The request object.

        Returns:
            JsonResponse: JSON response containing alerts data.
        """

        vehicles = Alert.objects.all()
        serializer = AlertSerializer(vehicles, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    def post(self, request):
        """Handle POST requests."""
        serializer = AlertSerializer(data=request.data)
        if serializer.is_valid():
            alert = serializer.save()
            if not alert.check_neighboring_vehicles(radius=5):
                vehicles_in_range = alert.get_vehicles_in_range(radius=5)
                alert.receivers.set(vehicles_in_range)
                return HttpResponse(status=status.HTTP_201_CREATED)
            else:
                alert.delete()
                return HttpResponse("Neighboring vehicles with similar values found. Alert not created.",
                                    status=status.HTTP_200_OK)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


class UserAPI(APIView):
    def get(self, request, vehicle_id):
        """Handle GET requests.

        Args:
            request: The request object.
            vehicle_id: The id of the vehicle.

        Returns:
            JsonResponse: JSON response containing user data.
        """
        try:
            vehicle = Vehicle.objects.get(pk=vehicle_id)
        except Vehicle.DoesNotExist:
            return JsonResponse({"error": "Vehicle does not exist."}, status=status.HTTP_404_NOT_FOUND)

        user = vehicle.owners.first()  # Assuming the vehicle has only one owner
        if user:
            contacts = user.contacts.all().values_list('phoneNumber', flat=True)  # Get phone numbers of the user
            return JsonResponse({"phone_numbers": list(contacts)}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No user found for the given vehicle."}, status=status.HTTP_404_NOT_FOUND)


class NeighboringVehiclesAPI(APIView):
    def get(self, request, vehicle_id):
        """
        Retrieve the IDs of neighboring vehicles given a vehicle ID.

        Args:
            request: The request object.
            vehicle_id (int): The ID of the vehicle.

        Returns:
            JsonResponse: JSON response containing the IDs of neighboring vehicles.
        """
        try:
            vehicle = Vehicle.objects.get(pk=vehicle_id)
        except Vehicle.DoesNotExist:
            return JsonResponse({"error": "Vehicle does not exist."}, status=404)

        vehicles_in_range = vehicle.get_vehicles_in_range(radius=5)
        neighboring_vehicle_ids = [v.id for v in vehicles_in_range]

        return JsonResponse({"neighboring_vehicle_ids": neighboring_vehicle_ids}, status=200)
