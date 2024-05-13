import mandates
import csv

# Path to the CSV file
file_path = 'LeggiElettorali/Norwegian/Data/voti_liste.csv'

# List to hold the data
data = []

# Open the file in read mode
with open(file_path, newline='') as file:
    
    reader = csv.reader(file, delimiter=',')
    next(reader)  # Skip header row if there is one
    
    # Iterate over each row in the CSV
    for row in reader:
        region, party, votes = row
        votes = int(votes)
    
        data.append([region, party, votes])

# for row in data:
#     print(row)


parties = ["+EUROPA - ITALIA IN COMUNE - PDE ITALIA",   # Dette er noob måte å gjøre det på, bør bruke instances?
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

seats = {key:0 for key in parties}



data0 = data.copy()
for row in data:
    row[2]= row[2] / 1.4

for region in regions:
    # print(region)
    number_of_mandates = mandates.getNumberOfMandates(region)
    # print(number_of_mandates)
    for i in range(number_of_mandates):
        region_list = [x for x in data if x[0] == region]
        # print(region_list, "\n")
        max_key = max(region_list, key=lambda key: key[2])
        # print("MAX IS:__________")
        # print(max_key)

        seats[max_key[1]] += 1
    
        print(max_key[1], "has won a seat in", region, "with", max_key[2], "in score")
        # sainte lague
        data[data.index(max_key)][2] = max_key[2] / (2*seats[max_key[1]] + 1)
        print()
    
            # Todo: change sainte lauge to have it not divide by number of seats in the parlament, but the number of seats won in the region
            # Change that we don't divide all the data by 1.4 when we calculate the reference score, but after bla bla... 

for key in seats.keys():
    print(key, seats[key])

print("Sum seats:", sum(seats.values()))
            


            
    

