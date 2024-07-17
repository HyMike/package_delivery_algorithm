import datetime

#Create a Truck Object that allows to track it's location, time and packages.
class Trucks:
    def __init__(self, speed, miles, current_location, departure_time, packages):
        self.speed = speed
        self.miles = miles
        self.currentLocation = current_location
        self.time = departure_time
        self.departure_time = departure_time
        self.packages = packages

    def __str__(self):
        return "%s,%s,%s,%s,%s,%s" % (self.speed, self.miles, self.current_location, self.time, self.departure_time, self.packages)
