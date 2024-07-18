#Store package data
import csv
import datetime
class Packages:
    def __init__(self, ID, street, city, state, zip,deadline,weight,status,departure_time,delivery_time):
        self.ID = ID
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None
    def __str__(self):
        return "ID: %s, %s, %s, %s,%s, Deadline: %s,Weight: %skg,Status: %s,Departure Time: %s,Delivery Time: %s" % (self.ID, self.street, self.city, self.state, self.zip, self.deadline, self.weight, self.status, self.departure_time, self.delivery_time)
    #status_update method will update the delivery status. At hub, delivered.
    #Time is needed to compare with depart time and delivery time to give status. Given By User
    def status_update(self, time):
        if self.delivery_time == None:
            self.status = "At the hub"
        elif time < self.departure_time:
            self.status = "At the hub"
        elif time < self.delivery_time:
            self.status = "En route"
        else:
            self.status = "Delivered"
    # WGUPS does not know the correct address for ID= 9 (410 S. State St., Salt Lake City, UT 84111) until 10:20 a.m
        if self.ID == 9:
            if time > datetime.timedelta (hours=10, minutes= 20):
                self.street = "410 S State St"
                self.zip = "84111"
            else:
                self.street = "300 State St"
                self.zip = "84103"

#Using package.CSV file to create a package object that contains all the delivery information, so we can use it.
def loading_package_data(file, package_hash_table):
    with open(file) as packages:
        package_info = csv.reader(packages, delimiter=',')
        next(package_info)
        for package in package_info:
            package_ID = int(package[0])
            package_street = package[1]
            package_city = package[2]
            package_state = package[3]
            package_zip = package[4]
            package_deadline = package[5]
            package_weight = package[6]
            package_status = "At the Hub"
            package_departure_time = None
            package_delivery_time = None

            package_data = Packages(package_ID, package_street, package_city, package_state, package_zip, package_deadline, package_weight, package_status, package_departure_time, package_delivery_time)
            package_hash_table.insert(package_ID, package_data)
