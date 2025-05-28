# Tristan Duarte Student ID: 011490410
 
import pandas as pd
import Classes as cls

# Load distance data using pandas
distance_df = pd.read_csv('distances.csv', header=None)
name_df = pd.read_csv('dest_names.csv')

# Fill the upper triangle so that i, j == j, i
rows, cols = distance_df.shape
for i in range(rows):
    for j in range(cols):
        if pd.isna(distance_df.iloc[i, j]):
            if j < rows and i < cols:
                distance_df.iloc[i, j] = distance_df.iloc[j, i]

addresses = name_df['Addr'].tolist()                            # Store addresses
distance_matrix = distance_df.astype(float).values.tolist()     # Convert DataFrame to 2D list
package_df = pd.read_csv('WGUPS Package File.csv')              # Load package data
packages = cls.HashTable(len(package_df))  

print (addresses)
print(distance_matrix)                     # Initialize hashtable

# Load packages into hashtable
for index, row in package_df.iterrows():
    packages.insert(row['PackageID'], row['Address'], row['City'],
                    row['Zip'], row['DeliveryDeadline'], row['Weight'],
                    notes=row['SpecialNotes']
    )

packages.display()  # Display all packages in the hashtable

# Innitialize trucks
truck1 = cls.Truck(1)
truck2 = cls.Truck(2)
truck3 = cls.Truck(3)

# Manually load packages into trucks based on special requirements and delivery deadlines
truck1.load_package(packages.get(1))  
truck1.load_package(packages.get(2))  
truck1.load_package(packages.get(3))  
truck1.load_package(packages.get(4))  
truck1.load_package(packages.get(5))
truck1.load_package(packages.get(6))
truck1.load_package(packages.get(13))
truck1.load_package(packages.get(14)) 
truck1.load_package(packages.get(15))
truck1.load_package(packages.get(16)) 
truck1.load_package(packages.get(19)) 
truck1.load_package(packages.get(20)) 
truck1.load_package(packages.get(29)) 
truck1.load_package(packages.get(30)) 
truck1.load_package(packages.get(31)) 
truck1.load_package(packages.get(34)) 
truck1.load_package(packages.get(37))
truck1.load_package(packages.get(40))
truck1.load_package(packages.get(21)) 
truck1.load_package(packages.get(22)) 
truck1.load_package(packages.get(24)) 

truck2.load_package(packages.get(3)) 
truck2.load_package(packages.get(18))  
truck2.load_package(packages.get(36)) 
truck2.load_package(packages.get(38)) 
truck2.load_package(packages.get(5)) 
truck2.load_package(packages.get(8)) 
truck2.load_package(packages.get(11)) 
truck2.load_package(packages.get(12)) 
truck2.load_package(packages.get(17)) 
truck2.load_package(packages.get(23)) 
truck2.load_package(packages.get(27)) 
truck2.load_package(packages.get(35)) 
truck2.load_package(packages.get(2)) 
truck2.load_package(packages.get(4)) 
truck2.load_package(packages.get(7)) 
truck2.load_package(packages.get(10)) 

truck3.load_package(packages.get(6)) 
truck3.load_package(packages.get(25)) 
truck3.load_package(packages.get(28)) 
truck3.load_package(packages.get(32)) 
truck3.load_package(packages.get(9)) 
truck3.load_package(packages.get(26)) 
truck3.load_package(packages.get(33)) 
truck3.load_package(packages.get(39)) 

def deliver_packages(truck):
    """Deliver packages for a given truck."""
    while truck.packages:
        closest_package = (None, float('inf'))  # Get the first package
        for package in truck.packages:
            package.status = "En route"
            distance = distance_matrix[addresses[package.address]][addresses[truck.current_location]]
            if distance > closest_package[1]:
                closest_package = (package, distance)
        truck.deliver_package(closest_package[0], closest_package[1])
    return


current_time = cls.datetime.strptime("08:00", "%H:%M")  # Start time for all trucks
available_drivers = 2  # Number of available drivers
# Deliver packages using the trucks until all packages are delivered
while truck1.packages or truck2.packages or truck3.packages:
    if truck1.packages:
        if not truck1.occupied and available_drivers > 0:
            truck1.occupied = True
            available_drivers -= 1
        if truck1.occupied:
            deliver_packages(truck1)
    elif truck1.occupied:
        truck1.occupied = False
        available_drivers += 1

    if truck2.packages:
        if not truck2.occupied and available_drivers > 0:
            truck2.occupied = True
            available_drivers -= 1
        if truck2.occupied:
            deliver_packages(truck2)
    elif truck2.occupied:
        truck2.occupied = False
        available_drivers += 1

    if truck3.packages:
        if not truck3.occupied and available_drivers > 0:
            truck3.occupied = True
            available_drivers -= 1
        if truck3.occupied:
            deliver_packages(truck3)
    elif truck3.occupied:
        truck3.occupied = False
        available_drivers += 1
    
# ...existing code...