import yaml
import os

from Classes.mandatesDistribution import MandatesDistribution

current_directory_path = os.path.dirname(__file__)
instance_directory_path = os.path.join(current_directory_path, "Instances")

for f in os.scandir(instance_directory_path):
    if f.is_file() and f.name.endswith('.yaml'):
        with open(f, 'r') as file:
            instance = yaml.safe_load(file)
            mandates = MandatesDistribution(instance)
            mandates.print_results()
