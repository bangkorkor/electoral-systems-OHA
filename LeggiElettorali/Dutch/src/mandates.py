import csv
import math

NUM_SEATS = 605  # Number of seats

PARTIES = ["+EUROPA - ITALIA IN COMUNE - PDE ITALIA",   # Dette er noob maate aa gjore det paa, br bruke instances?
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

# function for printing sorted dictionary
def sort_dict_by_value(dict):
    for key in sorted(dict, key=dict.get, reverse=True):
        print(f'{key}: {dict[key]}')
    

# Initialize the dictionary to hold results
seats = {party: 0 for party in PARTIES}

# Read the CSV file
file_path = 'LeggiElettorali/Dutch/Data/voti_liste.csv' # Path to the CSV file
data = []   # List of lists, each list contains the party and the number of votes

with open(file_path, newline='') as file:
    reader = csv.reader(file, delimiter=',')
    next(reader)  
    for row in reader:
        region, party, votes = row
        data.append([party, int(votes)])

# Get total number of votes for each party
votes_for_party = {}
for party, vote in data:
    if party in votes_for_party:
        votes_for_party[party] += vote
    else:
        votes_for_party[party] = vote


# ----------------- D´Hondt method ----------------- 
# here the seats are assigned
# --------------------------------------------------

total_votes = sum(votes_for_party.values())

# assign seats to each party by rounding down, this will leave some seats unassigned
electoral_devisor = total_votes / NUM_SEATS
for party, vote in votes_for_party.items():
    seats[party] = math.floor(vote / electoral_devisor)

seats_left = NUM_SEATS -  sum(seats.values())   # Number of seats left to assign

sort_dict_by_value(seats)
print()
print("Ordinary seats are assigned!")
print(f'{seats_left} seats left to assign')
print()


# ASSIGN THE REMINDING SEATS

# remove parties that have zero seats
patries_with_seats = {}
for party, seat in seats.items():
    if seat > 0:
        patries_with_seats[party] = seat

# give seat to the party with the higest votes per seat
while seats_left > 0:
    votes_per_seat = {}
    for party, vote in votes_for_party.items():
        if party in patries_with_seats:
            votes_per_seat[party] = vote / (patries_with_seats[party])
    party_with_highest_votes_per_seat = max(votes_per_seat, key=votes_per_seat.get)
    patries_with_seats[party_with_highest_votes_per_seat] += 1
    seats_left -= 1
    print(f'{party_with_highest_votes_per_seat} got an additional seat')
    print(f'{seats_left} seats left to assign')
    print()

# updating the seats dictionary to include the new seats, (the old seats are still there)
for party, seat in patries_with_seats.items():
    seats[party] = seat

sort_dict_by_value(seats)
