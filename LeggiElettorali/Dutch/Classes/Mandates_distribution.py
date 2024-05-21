import csv
import math
import json
import os


NUM_SEATS = 605  # Number of seats

class Mandates_distribution:

    def __init__(self, instance):
        current_directory_path = os.path.dirname(__file__)

        self.vote_data = self.get_data(current_directory_path +"/../Data/" + instance["data"]["vote_data_csv"])
        self.parties = self.get_parites(current_directory_path + "/../Data/" + instance["data"]["parties"])
        self.mandate_distribution = self.get_mandate_distribution(self.vote_data, self.parties)
        self.print_dict_by_value(self.mandate_distribution)

    

    def get_data(self, file_path): 
        # reads the csv file and returns a list of lists with the party and the number of votes 
        data = []
        with open(file_path, newline='') as file:
            reader = csv.reader(file, delimiter=',')
            next(reader)  
            for row in reader:
                region, party, votes = row      # mark that region is not used
                data.append([party, int(votes)])
        # Get total number of votes for each party
        votes_for_party = {}
        for party, vote in data:
            if party in votes_for_party:
                votes_for_party[party] += vote
            else:
                votes_for_party[party] = vote   
        return votes_for_party
    
    def get_parites(self, file_path):
        # reads json file ansd intializes the mandates dictionary   
        with open(file_path, 'r') as file:
            data = json.load(file)
        parties = data['parties']
        empty_mandates_distriubtion = {party: 0 for party in parties}
        return empty_mandates_distriubtion
    
    def get_mandate_distribution(self, data, parties):
        # assign seats to each party by rounding down, this will leave some seats unassigned
        mandates_distribution = parties.copy()      # dictionary to hold the number of mandates per party
        total_votes = sum(data.values())            # sums all the total votes
        electoral_devisor = total_votes / NUM_SEATS
        for party, vote in data.items():
            mandates_distribution[party] = math.floor(vote / electoral_devisor)

        # ASSIGN THE REMINDING SEATS
        seats_left = NUM_SEATS -  sum(mandates_distribution.values())   # Number of seats left to assign
        # remove parties that have zero seats
        patries_with_seats = {}
        for party, seat in mandates_distribution.items():
            if seat > 0:
                patries_with_seats[party] = seat

        # give seat to the party with the higest votes per seat
        while seats_left > 0:
            votes_per_seat = {}
            for party, vote in data.items():
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
            mandates_distribution[party] = seat            
        
        return mandates_distribution
    
    def print_dict_by_value(self, dict):
        for key in sorted(dict, key=dict.get, reverse=True):
            print(f'{key}: {dict[key]}')
        

        
        



