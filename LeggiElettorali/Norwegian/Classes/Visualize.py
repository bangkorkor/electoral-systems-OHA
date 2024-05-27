import json
import os
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import poli_sci_kit
import matplotlib.patches as mpatches



class Visualize:
    def __init__(self, mandates,instance):
        current_directory_path = os.path.dirname(__file__)

        self.mandate_distribution = mandates
        #self.party_colors = self.get_party_colors(current_directory_path + "/../Data/" + instance["data"]["colors"])
        #print(self.party_colors)
        #self.parties = list(self.mandate_distribution.keys())
        #self.mandates = list(self.mandate_distribution.values())


    def get_party_colors(self, file_path):
        with open(file_path, 'r') as file:
            colors = json.load(file)
        return colors
        

    def get_remove_losers(self, mandate_list):
        # remove parties that have zero mandates
        parties_suitable = {}
        for party, mandate in mandate_list.items():
            if mandate > 0:
                parties_suitable[party] = mandate
        return parties_suitable

    def show_dot_chart(self):
        parties = list(self.get_remove_losers(self.mandate_distribution).keys())
        mandates = list(self.get_remove_losers(self.mandate_distribution).values())


        # COLORS, keep only parties that have mandates
        #colors = []
        #for elm in self.party_colors:
         #   if elm in parties:
         #       colors.append(self.party_colors[elm])


        colors2 = [
            "#FF5733",  # Red-Orange
            "#33FF57",  # Lime Green
            "#3357FF",  # Blue
            "#F0FF33",  # Yellow
            "#FF33F0",  # Pink
            "#33FFF0",  # Aqua
            "#F033FF",  # Purple
            "#FF8633",  # Orange
            "#86FF33",  # Light Green
            "#3386FF"   # Light Blue
]
        

        fig, ax2 = plt.subplots(figsize=(10,7))  # Only ax2 subplot

        ax2 = poli_sci_kit.plot.parliament(
            allocations=mandates,
            labels=parties,
            colors=colors2,
            style="semicircle",
            num_rows=12,
            marker_size=60,
            speaker=False,
            axis=ax2,
)

        # Create a legend for party colors
        legend_patches = [mpatches.Patch(color=color, label=party) for party, color in zip(parties, colors2)]
        ax2.legend(handles=legend_patches, loc='upper left')

        plt.show()


    
        
        
