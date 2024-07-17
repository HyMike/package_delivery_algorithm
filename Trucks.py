import datetime

class Trucks:
    def __init__(self, speed, miles, currentLocation, departTime, packages):
        self.speed = speed
        self.miles = miles
        self.currentLocation = currentLocation
        self.time = departTime
        self.departTime = departTime
        self.packages = packages

    def __str__(self):
        return "%s,%s,%s,%s,%s,%s" % (self.speed, self.miles, self.currentLocation, self.time, self.departTime, self.packages)

def addresss(address, AddressCSV):
    for row in AddressCSV:
        if address in row[2]:
            return int(row[0])

def Betweenst(addy1, addy2, DistanceCSV):
    distance = DistanceCSV[addy1][addy2]
    if distance == '':
        distance = DistanceCSV[addy2][addy1]
    return float(distance)

def truckDeliverPackages(truck, packageHash, AddressCSV, DistanceCSV):
    enroute = []
    for packageID in truck.packages:
        package = packageHash.search(packageID)
        enroute.append(package)

    truck.packages.clear()

    while len(enroute) > 0:
        nextAddy = 2000
        nextPackage = None
        for package in enroute:
            if package.ID in [25, 6]:
                nextPackage = package
                nextAddy = Betweenst(addresss(truck.currentLocation, AddressCSV), addresss(package.street, AddressCSV), DistanceCSV)
                break
            if Betweenst(addresss(truck.currentLocation, AddressCSV), addresss(package.street, AddressCSV), DistanceCSV) <= nextAddy:
                nextAddy = Betweenst(addresss(truck.currentLocation, AddressCSV), addresss(package.street, AddressCSV), DistanceCSV)
                nextPackage = package
        truck.packages.append(nextPackage.ID)
        enroute.remove(nextPackage)
        truck.miles += nextAddy
        truck.currentLocation = nextPackage.street
        truck.time += datetime.timedelta(hours=nextAddy / 18)
        nextPackage.deliveryTime = truck.time
        nextPackage.departureTime = truck.departTime