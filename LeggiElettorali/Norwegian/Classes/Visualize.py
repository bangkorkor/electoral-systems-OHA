import json
import os
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import poli_sci_kit
import matplotlib.patches as mpatches
import numpy as np



class Visualize:
    def __init__(self, mandates,instance):
        current_directory_path = os.path.dirname(__file__)
        self.mandate_distribution = mandates
        self.party_colors = self.get_party_colors(current_directory_path + "/../Data/" + instance["data"]["colors"])
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


         #We do not want to plot the parties that got 0 seats, so we remove them when plotting
        parties_that_have_a_seat = self.get_remove_losers(self.mandate_distribution)

        #Sort the parties in ascending order by the number of seats received
        sorted_mandates_list = sorted(parties_that_have_a_seat.items(), key=lambda item: item[1])
        sorted_parties = [party for party, seats in sorted_mandates_list]
        sorted_seats = [seats for party, seats in sorted_mandates_list]
        print("Lengde seats:", len(sorted_seats))

        # COLORS, keep only parties that have mandates
        colors = []
        for elm in self.party_colors:
            if elm in parties:
                colors.append(self.party_colors[elm])

        print("Lengde colors: ", len(colors))


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
            allocations=sorted_seats,
            labels=parties,
            colors=colors2,
            style="rectangle",
            num_rows=23,
            marker_size=120,
            speaker=False,
            axis=ax2,
)

        plt.title("The Norwegian system\n applied on the 2019\n Italian election results", fontsize=25, pad=20, loc='center', x=0.01, y=0.70)
        plt.subplots_adjust(left=0.2, right=1.15, top=0.9, bottom=0.1)
        # Create a legend for party colors
        legend_patches = [mpatches.Patch(color=color, label=party) for party, color in zip(sorted_parties, colors)]
        ax2.legend(handles=legend_patches, loc='upper left', bbox_to_anchor=(-0.18, 0.65), fontsize='medium', frameon=True)

        plt.show()

 #Plot nr. 2

    def show_circular_bar_plot(self):


        parties = list(self.get_remove_losers(self.mandate_distribution).keys())

        #We do not want to plot the parties that got 0 seats, so we remove them when plotting
        parties_that_have_a_seat = self.get_remove_losers(self.mandate_distribution)

        #Sort the parties in ascending order by the number of seats received
        sorted_mandates_list = sorted(parties_that_have_a_seat.items(), key=lambda item: item[1])
        sorted_parties = [party for party, seats in sorted_mandates_list]
        sorted_seats = [seats for party, seats in sorted_mandates_list]

        # set figure size
        plt.figure(figsize=(10,7))

        # plot polar axis
        ax = plt.subplot(111, polar=True)

        # remove grid
        plt.axis('off')

        # Set the coordinates limits
        upperLimit = 250
        lowerLimit = 100

        # Compute max and min in the dataset
        max_value = max(sorted_seats)

        # Let's compute heights: they are a conversion of each item value in those new coordinates
        # In our example, 0 in the dataset will be converted to the lowerLimit (10)
        # The maximum will be converted to the upperLimit (100)
        slope = (max_value - lowerLimit) / max_value
        print("Her kommer slopene: ", slope)
        sorted_seats = np.array(sorted_seats)
        heights = slope * sorted_seats + np.log(sorted_seats+1) * 60
        print("Her kommer høydene: ", heights)

        # Compute the width of each bar. In total we have 2*Pi = 360°
        width = 2*np.pi / len(sorted_seats)

        # Compute the angle each bar is centered on:
        indexes = list(range(1, len(sorted_seats)+1))
        angles = [element * width for element in indexes]
        angles

        # Define colors for bars
        colors = []
        for elm in self.party_colors:
            if elm in parties:
                colors.append(self.party_colors[elm])
 
        # Draw bars
        bars = ax.bar(
            x=angles, 
            height=heights, 
            width=width, 
            bottom=lowerLimit,
            linewidth=2, 
            edgecolor="white",
            color=colors)

        # little space between the bar and the label
        labelPadding = 15

        # Add labels
        for bar, angle, height, label, seats in zip(bars,angles, heights, sorted_parties, sorted_seats):

            # Labels are rotated. Rotation must be specified in degrees :(
            rotation = np.rad2deg(angle)

            # Flip some labels upside down
            alignment = ""
            if angle >= np.pi/2 and angle < 3*np.pi/2:
                alignment = "right"
                rotation = rotation + 180
            else: 
                alignment = "left"

            # Finally add the labels
            ax.text(
                x=angle, 
                y=lowerLimit + bar.get_height() + labelPadding, 
                s=label, 
                ha=alignment, 
                va='center', 
                rotation=rotation, 
                rotation_mode="anchor") 
    
            ax.text(
                x=angle, 
                y=lowerLimit + bar.get_height()/2.2,
                s=seats, 
                ha=alignment, 
                va='center', 
                rotation=rotation, 
                rotation_mode="anchor") 

        ax.set_title("The Norwegian system applied on the 2019 Italian election results", pad=10, fontsize=20, y=1.05)
        plt.tight_layout(pad=3)
        plt.show()

    
        
        
