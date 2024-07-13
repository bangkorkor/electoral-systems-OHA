# main.py

This is the file used to run both the calculations and to visually represent the results.
It creates an instance using the structure in Dutch_electoral_system.yaml and uses this instance to run the
Mandates_distribution.py:

```python
    mandates = Mandates_distribution(instance)
```

It then creates an instance of Visualize, and uses the numbers from Mandates_distribution.py to plot the results, by calling the two plotting functions in Visualize.py:

```python
visualizer.show_dot_chart()
visualizer.show_circular_bar_plot()
```
