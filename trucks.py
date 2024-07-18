import datetime

# Create a Truck Object that allows tracking its location, time, and packages.
class Trucks:
    def __init__(self, speed, miles, current_location, departure_time, packages):
        self.speed = speed
        self.miles = miles
        self.current_location = current_location
        self.time = departure_time
        self.departure_time = departure_time
        self.packages = packages
        self.delivered_packages = []  # List to store delivered packages

    def deliver_package(self, package_id):
        """ Method to mark a package as delivered by this truck. """
        self.delivered_packages.append(package_id)


    def get_delivered_packages(self):
        """ Method to retrieve the list of packages delivered by this truck. """
        return self.delivered_packages

    def __str__(self):
        return f"Truck speed: {self.speed}, Miles driven: {self.miles}, Current location: {self.current_location}, Time: {self.time}, Departure time: {self.departure_time}, Packages: {self.packages}, Delivered packages: {self.delivered_packages}"