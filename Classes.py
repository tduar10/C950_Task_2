class Package:
   def __init__(self, package_id, address, deadline, city, zip_code, weight, status="At depot", delivery_time=None):
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

    def insert(self, package_id, address, deadline, city, zip_code, weight, status="At depot", delivery_time=None):
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
