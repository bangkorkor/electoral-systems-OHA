import csv
import json
import os

class AdjustmentMandates:
    def __init__(self, instance):
        # Initialize the necessary data from the given instance
        current_directory_path = os.path.dirname(__file__)

        self.vote_data = self.get_vote_data(os.path.join(current_directory_path, "../Data/", instance["data"]["vote_data_csv"]))
        self.parties = self.get_parties(os.path.join(current_directory_path, "../Data/", instance["data"]["parties"]))

    def get_vote_data(self, file_path):
        # Read vote data from the CSV file
        vote_data = {}
        with open(file_path, newline='') as file:
            reader = csv.reader(file, delimiter=',')
            next(reader)  # Skip the header row
            for row in reader:
                region, party, votes = row
                votes = int(votes)
                if region not in vote_data:
                    vote_data[region] = {}
                vote_data[region][party] = votes
        return vote_data

    def get_parties(self, file_path):
        # Read party data from the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data['parties']

    def calculate_total_votes(self):
        # Calculate the total number of votes for each party across all regions
        total_votes = {}
        for region, region_votes in self.vote_data.items():
            for party, votes in region_votes.items():
                if party not in total_votes:
                    total_votes[party] = 0
                total_votes[party] += votes
        return total_votes

    def calculate_percentages(self):
        # Calculate the percentage of total votes for each party
        total_votes = self.calculate_total_votes()
        total_votes_sum = sum(total_votes.values())
        percentages = {party: (votes / total_votes_sum) * 100 for party, votes in total_votes.items()}
        return percentages
