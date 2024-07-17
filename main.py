# Michael Hy
# Student ID: 010920685

import csv
import datetime

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

from hash_table import HashTableWChains
from packages import Packages, loadPackageData
from trucks import Trucks, truckDeliverPackages

# Initialize the hash table
packageHash = HashTableWChains()

# Load package data into the hash table
loadPackageData('CSVFiles/packageCSV.csv', packageHash)

# Manually load trucks and assign departure times
truck1 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=8), [1, 13, 14, 15, 16, 19, 20, 27, 29, 30, 31, 34, 37, 40])
truck2 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=11), [2, 3, 4, 5, 9, 18, 26, 28, 32, 35, 36, 38])
truck3 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5), [6, 7, 8, 10, 11, 12, 17, 21, 22, 23, 24, 25, 33, 39])

# Deliver packages for each truck
truckDeliverPackages(truck1, packageHash, address_list, distance_list)
truckDeliverPackages(truck3, packageHash, address_list, distance_list)
# Ensure truck 2 doesn't leave until either truck 1 or 3 has returned
truck2.departTime = min(truck1.time, truck3.time)
truckDeliverPackages(truck2, packageHash, address_list, distance_list)

# Title
print("Western Governors University Parcel Service")
# Total miles for all of the trucks
print("The overall miles are:", (truck1.miles + truck2.miles + truck3.miles))

# Loop to get user input for package status at a given time
while True:
    userTime = input("Please enter a time for which you'd like to see the status of each package. Format: HH:MM. ")
    (h, m) = userTime.split(":")
    timeChange = datetime.timedelta(hours=int(h), minutes=int(m))
    try:
        singleEntry = [int(input("Enter the Package ID or nothing at all."))]
    except ValueError:
        singleEntry = range(1, 41)
    for packageID in singleEntry:
        package = packageHash.search(packageID)
        package.statusUpdate(timeChange)
        print(str(package))