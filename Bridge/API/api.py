import json
from configparser import ConfigParser

import requests

from API.vehicle import VehicleFactory


class VehicleAPI:
    """A class to interact with the vehicle API."""

    def __init__(self):
        """Initializes VehicleAPI."""
        # Reads server configuration from an ini file
        config_object = ConfigParser()
        config_object.read("config.ini")

        # Extracts fields from the config file
        self.FIELDS = []
        if "VEHICLE_FIELDS" in config_object:
            fields_section = config_object["VEHICLE_FIELDS"]
            self.FIELDS = [fields_section[field] for field in fields_section]
        if "SERVERCONFIG" in config_object:
            # Builds the URI for API requests using config values
            server = config_object["SERVERCONFIG"]
            self.url = 'http://' + server["HOST"] + ':' + server["PORT"] + '/' + server["VEHICLES_ENDPOINT"]

    def get_all_vehicles(self):
        """
        Retrieves all vehicles from the API.

        Returns:
            Tuple: A tuple containing status_code and vehicle objects, or (status_code, None).
        """
        response = requests.get(url=self.url)
        if response.status_code == 200:
            vehicles_info = response.json()
            vehicles = [VehicleFactory.create_vehicle(vehicle_info) for vehicle_info in vehicles_info]
            return response.status_code, vehicles
        else:
            return response.status_code, None

    def get_vehicle_by_id(self, vehicle_id):
        """
        Retrieves a specific vehicle from the API by its ID.

        Args:
            vehicle_id (str): Vehicle's ID.

        Returns:
            Tuple: A tuple containing status_code and JSON object of the vehicle, or (status_code, None).
        """
        specific_url = f"{self.url}{vehicle_id}/"
        response = requests.get(url=specific_url)
        if response.status_code == 200:
            vehicle_info = response.json()
            vehicle = VehicleFactory.create_vehicle(vehicle_info)
            return response.status_code, vehicle
        else:
            return response.status_code, None

    def delete_vehicle_by_id(self, vehicle_id):
        """
        Deletes a vehicle from the API by its ID.

        Args:
            vehicle_id (str): Vehicle's ID.

        Returns:
            int: Status code.
        """
        specific_url = f"{self.url}{vehicle_id}/"
        response = requests.delete(url=specific_url)
        return response.status_code

    def create_vehicle(self, data):
        """
        Creates a new vehicle in the API.

        Args:
            data (dict): Dictionary of data.

        Returns:
            Tuple: A tuple containing status_code and vehicle.
        """
        if set(data.keys()) != set(self.FIELDS):
            raise Exception("Error in data format. The dictionary must include these fields:" + str(self.FIELDS))
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=self.url, data=json.dumps(data), headers=headers)
        if response.status_code == 201:
            return response.status_code, VehicleFactory.create_vehicle(data)
        else:
            return response.status_code, None

    def update_vehicle(self, vehicle_id, data):
        """
        Updates a specific vehicle in the API by its ID.

        Args:
            vehicle_id (str): Vehicle's ID.
            data (dict): Dictionary of data to update.

        Returns:
            Tuple: A tuple containing status_code and vehicle.
        """
        if set(data.keys()) != set(self.FIELDS):
            raise Exception("Error in data format. The dictionary must include these fields:" + str(self.FIELDS))
        specific_url = f"{self.url}{vehicle_id}/"
        response = requests.put(url=specific_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            return response.status_code, VehicleFactory.create_vehicle(data)
        else:
            return response.status_code, None


class AlertsAPI:
    """A class to interact with the alerts API."""

    def __init__(self):
        """Initializes AlertsAPI."""
        # Reads server configuration from an ini file
        config_object = ConfigParser()
        config_object.read("config.ini")

        # Extracts fields from the config file
        self.FIELDS = []
        if "ALERT_FIELDS" in config_object:
            fields_section = config_object["ALERT_FIELDS"]
            self.FIELDS = [fields_section[field] for field in fields_section]

        if "SERVERCONFIG" in config_object:
            # Builds the URI for API requests using config values
            server = config_object["SERVERCONFIG"]
            self.url = 'http://' + server["HOST"] + ':' + server["PORT"] + '/' + server["ALERTS_ENDPOINT"]

    def create_alert(self, data):
        """
        Creates a new alert in the API.

        Args:
            data (dict): Dictionary of data.

        Returns:
            int: Status code.
        """
        if set(data.keys()) != set(self.FIELDS):
            raise Exception("Error in data format. The dictionary must include these fields:" + str(self.FIELDS))
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=self.url, data=json.dumps(data), headers=headers)
        return response.status_code


class NeighboringVehiclesAPI:
    """A class to interact with the neighboring vehicles API."""

    def __init__(self):
        """Initializes NeighboringVehiclesAPI."""
        # Reads server configuration from an ini file
        config_object = ConfigParser()
        config_object.read("config.ini")

        if "SERVERCONFIG" in config_object:
            # Builds the URI for API requests using config values
            server = config_object["SERVERCONFIG"]
            self.url = 'http://' + server["HOST"] + ':' + server["PORT"] + '/api/neighboring-vehicles/'

    def get_neighboring_vehicles(self, vehicle_id):
        """
        Retrieves neighboring vehicles from the API given a vehicle ID.

        Args:
            vehicle_id (str): ID of the vehicle.

        Returns:
            Tuple: A tuple containing status_code and neighboring vehicle IDs, or (status_code, None).
        """
        specific_url = f"{self.url}{vehicle_id}/"
        response = requests.get(url=specific_url)
        if response.status_code == 200:
            neighboring_vehicles = response.json()
            return response.status_code, neighboring_vehicles.get("neighboring_vehicle_ids", [])
        else:
            return response.status_code, None
