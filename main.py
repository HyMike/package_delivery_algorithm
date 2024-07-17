# Michael Hy
# Student ID: 010920685

import csv
import datetime
from chain_hash_table import CreateHashMap
from package import Packages, loading_package_data



# Load the distance table CSV file and package CSV file
def load_csv_files():
    with open("CSV/Delivery_Address.csv") as delivery_addresses:
        address_CSV = csv.reader(delivery_addresses)
        address_list = list(address_CSV)
    with open("CSV/Package_Distance.csv") as package_distance:
        distance_CSV = csv.reader(package_distance)
        distance_list = list(distance_CSV)
    return address_list, distance_list

# Address and Distance CSV files loaded into memory
address_list, distance_list = load_csv_files()


# Initialize the hash table
packages_table = CreateHashMap()

#Takes the address list and find the minimum distance for the next address.
def get_nearest_address(address):
    for row in address_list:
        if address in row[2]:
            return int(row[0])

def address_distances(address, address2, distance_list):
    address_distance = distance_list[address][address2]
    if address_distance == '':
        address_distance = distance_list[address2][address]
    return float(address_distance)


# Load package data into the hash table
loading_package_data('CSV/WGUPS_Package.csv', packages_table)


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




# Manually load trucks and assign departure times
# truck1 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=8), [1, 13, 14, 15, 16, 19, 20, 27, 29, 30, 31, 34, 37, 40])
# truck2 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=11), [2, 3, 4, 5, 9, 18, 26, 28, 32, 35, 36, 38])
# truck3 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5), [6, 7, 8, 10, 11, 12, 17, 21, 22, 23, 24, 25, 33, 39])
#
# # Deliver packages for each truck
# truckDeliverPackages(truck1, packageHash, address_list, distance_list)
# truckDeliverPackages(truck3, packageHash, address_list, distance_list)
# # Ensure truck 2 doesn't leave until either truck 1 or 3 has returned
# truck2.departTime = min(truck1.time, truck3.time)
# truckDeliverPackages(truck2, packageHash, address_list, distance_list)
#
# # Title
# print("Western Governors University Parcel Service")
# # Total miles for all of the trucks
# print("The overall miles are:", (truck1.miles + truck2.miles + truck3.miles))
#
# # Loop to get user input for package status at a given time
# while True:
#     userTime = input("Please enter a time for which you'd like to see the status of each package. Format: HH:MM. ")
#     (h, m) = userTime.split(":")
#     timeChange = datetime.timedelta(hours=int(h), minutes=int(m))
#     try:
#         singleEntry = [int(input("Enter the Package ID or nothing at all."))]
#     except ValueError:
#         singleEntry = range(1, 41)
#     for packageID in singleEntry:
#         package = packageHash.search(packageID)
#         package.statusUpdate(timeChange)
#         print(str(package))