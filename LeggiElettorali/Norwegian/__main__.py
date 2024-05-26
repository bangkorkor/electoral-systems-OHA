import yaml
import os

from mandates_distribution import MandatesDistribution
from district_mandates import DistrictMandates

def load_instance(file_path):
    with open(file_path, 'r') as file:
        instance = yaml.safe_load(file)
    return instance

def main():
    current_directory_path = os.path.dirname(__file__)
    instance_directory_path = os.path.join(current_directory_path, "Instances")

    for f in os.scandir(instance_directory_path):
        if f.is_file() and f.name.endswith('.yaml'):
            instance = load_instance(f.path)
            if "mandates_distribution" in instance["type"]:
                MandatesDistribution(instance)
            elif "district_mandates" in instance["type"]:
                DistrictMandates(instance)

if __name__ == "__main__":
    main()
