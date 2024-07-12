import csv
import os

class DistrictMandates:
    TOTAL_MANDATES = 73

    def __init__(self, instance):
        # Initialize the necessary data from the given instance
        current_directory_path = os.path.dirname(__file__)
        self.regions_data = self.load_regions_data(os.path.join(current_directory_path, "../Data/", instance["data"]["size_csv"]))
        self.number_of_regions = len(self.regions_data)
        self.total_mandates = self.TOTAL_MANDATES - self.number_of_regions  # Total mandates excluding one adjustment mandate per region
        self.seats_per_region = self.calculate_seats_per_region()
        self.district_mandates = self.calculate_district_mandates()


    #Reading the size.csv containing the data about the different regions, their size, and their population
    def load_regions_data(self, file_path):
        # Load regions data from the CSV file
        regions_data = []
        with open(file_path, newline='') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                region, population, size = row
                regions_data.append({
                    'name': region,
                    'population': int(population),
                    'size': int(size)
                })
        return regions_data

    def calculate_seats_per_region(self):
        # Calculate the number of seats per region using Sainte-Laguë method
        total_population = sum(region['population'] for region in self.regions_data)
        total_size = sum(region['size'] for region in self.regions_data)

        # Calculate weights for each region based on population and size
        weights = {region['name']: region['population'] + 1.4 * region['size'] for region in self.regions_data}
        total_weight = sum(weights.values())

        # Initialize seats and divisors for Sainte-Laguë method
        seats = {region['name']: 0 for region in self.regions_data}
        divisors = {region['name']: 1.0 for region in self.regions_data}

        # Distribute seats using Sainte-Laguë method
        for _ in range(self.total_mandates):
            highest_weight_region = max(weights, key=lambda r: weights[r] / divisors[r])
            seats[highest_weight_region] += 1
            divisors[highest_weight_region] += 2

        return seats

    def calculate_district_mandates(self):
        # Use the calculated seats per region as district mandates
        return self.seats_per_region

    def get_number_of_regions(self):
        # Return the number of regions
        return self.number_of_regions

    def get_district_mandates(self):
        # Return the district mandates
        return self.district_mandates

    def get_seats_per_region(self):
        # Return the seats per region
        return self.seats_per_region
    
    def get_total_district_seats(self):
        # Return the total number of district seats
        return sum(self.district_mandates.values())

    @classmethod
    def get_total_mandates(cls):
        return cls.TOTAL_MANDATES