from datetime import datetime, timedelta

class Package:
   def __init__(self, package_id, address, deadline, city, zip_code, weight, status="At depot", delivery_time=None, notes=None):
        self.package_id = package_id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip_code = zip_code
        self.weight = weight
        self.status = status
        self.delivery_time = delivery_time
   def __str__(self):
           return (f"Package {self.package_id}: {self.address}, {self.city}, {self.zip_code}, "
                   f"Deadline: {self.deadline}, Weight: {self.weight}kg, Status: {self.status}, "
                   f"Delivered at: {self.delivery_time}")


class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for i in range(size)]

    def _hash(self, key):
        return hash(key)

    def insert(self, package_id, address, deadline, city, zip_code, weight, status="At depot", delivery_time=None, notes=None):
        # Check if package_id is already in the table
        if self.get(package_id):
            print(f"Package ID {package_id} already exists. Updating the package.")
            self.remove(package_id)
        # Create a new package object
        # and insert it into the hash table
        # Hash the package_id to find the index 
        idx = self._hash(package_id)
        package = Package(package_id, address, deadline, city, zip_code, weight, status, delivery_time)

        # Update if package with same ID already exists
        for i, (k, v) in enumerate(self.table[idx]):
            if key == package_id:
                self.table[idx][i] = (package_id, package)
                return

        # Otherwise, append the new package
        self.table[idx].append((package_id, package))

    def get(self, package_id):
        idx = self._hash(package_id)
        for key, package in self.table[idx]:
            if key == package_id:
                return package
        return None

    def update_status(self, package_id, status, delivery_time=None):
        package = self.get(package_id)
        if package:
            package.status = status
            package.delivery_time = delivery_time

    def remove(self, package_id):
        idx = self._hash(package_id)
        self.table[idx] = [(k, v) for k, v in self.table[idx] if k != package_id]

    def display(self):
        for bucket in self.table:
            for key, package in bucket:
                print(package)
   

class Truck:
    def __init__(self, truck_id, start_time=datetime.strptime("08:00", "%H:%M")):
        self.truck_id = truck_id
        self.packages = []  # Holds Package objects
        self.current_location = "Hub"
        self.miles_traveled = 0.0
        self.speed = 18  # mph
        self.time = start_time
        self.start_time = start_time
        self.return_to_depot = False

    def load_package(self, package):
        if len(self.packages) < 16:
            self.packages.append(package)
            package.status = "En route"
            return True
        else:
            print(f"Truck {self.truck_id} is full!")
            return False

    def deliver_package(self, package, distance):
        travel_time = timedelta(hours = distance / self.speed)
        self.time += travel_time
        self.miles_traveled += distance
        self.current_location = package.address
        package.status = f"Delivered at {self.time.strftime('%H:%M')}"
        package.delivery_time = self.time
        self.packages.remove(package)

    def return_to_depot(self):
        # Simulate returning to hub (you'll calculate the distance externally)
        self.current_location = "Depot"
        self.return_to_depot = True

    def __str__(self):
        return (f"Truck {self.truck_id} | Packages: {len(self.packages)} | "
                f"Current Location: {self.current_location} | "
                f"Miles Traveled: {self.miles_traveled:.2f} | "
                f"Time: {self.time.strftime('%H:%M')}")


