import csv

# Path to the CSV file
file_path = 'LeggiElettorali/Norwegian/Data/size.csv'

# List to hold the data
data = []

# Open the file in read mode
with open(file_path, newline='') as file:
    # Create a CSV reader object using a comma as the delimiter
    reader = csv.reader(file, delimiter=',')
    
    # Iterate over each row in the CSV
    for row in reader:
        # Clean up and strip any unwanted spaces
        row = [item.strip() for item in row]
        # Convert the second and third items in the list to integers
        row[1] = int(row[1])
        row[2] = int(row[2])
        # Append the row to our data list
        data.append(row)


# Calculate the number of refrence score
refrenceScore0 = {}
for row in data:
    refrenceScore0[row[0]] = row[1]+  1.8 * row[2]

# Sainte-Laguë method
mandates = {key:0 for key in refrenceScore0.keys()}

refrenceScore = refrenceScore0.copy()
for i in range(150):
    max_key = max(refrenceScore, key=lambda key: refrenceScore[key])      # max_key is the party with the highest refrenceScore
    mandates[max_key] += 1
    refrenceScore[max_key] = refrenceScore0[max_key] / (2*mandates[max_key] + 1)

    


for key in mandates.keys():
    print(key, mandates[key])

print()
print("Sum mandates:", sum(mandates.values()))



