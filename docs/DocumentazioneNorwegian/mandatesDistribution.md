# mandatesDistribution.py

This is the final file, and it basically collects all the data calculated in the two previous functions and use them to calculate and return the final distribution of seats. These return values are then used in Visualize.py to plot the results.

## calculate_under_threshold_data

```python
def calculate_under_threshold_data(self):
```

This function checks whether or not a party has received enough votes in a region to lie above the 4% threshold. If not, it will not be able to get any representatives at the parliament.

## calculate_qualifying_district_mandates

```python
    def calculate_qualifying_district_mandates(self):
```

This one simply retrieves the number of district mandates the qualifying parties is granted.

## sainte_lague

```python
    def sainte_lague(self, votes, total_seats, first_divisor):
```

Here comes the distribution of seats using the Sainte-Laguë method

## calculate_national_mandates

```python
    def calculate_national_mandates(self):
```

This calculates the national mandates for qualifying parties, which will then later together with the district mandates be used to allocate the adjustment mandates.

## adjust_mandates_until_balanced

```python
    def adjust_mandates_until_balanced(self):
```

Now it is time to adjust the mandates until all differences are non-negative

## remove_overrepresented_parties

```python
    def remove_overrepresented_parties(self, differences):
```

The name of the function pretty much explains it, but its purpose is to remove the parties that are overrepresented (negative difference)

## calculate_regional_quotients

```python
    def calculate_regional_quotients(self):
```

For the adjustment mandates, a list of regional quotients has to be calculated, and these are later sorted using another function called flatten_sorted_quotients.

## assign_adjustment_mandates

```python
    def assign_adjustment_mandates(self):
```

Now that each party allocated adjustment mandates have a weighted quotient in each region, we can start distributing the parties adjustment mandates from the different regions. The full details on how this is done can be found in the final report.

## calculate_district_mandate_distribution

```python
    def calculate_district_mandate_distribution(self):
```

This function uses the return values calculated in districtMandates.py to calculate the distribution of district mandates

## calculate_total_party_mandates

```python
    def calculate_total_party_mandates(self):
```

Now it is time to sum up and compute the total number of mandates each party is receiving, using all of the previous functions.
