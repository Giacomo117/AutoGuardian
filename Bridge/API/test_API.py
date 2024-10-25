from random import uniform

from API.api import VehicleAPI, AlertsAPI, NeighboringVehiclesAPI

"""
Run these tests only if the database is empty...
if other vehicles exist with a given ID, you won't be able to create them,
so it's expected that the test might fail.
"""


# Test to create random vehicles
def test_create_random_vehicles():
    api = VehicleAPI()
    passed = True
    for i in range(4, 7):
        data = {
            'id': i,
            'latitude': uniform(0, 90),
            'longitude': uniform(0, 90),
            'smoke': uniform(0, 500),
            'temperature': uniform(0, 200)
        }
        status_code, vehicle = api.create_vehicle(data=data)
        if status_code != 201:
            passed = False

    print('Test Passed' if passed else 'Test Failed')


# Test to delete a specific vehicle
def test_delete_specific_vehicle(vehicle_id):
    api = VehicleAPI()
    passed = api.delete_vehicle_by_id(vehicle_id=vehicle_id) == 204
    print('Test Passed' if passed else 'Test Failed')


# Test to delete all entries
def test_delete_all_entry():
    api = VehicleAPI()
    passed = True
    for i in range(4, 7):
        if api.delete_vehicle_by_id(vehicle_id=i) != 204:
            passed = False

    print('Test Passed' if passed else 'Test Failed')


# Test to update a vehicle
def test_update_vehicle(vehicle_id):
    api = VehicleAPI()
    passed = api.update_vehicle(vehicle_id=vehicle_id, data={
        'id': vehicle_id,
        'latitude': uniform(0, 90),
        'longitude': uniform(0, 90),
        'smoke': uniform(0, 500),
        'temperature': uniform(0, 200)
    })[0] == 200
    print('Test Passed' if passed else 'Test Failed')


# Test to get all vehicles
def test_get_all_vehicles():
    api = VehicleAPI()
    passed = api.get_all_vehicles()[0] is not None
    print('Test Passed' if passed else 'Test Failed')


# Test to get a vehicle by ID
def test_get_vehicle_by_id(vehicle_id):
    api = VehicleAPI()
    passed = api.get_vehicle_by_id(vehicle_id=vehicle_id)[0] is not None
    print('Test Passed' if passed else 'Test Failed')


def test_create_alert():
    api = AlertsAPI()
    data = {
        'sender': 1,
        'latitude': 10,
        'longitude': 10,
        'smoke': 0,
        'temperature': 0
    }
    status_code = api.create_alert(data=data)
    if status_code != 201:
        print("Test failed")
    else:
        print("Test passed")


def main():
    test_create_random_vehicles()
    test_create_alert()
    test_get_all_vehicles()
    test_get_vehicle_by_id(2)
    test_update_vehicle(1)
    test_delete_all_entry()


if __name__ == "__main__":
    # main()
    api = NeighboringVehiclesAPI()
    statut_code, n = api.get_neighboring_vehicles("2")
    print(type(n))
