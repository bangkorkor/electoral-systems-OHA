# adjustmentMandates.py

This file is used to calculate and distribute the adjustment mandates. This process is quite complicated,
and so the full explanation on how it works can be found in the final report.

## get_vote_data

```python
def get_vote_data(self, file_path):
```

This function is reading the voti_liste.csv and stores in variables how many votes each party has gotten in every region.

## def calculate_total_votes

```python
    def calculate_total_votes(self):
```

This function calculates and returns the total number of votes each party has received nationwide.

## calculate_percentages

```python
    def calculate_percentages(self):
```

This small function simply calculates the percentage of total votes each party has received

## Other info

The functions here are used to calculate some of the numbers needed in the mandatesDistribution.py,
where the final allocations of the seats are calculated.
