import yaml
import os

from Classes.Mandates_distribution import Mandates_distribution
from Classes.Visualize import Visualize

current_directory_path = os.path.dirname(__file__)
instance_directory_path = os.path.join(current_directory_path, "Instances")

for f in os.scandir(instance_directory_path):
    file = open(f)
    instance = yaml.safe_load(file)
    file.close()
    
#Creates and instance of Mandates_distribution and calculates results
mandates = Mandates_distribution(instance)
results = mandates.mandate_distribution

#Instantiates an instance of Visualize
visualizer = Visualize(results, instance)

#Plots the dot chart
visualizer.show_dot_chart()

#Plots the circular bar plot
visualizer.show_circular_bar_plot()



