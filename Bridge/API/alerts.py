class Alert:
    """A class to represent an alert."""

    def __init__(self):
        """Initializes an Alert object."""
        self.sender = None
        self.receivers = None
        self.latitude = None
        self.longitude = None
        self.smoke = None
        self.temperature = None
        self.date = None
        self.recent = None

    def serialize(self):
        """
        Serializes the Alert object into a string.

        Returns:
            str: A string representation of the Alert object.
        """
        return str({
            "sender": self.sender,
            "receivers": self.receivers,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "smoke": self.smoke,
            "temperature": self.temperature,
            "date": self.date,
            "recent": self.recent
        })

    def __str__(self):
        """
        Returns a string representation of the Alert object.

        Returns:
            str: A string representation of the Alert object.
        """
        return self.serialize()
