# districtMandates.py

The purpose of this file is to distribute the right amount of mandates to every region.

## load_regions_data

```python
def load_regions_data(self, file_path):
```

This function is reading the size.csv containing the data about the different regions, their size, and their population

## calculate_seats_per_region

```python
def calculate_seats_per_region(self):
```

This is the function that actually calculates the district mandates, based on the Sainte-Laguë method.
It returns the number of seats each region is allocated in the parliament, but not which parties get a seat.

## Other functions

There are also other functions, but these are mainly getters, that are used to fetch the variables later in the other files.
