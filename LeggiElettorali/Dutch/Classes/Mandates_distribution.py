import csv
import math
import json
import os


NUM_MANDATES = 605  # Number of mandates

class Mandates_distribution:

    def __init__(self, instance):
        current_directory_path = os.path.dirname(__file__)

        self.vote_data = self.get_data(current_directory_path +"/../Data/" + instance["data"]["vote_data_csv"])
        self.parties = self.get_parties(current_directory_path + "/../Data/" + instance["data"]["parties"])
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
    
    def get_parties(self, file_path):
        # reads json file ansd intializes the mandates dictionary   
        with open(file_path, 'r') as file:
            data = json.load(file)
        parties = data['parties']
        empty_mandates_distriubtion = {party: 0 for party in parties}
        return empty_mandates_distriubtion
    
    def get_mandate_distribution(self, data, parties):
        # assign mandates to each party by rounding down, this will leave some mandates unassigned
        mandates_distribution = parties.copy()      # dictionary to hold the number of mandates per party
        total_votes = sum(data.values())            # sums all the total votes
        electoral_devisor = total_votes / NUM_MANDATES
        for party, vote in data.items():
            mandates_distribution[party] = math.floor(vote / electoral_devisor)

        # ASSIGN THE REMINDING MANDATES
        mandates_left = NUM_MANDATES -  sum(mandates_distribution.values())   
        # remove parties that have zero mandates
        parties_suitable = {}
        for party, mandate in mandates_distribution.items():
            if mandate > 0:
                parties_suitable[party] = mandate

        # give mandate to the party with the higest votes per mandate
        while mandates_left > 0:
            votes_per_mandate = {}
            for party, vote in data.items():
                if party in parties_suitable:
                    votes_per_mandate[party] = vote / (parties_suitable[party])
            party_with_highest_votes_per_mandate = max(votes_per_mandate, key=votes_per_mandate.get)
            parties_suitable[party_with_highest_votes_per_mandate] += 1
            mandates_left -= 1
            # print(f'{party_with_highest_votes_per_mandate} got an additional mandate')
            # print(f'{mandates_left} mandates left to assign')
            # print()    
        # updating the mandates dictionary to include the new mandates, (the old mandates are still there)
        for party, mandate in parties_suitable.items():
            mandates_distribution[party] = mandate            
        
        return mandates_distribution
    
    def print_dict_by_value(self, dict):
        for key in sorted(dict, key=dict.get, reverse=True):
            print(f'{key}: {dict[key]}')
        

        
        



