# REST API

Implementation of a small REST API providing CRUD (Create, Read, Update, Delete) functionalities to manage vehicle data in the system.

## Endpoints and Supported Operations

### `/api/vehicles/`

- **GET**: Retrieves the complete list of vehicles.
- **POST**: Creates a new vehicle.

### `/api/vehicles/<vehicle_id>/`

- **GET**: Retrieves details of a specific vehicle.
- **PUT**: Updates an existing vehicle: json_fields = ['id', 'latitude', 'longitude', 'smoke', 'temperature'].
- **DELETE**: Deletes an existing vehicle.

### `/api/alerts/`

- **POST**: Creates a new alert: json_fields = ['sende_id', 'latitude', 'longitude', 'smoke', 'temperature']

### `/api/contacts/<vehicle_id>`

**GET**: Retrieves contacts associated with the vehicle owner.

## Usage

Usage examples with `curl` on Linux-like systems:

```bash
# Get all vehicles
curl -X GET http://<IP_ADDRESS>:<PORT>/api/vehicles/

# Get a specific vehicle
curl -X GET http://<IP_ADDRESS>:<PORT>/api/vehicles/<vehicle_id>/

# Create a new vehicle
curl -X POST -H "Content-Type: application/json" -d '{"id": <vehicle_id>, "latitude": <latitude>, "longitude": <longitude>, "smoke": <smoke> , "temperature": <temperature>}' http://<IP_ADDRESS>:<PORT>/api/vehicles/

# Update an existing vehicle, assign the new position to vehicle <vehicle_id>
curl -X PUT -H "Content-Type: application/json" -d '{"id": <vehicle_id>, "latitude": <latitude>, "longitude": <longitude>, "smoke": <smoke> , "temperature": <temperature>}' http://<IP_ADDRESS>:<PORT>/api/vehicles/<vehicle_id>/

# Delete a vehicle
curl -X DELETE http://<IP_ADDRESS>:<PORT>/api/vehicles/<vehicle_id>/

# Create a new alert
curl -X POST -H "Content-Type: application/json" -d '{"sender": 2, "latitude":10, "longitude": 10, "smoke": 0 , "temperature": 0}' http://192.168.188.70:8080/api/alerts/
