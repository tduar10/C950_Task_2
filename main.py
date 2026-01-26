# Tristan Duarte Student ID: 011490410

import csv
import datetime
import Classes as cls

# Read the CSV files
with open("Distances.csv") as csvfile:
    csv_distance = csv.reader(csvfile)
    csv_distance = list(csv_distance)

with open("Dest_Names.csv") as csvfile:
    csv_address = csv.reader(csvfile)
    csv_address = list(csv_address)
    # Remove header so the list index matches the distance matrix rows
    csv_address.pop(0)

with open("WGUPS Package File.csv") as csvfile:
    csv_package = csv.reader(csvfile)
    csv_package = list(csv_package)

# Create the hash table instance
package_hash_table = cls.HashTable()

# Load packages into the hash table
def load_package_data(filename):
    with open(filename) as package_info:
        package_data = csv.reader(package_info)
        next(package_data)  # Skip header
        for package in package_data:
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pZip = package[4]
            pDeadline = package[5]
            pWeight = package[6]
            pStatus = "At Hub"

            # Insert data into hash table
            package_hash_table.insert(pID, pAddress, pDeadline, pCity, pZip, pWeight, pStatus)

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

    # Cycle through the list until all packages are delivered
    while len(upcoming_delivery) > 0:
        next_address = 2000
        next_package = None

        # Find the package with the minimum distance from the current location
        for package in upcoming_delivery:
            # Logic to handle the wrong address for package 9
            # Only update if the current time is past 10:20 AM
            if package.package_id == 9:
                if truck.time >= datetime.timedelta(hours=10, minutes=20):
                    package.address = "410 S State St"
                    package.zip_code = "84111"
            
            # Calculate distance
            dist = distance_between(extract_address(truck.address), extract_address(package.address))
            
            if dist <= next_address:
                next_address = dist
                next_package = package

        # Add closest package to the truck's delivered list
        truck.packages.append(next_package.package_id)
        upcoming_delivery.remove(next_package)
        
        # Update truck stats
        truck.mileage += next_address
        truck.address = next_package.address
        truck.time += datetime.timedelta(hours=next_address / 18)
        
        # Update package delivery time and departure time in the hash table
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.depart_time

# Initialize trucks
# Truck 1: Early deadlines
truck1 = cls.Truck(1, 18, None, [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East", datetime.timedelta(hours=8))

# Truck 2: Delayed packages (arrive at 9:05) and Can Only Be On Truck 2
truck2 = cls.Truck(2, 18, None, [3, 6, 18, 25, 28, 32, 36, 38], 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))

# Truck 3: Remaining packages and Wrong Address (Package 9)
# Leaves at 10:20 when address is corrected and driver 1 is back
truck3 = cls.Truck(3, 18, None, [2, 4, 5, 7, 8, 9, 10, 11, 12, 17, 19, 21, 22, 23, 24, 26, 27, 33, 35, 39], 0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))

# Run the delivery simulation
delivering_packages(truck1)
delivering_packages(truck2)
# Ensure Truck 3 doesn't leave until Truck 1 is finished (simulating driver availability)
truck3.depart_time = max(truck3.depart_time, truck1.time)
delivering_packages(truck3)

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

            print(f"\nStatus of all packages at {convert_user_time}:")
            print(f"{'ID':<4} {'Address':<40} {'City':<20} {'Zip':<10} {'Weight':<10} {'Deadline':<10} {'Status':<15} {'Time'}")
            print("-" * 120)

            # Iterate through all 40 packages
            for packageID in range(1, 41):
                package = package_hash_table.search(packageID)
                
                status_at_time = "At Hub"
                timestamp = ""
                
                # Determine status based on user time vs delivery/departure time
                if convert_user_time < package.departure_time:
                    status_at_time = "At Hub"
                    timestamp = f"Departs at {package.departure_time}"
                elif package.departure_time <= convert_user_time < package.delivery_time:
                    status_at_time = "En Route"
                    timestamp = f"Departs at {package.departure_time}"
                else:
                    status_at_time = "Delivered"
                    timestamp = f"{package.delivery_time}"

                print(f"{package.package_id:<4} {package.address:<40} {package.city:<20} {package.zip_code:<10} {package.weight:<10} {package.deadline:<10} {status_at_time:<15} {timestamp}")

    except ValueError:
        print("Invalid entry. Please try again.")
