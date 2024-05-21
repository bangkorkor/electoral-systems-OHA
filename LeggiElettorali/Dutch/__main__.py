import yaml
import os

from Classes.Mandates_distribution import Mandates_distribution

current_directory_path = os.path.dirname(__file__)
instance_directory_path = os.path.join(current_directory_path, "Instances")

for f in os.scandir(instance_directory_path):
    file = open(f)
    instance = yaml.safe_load(file)
    file.close()
    
mandates = Mandates_distribution(instance)


