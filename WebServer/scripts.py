from REST.models import Vehicle, Alert, User


def create_users_and_vehicles():
    """
    Function to create users and associate vehicles with them.

    Creates three users and associates a vehicle with each user.

    Returns:
        None
    """
    # Creation of users
    users = []
    for i in range(1, 4):
        username = f"admin{i}"
        password = username
        user = User.objects.create_user(username=username, password=password)
        users.append(user)
        print(f"User '{username}' created with password '{password}'")

    # Associating a vehicle with each user
    for i, user in enumerate(users):
        vehicle = Vehicle.objects.create(id=i + 1, latitude=0, longitude=0, smoke=0, temperature=0)
        user.vehicles.add(vehicle)
        print(f"Vehicle {i + 1} associated with user '{user.username}'")
    vehicle = Vehicle.objects.get(pk=1)
    vehicle.latitude = 10
    vehicle.longitude = 10
    vehicle.save()
    vehicle = Vehicle.objects.get(pk=2)
    vehicle.latitude = 10
    vehicle.longitude = 10
    vehicle.save()


def create_alerts():
    """
    Function to create alerts for vehicles.

    Creates alerts for vehicles to simulate a situation.

    Returns:
        None
    """
    # Coordinates of Modena
    modena_latitude = 44.647128
    modena_longitude = 10.925226

    # Creating alerts to simulate the situation
    for vehicle in Vehicle.objects.all():
        # Creating 3 alerts for each vehicle
        for i in range(1, 4):
            # If the index i is even, position the alert within a 5 km radius, otherwise not
            if i % 2 == 0:
                # Coordinates for alerts within the 5 km radius
                alert_latitude = modena_latitude + 0.01 * i
                alert_longitude = modena_longitude - 0.01 * i
            else:
                # Coordinates for alerts outside the 5 km radius
                alert_latitude = modena_latitude + 0.1 * i
                alert_longitude = modena_longitude - 0.1 * i

            alert = Alert.objects.create(sender=vehicle, latitude=alert_latitude, longitude=alert_longitude,
                                         smoke=vehicle.smoke, temperature=vehicle.temperature)
            # Associating alerts with all other vehicles (except the sender)
            for receiver_vehicle in Vehicle.objects.exclude(pk=vehicle.pk):
                alert.receivers.add(receiver_vehicle)
            print(f"Alert created for vehicle {vehicle.id}")


def script():
    """
    Function to execute the script.

    Deletes all existing users, vehicles, and alerts, then creates new users, vehicles, and alerts.

    Returns:
        None
    """
    User.objects.all().delete()
    Vehicle.objects.all().delete()
    Alert.objects.all().delete()
    create_users_and_vehicles()
    # create_alerts()  # Uncomment this line if you want to create alerts
