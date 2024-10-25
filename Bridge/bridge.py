# bridge.py

import configparser
import json

import serial
import serial.tools.list_ports

from API.api import VehicleAPI, AlertsAPI, NeighboringVehiclesAPI
from MQTT_client.client import MQTTClient


class Bridge:
    def __init__(self):
        self.ID = 1
        self.client = None
        self.portname = None
        self.inbuffer = []
        self.ser = None
        self.first = True
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.setup_serial()
        self.setup_mqtt()
        self.vehicle_api = VehicleAPI()
        self.alert_api = AlertsAPI()

    def setup_mqtt(self):
        """Sets up MQTT client."""
        self.client = MQTTClient(self)
        self.client.subscribe()

    def setup_serial(self):
        """Sets up serial connection."""
        self.ser = None
        self.portname = None
        if self.config.get("SERIAL", "PORTNAME", fallback="COM1"):
            self.portname = self.config.get("SERIAL", "PORTNAME", fallback="COM1")
        try:
            if self.portname:
                print("\nConnecting to " + self.portname + '\n')
                self.ser = serial.Serial(self.portname, 9600, timeout=0)
        except:
            self.ser = None
            print(f'\033[91mSetup failed: Unable to connect to {self.portname}. \nPlease check the port and update '
                  f'the "PORTNAME" in the config.ini file if necessary.\n\033[0m')
            self.print_available_ports()

    def loop(self):
        """Main loop for data processing."""
        if self.ser:
            while True:
                if self.ser and self.ser.in_waiting > 0:
                    lastchar = self.ser.read(1)
                    if lastchar == b'$':
                        self.inbuffer = []
                    elif lastchar == b'!':
                        data = b''.join(self.inbuffer)
                        self.use_data(data.decode())
                        self.inbuffer = []
                    else:
                        self.inbuffer.append(lastchar)
        else:
            print('\033[91mError on main loop: the serial connection has not been established.\033[0m\n')

    def check_alert(self, data):
        """Checks for alerts based on data."""
        data["sender"] = data.pop("id")
        # se risponde 200 ==> i vicini hanno stessi valori ==> no alert
        # se risponde 201 ==> l'alert creato
        if data["t"] == 1 or data["s"] == 1 or data["u"] == 1:
            if self.alert_api.create_alert(data) == 201:
                neighbors = self.get_neighbors()
                print("i miei vicini sono: " + str(neighbors))
                # allerto i vicini
                print("allerto i vicini")
                self.client.publish(payload=str(neighbors))

    def use_data(self, data):
        """Processes incoming data."""
        try:
            data = json.loads(data)
            # print(data)
            if self.first:
                self.vehicle_api.create_vehicle(self.solve_format_data(data))
                self.first = False
            self.vehicle_api.update_vehicle(data["id"], self.solve_format_data(data))
            self.check_alert(data)
        except json.JSONDecodeError as e:
            print("Error during JSON string parsing:", e)

    def handle_alert(self, payload):
        """
        Handles an alert message received from MQTT.
        """
        # il payload contiene la lista che è una stringa
        ids = eval(payload)
        if self.ID in ids:
            self.sendAlarm()

    def get_neighbors(self):
        # ritorna una lista di id dei vicini
        api = NeighboringVehiclesAPI()
        status_code, neighbors = api.get_neighboring_vehicles(str(self.ID))
        return neighbors

    def sendAlarm(self):
        # bisogna mandare all'arduino qualcosa per dirgli oh bello accenditi.
        self.ser.write(b'$')

    @staticmethod
    def print_available_ports():
        """Prints available serial ports."""
        print("List of available ports: ")
        ports = serial.tools.list_ports.comports()
        for port in ports:
            print('\t\t\t\t\t\t/---------------------------------------------/')
            print('\t\t\t\t\t\t- port name: ' + str(port.device))
            print('\t\t\t\t\t\t- port description: ' + str(port.description))
        print('\t\t\t\t\t\t/---------------------------------------------/\n')

    def solve_format_data(self, data):
        d = data.copy()
        s = d.pop("s")
        u = d.pop("u")
        t = d.pop("t")
        return d
