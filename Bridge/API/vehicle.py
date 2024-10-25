class Vehicle:
    """A class to represent a vehicle."""

    def __init__(self):
        """Initializes a Vehicle object."""
        self.id = None
        self.latitude = None
        self.longitude = None
        self.smoke = None
        self.temperature = None

    def serialize(self):
        """
        Serializes the Vehicle object into a string.

        Returns:
            str: A string representation of the Vehicle object.
        """
        return str({
            "id": self.id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "smoke": self.smoke,
            "temperature": self.temperature
        })

    def __str__(self):
        """
        Returns a string representation of the Vehicle object.

        Returns:
            str: A string representation of the Vehicle object.
        """
        return self.serialize()


class VehicleFactory:
    """A factory class to create Vehicle objects."""

    @staticmethod
    def create_vehicle(vehicle_info):
        """
        Creates a Vehicle object from the provided vehicle_info dictionary.

        Args:
            vehicle_info (dict): A dictionary containing vehicle information.

        Returns:
            Vehicle: A Vehicle object initialized with the provided information.
        """
        vehicle = Vehicle()
        vehicle.id = vehicle_info.get("id")
        vehicle.latitude = vehicle_info.get("latitude")
        vehicle.longitude = vehicle_info.get("longitude")
        vehicle.smoke = vehicle_info.get("smoke")
        vehicle.temperature = vehicle_info.get("temperature")
        return vehicle
