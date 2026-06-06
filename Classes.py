# Tristan Duarte Student ID: 011490410

import datetime

class HashTable:
    # Initialize the hash table with empty bucket list entries.
    def __init__(self, initial_capacity=40):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Insert a new item into the hash table.
    def insert(self, key, item, deadline, city, zip_code, weight, status):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # Update if the key is already in the bucket
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = Package(key, item, deadline, city, zip_code, weight, status)
                return True

        # If not found, append the new package to the bucket
        p = Package(key, item, deadline, city, zip_code, weight, status)
        bucket_list.append([key, p])
        return True

    # Search for an item with matching key in the hash table.
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # Search for the key in the bucket list
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1] # Returns the Package object
        return None

    # Remove an item with matching key from the hash table.
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])
                return


class Package:
    def __init__(self, package_id, address, deadline, city, zip_code, weight, status):
        self.package_id = package_id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip_code = zip_code
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None

        # Address correction support (used for package 9)
        self.corrected_address = None
        self.corrected_zip = None
        self.correction_time = None

    # Register a known-future address correction without changing the address yet
    def set_address_correction(self, new_address, new_zip, correction_time):
        self.corrected_address = new_address
        self.corrected_zip = new_zip
        self.correction_time = correction_time

    # Return the address that is accurate as of the given time
    def address_for_time(self, current_time):
        if (self.correction_time is not None
                and current_time >= self.correction_time
                and self.corrected_address is not None):
            return self.corrected_address
        return self.address

    # Return the zip that is accurate as of the given time
    def zip_for_time(self, current_time):
        if (self.correction_time is not None
                and current_time >= self.correction_time
                and self.corrected_zip is not None):
            return self.corrected_zip
        return self.zip_code

    def __str__(self):
        return (f"ID: {self.package_id}, {self.address}, {self.city}, {self.zip_code}, "
                f"Deadline: {self.deadline}, Weight: {self.weight}, Status: {self.status}, "
                f"Departure: {self.departure_time}, Delivery: {self.delivery_time}")


class Truck:
    def __init__(self, truck_id, speed, capacity, packages, mileage, address, depart_time):
        self.truck_id = truck_id
        self.speed = speed
        self.capacity = capacity
        self.packages = packages
        self.mileage = mileage
        self.address = address
        self.depart_time = depart_time
        self.time = depart_time # Tracks the truck's internal clock

    def __str__(self):
        return (f"Truck ID: {self.truck_id}, Speed: {self.speed}, Capacity: {self.capacity}, "
                f"Packages: {self.packages}, Mileage: {self.mileage}, Address: {self.address}, "
                f"Depart Time: {self.depart_time}")