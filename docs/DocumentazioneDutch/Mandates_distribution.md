# Mandates_distribution.py

Because of the simplicity of the Dutch electoral system, the team realized that only one class was needed for the calculation. This class is called Mandates_distribution and is the file that returns the values that are to be used in the visualization class Visualize.py

## get_data

```python
    def get_data(self, file_path):
```

As only the total votes received by each party is relevant, this function reads the voti_liste.csv and returns the total votes a party has received across all regions.

## get_mandate_distribution

```python
    def get_mandate_distribution(self, data, parties):
```

This function simulates the first part of the mandate distribution, where the Hare quota is calcuated for each party and the seats are thereafter assigned based on this quota. Because we’re always rounding down, there will be instances where one or more mandates remain not distributed. When this happens, the distribution of these mandates will be calculated using another method called the D’Hondt method which is also included in this function.
