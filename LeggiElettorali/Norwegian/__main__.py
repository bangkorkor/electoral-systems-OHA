import yaml
import os

from Classes.mandatesDistribution import MandatesDistribution
from Classes.Visualize import Visualize

current_directory_path = os.path.dirname(__file__)
instance_directory_path = os.path.join(current_directory_path, "Instances")

for f in os.scandir(instance_directory_path):
    if f.is_file() and f.name.endswith('.yaml'):
        with open(f, 'r') as file:
            instance = yaml.safe_load(file)
            mandates = MandatesDistribution(instance)
            mandates.print_results()

#Stores the mandate distribution in a variable called results, which can then be used for plotting
results = mandates.total_party_mandates

#Instantiates an instance of Visualize
visualizer = Visualize(results, instance)

#Plots the dot chart
visualizer.show_dot_chart()

#Plots the circular bar plot
visualizer.show_circular_bar_plot()

