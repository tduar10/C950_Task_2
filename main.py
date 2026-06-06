# Tristan Duarte Student ID: 011490410

import csv
import datetime
import Classes as cls

# Time package 9's correct address becomes known, and the truck capacity limit
PKG9_CORRECTION_TIME = datetime.timedelta(hours=10, minutes=20)
TRUCK_CAPACITY = 16

# Read the CSV files
with open("Distances.csv") as csvfile:
    csv_distance = csv.reader(csvfile)
    csv_distance = list(csv_distance)

with open("Dest Names.csv") as csvfile:
    csv_address = csv.reader(csvfile)
    csv_address = list(csv_address)
    # Remove header so the list index matches the distance matrix rows
    csv_address.pop(0)

# Create the hash table instance
package_hash_table = cls.HashTable()

# Load packages into the hash table
def load_package_data(filename):
    with open(filename) as package_info:
        package_data = csv.reader(package_info)
        next(package_data)  # Skip header
        for package in package_data:

            # Skip empty rows
            if len(package) < 7:
                continue

            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pZip = package[4]
            pDeadline = package[5]
            pWeight = package[6]
            pStatus = "At Hub"

            # Insert data into hash table
            package_hash_table.insert(pID, pAddress, pDeadline, pCity, pZip, pWeight, pStatus)

    # Register package 9's known-future address correction (applied at 10:20)
    pkg9 = package_hash_table.search(9)
    if pkg9 is not None:
        pkg9.set_address_correction("410 S State St", "84111", PKG9_CORRECTION_TIME)

# Load the data
load_package_data("WGUPS Package File.csv")

# Find the distance between two addresses
def distance_between(x_value, y_value):
    distance = csv_distance[x_value][y_value]
    if distance == '':
        distance = csv_distance[y_value][x_value]
    return float(distance)

# Get the address index from the string address
def extract_address(address):
    for index, row in enumerate(csv_address):
        if address in row[1]:
            return index
    # Some addresses in the package file spell out "South"/"North" but the
    # distance table uses the short form "S"/"N", so try again with those replaced
    short_addr = address.replace("South", "S").replace("North", "N")
    for index, row in enumerate(csv_address):
        if short_addr in row[1]:
            return index
    return -1

# Main algorithm to deliver packages
# This uses a Nearest Neighbor algorithm to determine the most efficient route
def delivering_packages(truck):
    # Create a list of all packages currently on the truck
    upcoming_delivery = []
    for packageID in truck.packages:
        package = package_hash_table.search(packageID)
        upcoming_delivery.append(package)

    # Clear the truck list so we can re-add them in delivered order
    truck.packages.clear()

    # Set departure time when the truck leaves the hub
    for package in upcoming_delivery:
        package.departure_time = truck.depart_time

    # Cycle through the list until all packages are delivered
    while len(upcoming_delivery) > 0:
        next_address = float('inf')
        next_package = None

        # Find the package with the minimum distance from the current location
        for package in upcoming_delivery:
            # Use the address accurate as of the truck's current time
            # (handles package 9's wrong address before 10:20)
            current_addr = package.address_for_time(truck.time)
            dist = distance_between(extract_address(truck.address), extract_address(current_addr))

            if dist < next_address:
                next_address = dist
                next_package = package

        # Add closest package to the truck's delivered list
        chosen_addr = next_package.address_for_time(truck.time)
        truck.packages.append(next_package.package_id)
        upcoming_delivery.remove(next_package)

        # Update truck stats
        truck.mileage += next_address
        truck.address = chosen_addr
        truck.time += datetime.timedelta(hours=next_address / truck.speed)

        # Update package delivery time in the hash table
        next_package.delivery_time = truck.time

# Initialize trucks
# Truck 1: early deadlines and the linked group (15 has a 9:00 deadline)
truck1 = cls.Truck(1, 18, TRUCK_CAPACITY, [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40, 21, 39, 11], 0.0, "4001 South 700 East", datetime.timedelta(hours=8))

# Truck 2: truck-2-only packages and delayed packages (arrive at 9:05)
truck2 = cls.Truck(2, 18, TRUCK_CAPACITY, [3, 6, 18, 25, 28, 32, 36, 38, 12, 17, 23, 24, 26, 2, 4, 33], 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))

# Truck 3: remaining packages and wrong address (package 9), leaves at 10:20
truck3 = cls.Truck(3, 18, TRUCK_CAPACITY, [5, 7, 8, 9, 10, 22, 27, 35], 0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))

# Enforce the 16-package capacity limit
for t in (truck1, truck2, truck3):
    if len(t.packages) > t.capacity:
        raise ValueError(f"Truck {t.truck_id} is over capacity ({len(t.packages)} > {t.capacity}).")

# Run the delivery simulation
delivering_packages(truck1)
delivering_packages(truck2)
# Ensure Truck 3 doesn't leave until Truck 1 is finished (simulating driver availability)
# Bump both depart_time and the internal clock so routing starts from the right time
truck3.depart_time = max(truck3.depart_time, truck1.time)
truck3.time = truck3.depart_time
delivering_packages(truck3)

# Format a timedelta as HH:MM for display
def format_td(td):
    total = int(td.total_seconds())
    h, rem = divmod(total, 3600)
    m, _ = divmod(rem, 60)
    return f"{h:02d}:{m:02d}"

# User Interface
print("WGUPS Routing Program")
print(f"Total Mileage for all trucks: {truck1.mileage + truck2.mileage + truck3.mileage:.1f} miles")

while True:
    try:
        user_input = input("Please type 'status' to view package status or 'exit' to quit: ")

        if user_input == 'exit':
            break

        if user_input == 'status':
            user_time_input = input("Please enter a time to check status (HH:MM): ")
            (h, m) = user_time_input.split(":")
            convert_user_time = datetime.timedelta(hours=int(h), minutes=int(m))

            print(f"\nStatus of all packages at {format_td(convert_user_time)}:")
            print(f"{'ID':<4} {'Address':<40} {'City':<20} {'Zip':<8} {'Weight':<8} {'Deadline':<10} {'Status':<12} {'Time'}")
            print("-" * 120)

            # Iterate through all 40 packages
            for packageID in range(1, 41):
                package = package_hash_table.search(packageID)

                # Show the address accurate as of the queried time
                display_addr = package.address_for_time(convert_user_time)
                display_zip = package.zip_for_time(convert_user_time)

                # Determine status based on user time vs departure/delivery time
                if package.departure_time is None or convert_user_time < package.departure_time:
                    status_at_time = "At Hub"
                    timestamp = f"Departs {format_td(package.departure_time)}" if package.departure_time is not None else ""
                elif convert_user_time < package.delivery_time:
                    status_at_time = "En Route"
                    timestamp = f"Departed {format_td(package.departure_time)}"
                else:
                    status_at_time = "Delivered"
                    timestamp = f"Delivered {format_td(package.delivery_time)}"

                print(f"{package.package_id:<4} {display_addr:<40} {package.city:<20} {display_zip:<8} {package.weight:<8} {package.deadline:<10} {status_at_time:<12} {timestamp}")
            print()

    except ValueError:
        print("Invalid entry. Please try again.")