class Package:
   def __init__(self, package_id, address, deadline, city, zip_code, weight, status="At the hub", delivery_time=None):
        self.package_id = package_id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip_code = zip_code
        self.weight = weight
        self.status = status
        self.delivery_time = delivery_time

  
