# Michael Hy
# Student ID: 010920685

import csv
import datetime
from chain_hash_table import CreateHashMap
from package import Packages, loading_package_data
from trucks import Trucks


#Convert the delivery address distance CSV file and package CSV file to list that can be manipulated.
def convert_csv_files():
    with open("CSV/Delivery_Address.csv") as delivery_addresses:
        address_CSV = csv.reader(delivery_addresses)
        address_list = list(address_CSV)
    with open("CSV/Package_Distance.csv") as package_distance:
        distance_CSV = csv.reader(package_distance)
        distance_list = list(distance_CSV)
    return address_list, distance_list

address_list, distance_list = convert_csv_files()

# Initialize a chain hash map
packages_table = CreateHashMap()

#Takes the address list and find the minimum distance for the next address.
def get_nearest_address(address,address_list):
    for row in address_list:
        if address in row[2]:
            return int(row[0])

def address_distances(address, address2, distance_list):
    address_distance = distance_list[address][address2]
    if address_distance == '':
        address_distance = distance_list[address2][address]
    return float(address_distance)


# Map package info onto the chain hash map.
loading_package_data("CSV/WGUPS_Package.csv", packages_table)


#Loading package to the trucks and assign departure times
truck1 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=8), [1, 13, 14, 15, 16, 19, 20, 27, 29, 30, 31, 34, 37, 40])
truck2 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5), [2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 18, 21, 22, 23, 24, 25, 26, 28, 32, 33, 36, 38, 39])
truck3 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=11), [6, 17, 35])


def deliver_package(truck, packages_table, address_list, distance_list):
    #list for package that marked for delivered..
    enroute = []
    for package_ID in truck.packages:
        package = packages_table.search(package_ID)
        enroute.append(package)


    truck.packages.clear()

    while len(enroute) > 0:
        #intializing variables
        next_address = 1500
        next_package = None

        for package in enroute:
            #Handle case where it need to be the next package to be delivered.
            if package.ID in [25, 6]:
                next_package = package
                next_address = address_distances(get_nearest_address(truck.current_location, address_list), get_nearest_address(package.street, address_list), distance_list)
                break
            #Otherwise, the algorithm selects the package with the shortest distance from the truck’s current location.
            if address_distances(get_nearest_address(truck.current_location, address_list), get_nearest_address(package.street, address_list), distance_list) <= next_address:

                next_address = address_distances(get_nearest_address(truck.current_location, address_list), get_nearest_address(package.street, address_list), distance_list)
                next_package = package

        # Mark package as delivered by this truck
        truck.deliver_package(next_package.ID)
        enroute.remove(next_package)
        truck.miles += next_address
        truck.current_location = next_package.street
        truck.time += datetime.timedelta(hours=next_address / 18)
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.departure_time



deliver_package(truck1, packages_table, address_list, distance_list)
deliver_package(truck2, packages_table, address_list, distance_list)

# Ensure truck 3 doesn't leave until either truck 1 or 2 has returned
truck3.departure_time = min(truck1.time, truck2.time)
deliver_package(truck3, packages_table, address_list, distance_list)

def get_user_input_time(prompt):
    while True:
        user_time = input(prompt)
        try:
            time_object = datetime.datetime.strptime(user_time, '%I:%M %p')
            return datetime.timedelta(hours=time_object.hour, minutes=time_object.minute)
        except ValueError:
            print("Invalid time format. Please use HH:MM AM/PM format.")


def get_time_interval_from_user():
    start_time = get_user_input_time("Please enter the start of the interval (HH:MM AM/PM): ")
    if start_time is None:
        return None, None
    end_time = get_user_input_time("Please enter the end of the interval (HH:MM AM/PM): ")
    if end_time is None:
        return None, None
    if start_time >= end_time:
        print("Start time must be earlier than end time. Please try again.")
        return None, None
    return start_time, end_time


def specific_time_check():
    user_input_time = get_user_input_time("Please enter a time that you would like to check the status of the packages and the trucks? (HH:MM AM/PM): ")
    return user_input_time


# Function to display package information with delivery details specific time or time frame.
def display_package_info(packages_table, trucks, check_time):
    # Header
    header = [
        "ID".ljust(4),
        "Address".ljust(30),
        "City".ljust(20),
        "State".ljust(10),
        "Zip Code".ljust(10),
        "Deadline".ljust(15),
        "Weight".ljust(10),
        "Status".ljust(15),
        "Departed".ljust(15),
        "Delivered Time".ljust(20),
        "Truck #".ljust(10)
    ]
    print(" ".join(header))

    for package_id in range(1, 41):
        package = packages_table.search(package_id)
        # Ensure the status and address are updated
        package.status_update(check_time)

        delivered_time = None
        delivering_truck_number = None
        for index, truck in enumerate(trucks, start=1):
            if package_id in truck.get_delivered_packages():
                delivered_time = package.delivery_time
                delivering_truck_number = index
                break

        # Shorten the address to a maximum of 25 characters
        shortened_address = package.street[:25]

        # Formatting package information
        row = [
            str(package.ID).ljust(4),
            shortened_address.ljust(30),
            package.city.ljust(20),
            package.state.ljust(10),
            package.zip.ljust(10),
            package.deadline.ljust(15),
            f"{package.weight} kg".ljust(10),
            package.status.ljust(15),
            str(package.departure_time).ljust(15),
            str(delivered_time).ljust(20),
            str(delivering_truck_number).ljust(10)
        ]
        print(" ".join(row))


#Main Interface of Program
print("Welcome to WGUPS Routing!")

while True:
    print("Total miles for all trucks:", truck1.miles + truck2.miles + truck3.miles)

    # Prompt user about what they want to do
    option = input(
        "Would you like to check the status of packages and trucks for a specific time or a specific interval?\nEnter 'time' for specific time or 'interval' for specific interval: ").lower()
    if option == "time":
        specific_time = specific_time_check()
        display_package_info(packages_table, [truck1, truck2, truck3], specific_time)
    elif option == "interval":
        start_time, end_time = get_time_interval_from_user()
        display_package_info(packages_table, [truck1, truck2, truck3], end_time)
    else:
        print("Invalid option. Please enter 'time' or 'interval'.")

    another_check = input("Do you want to check another time or interval? (yes/no): ")
    if another_check.lower() != "yes":
        break
