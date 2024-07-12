# Visualize.py

This script uses the results calculated in the other functions and gives a visual representation of how the Italian parliament will look using the Norwegian electoral system.

## Prepare the results

```python
    def get_party_colors(self, file_path):

    def get_remove_losers(self, mandate_list):

```

These functions are used to prepare the plotting by fetching the results calculated, and the colors associated to each party.

## show_dot_chart

```python
    def show_dot_chart(self):
```

This is the first type of plot and it uses a python library called poli_sci_kit to plot the seat distribution as a number of squares, where each square represents a seat, and the color of the square symbolizes the party it is allocated to. This gives a nice overview.

## show_circular_bar_plot

```python
    def show_circular_bar_plot(self):
```

This is the second type of plot, and it is what is called a "circular bar plot". Here the parties that received a seat will be represented using a bar, and the height of this bar will indicate the total number of seats. The width is constant for every party represented.
