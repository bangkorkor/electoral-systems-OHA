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

results = mandates.total_party_mandates
visualizer = Visualize(results, instance)
visualizer.show_dot_chart()
#visualizer.show_circular_bar_plot()
# visualizer.show_diagrams()

