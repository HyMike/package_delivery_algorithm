#Store package data
class Packages:
    def __init__(self, ID, street, city, state, zip,deadline,weight, status,departure_time,delivery_time):
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
        return "ID: %s, %-20s, %s, %s,%s, Deadline: %s,%s,%s,Departure Time: %s,Delivery Time: %s" % (self.ID, self.street, self.city, self.state, self.zip, self.deadline, self.weight, self.status, self.departureTime, self.deliveryTime)
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
