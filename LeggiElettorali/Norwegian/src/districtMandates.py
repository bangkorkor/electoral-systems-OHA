import mandatesDistribution
import csv

parties = ["+EUROPA - ITALIA IN COMUNE - PDE ITALIA",   # Dette er noob maate aa gjore det paa, br bruke instances?
"AUTONOMIE PER L'EUROPA",
"CASAPOUND ITALIA - DESTRE UNITE",
"EUROPA VERDE",
"FORZA ITALIA",
"FORZA NUOVA",
"FRATELLI D'ITALIA",
"LA SINISTRA",
"LEGA SALVINI PREMIER",
"MOVIMENTO 5 STELLE",
"PARTITO ANIMALISTA",
"PARTITO COMUNISTA",
"PARTITO DEMOCRATICO",
"PARTITO PIRATA",
"POPOLARI PER L'ITALIA",
"POPOLO DELLA FAMIGLIA - ALTERNATIVA POPOLARE",
"PPA MOVIMENTO POLITICO PENSIERO AZIONE",
"SVP"
]

regions = ["ABRUZZO",       # Dette er noob måte å gjøre det på, bør bruke instances?
"BASILICATA",
"CALABRIA",
"CAMPANIA",
"EMILIA-ROMAGNA",
"FRIULI-VENEZIA GIULIA",
"LIGURIA",
"LOMBARDIA",
"MARCHE",
"MOLISE",
"PIEMONTE",
"SARDEGNA",
"SICILIA",
"TOSCANA",
"TRENTINO-ALTO ADIGE",
"UMBRIA",
"VALLE D'AOSTA",
"VENETO",
"LAZIO",
"PUGLIA"
]

# Initialize the dictionary to hold data and results
data = []
seats = {party: 0 for party in parties}
seats_per_region = {region: {party: 0 for party in parties} for region in regions}

# Load data from the CSV file
file_path = 'LeggiElettorali/Norwegian/Data/voti_liste.csv'
with open(file_path, newline='') as file:
    reader = csv.reader(file, delimiter=',')
    next(reader)  
    for row in reader:
        region, party, votes = row
        data.append([region, party, int(votes)])

# Assuming `data` is a list of [region, party, votes]
original_votes = {}
for item in data:
    region, party, votes = item
    if region not in original_votes:
        original_votes[region] = {}
    original_votes[region][party] = votes

for region in regions:
    number_of_mandates = mandatesDistribution.getNumberOfMandates(region)
    for _ in range(number_of_mandates):
        region_list = [x for x in data if x[0] == region]
        max_key = max(region_list, key=lambda key: key[2])

        # Increment the seat count for the winning party in the region
        seats[max_key[1]] += 1
        seats_per_region[region][max_key[1]] += 1

        # Adjust the votes using a form of the Modified Sainte-Laguë method
        index = data.index(max_key)
        party_votes = original_votes[region][max_key[1]]
        
        if seats_per_region[region][max_key[1]] == 1:
            divisor = 1.4
        else:
            divisor = 2 * seats_per_region[region][max_key[1]] - 1
        
        data[index][2] = party_votes / divisor
        print(f"{max_key[1]} has won a seat in {region} with {max_key[2]} votes after adjustment.")

# Print results
for region, parties in seats_per_region.items():
    print(f"\n{region} Seats:")
    for party, count in parties.items():
        print(f"{party}: {count}")

print("\nTotal Seats per Party:")
for party, total in seats.items():
    print(f"{party}: {total}")