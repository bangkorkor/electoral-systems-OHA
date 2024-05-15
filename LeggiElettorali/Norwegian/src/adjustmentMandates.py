import csv
from districtMandates import get_district_mandates, get_number_of_regions

# File path to the CSVs
votes_file_path = 'LeggiElettorali/Norwegian/Data/voti_liste.csv'

# Dictionary to store total votes per party
total_votes = {}

# Retrieve the district mandates directly
district_mandates = get_district_mandates()

numberOfTotalMandates = sum(district_mandates.values()) + get_number_of_regions()

# Reading the votes CSV file
with open(votes_file_path, newline='') as file:
    reader = csv.reader(file, delimiter=',')
    next(reader)  # Skip the header
    for row in reader:
        region, party, votes = row
        total_votes[party] = total_votes.get(party, 0) + int(votes)


def sainte_lague(votes, total_seats, first_divisor):
    seats = {party: 0 for party in votes}
    divisors = {party: first_divisor for party in votes}
    for _ in range(total_seats):
        highest_quota_party = max(votes, key=lambda party: votes[party] / divisors[party])
        seats[highest_quota_party] += 1
        divisors[highest_quota_party] = 2 * seats[highest_quota_party] + 1 if seats[highest_quota_party] > 1 else 3
    return seats

def calculate_mandate_differences(national_mandates, district_mandates):
    differences = {}
    print("New Iteration")
    for party in national_mandates:
        # Retrieve the number of national and district mandates for the party
        national = national_mandates.get(party, 0)
        district = district_mandates.get(party, 0)
        differences[party] = national - district

        # Print the details for each party
        print(f"Party: {party}")
        print(f"  National mandates: {national}")
        print(f"  District mandates: {district}")
        print(f"  Difference (National - District): {differences[party]}")
        print(" ")  # Adds a blank line for better readability between parties

    return differences


def adjust_mandates_until_balanced(national_mandates, district_mandates, total_votes, qualifying_threshold):
    iteration_count = 0
    while True:
        # Calculate the sum of district mandates for parties that are also in national mandates
        district_mandate_sum = sum(district_mandates.get(party, 0) for party in national_mandates if party in district_mandates)

        print(f"Iteration count: {iteration_count} -------")
        print(f"Total National mandates: {sum(national_mandates.values())}")
        print(f"Total District mandates (for parties in National mandates): {district_mandate_sum}")

        differences = calculate_mandate_differences(national_mandates, district_mandates)
        if all(value >= 0 for value in differences.values()):
            break
        needs_redistribution, reduction_of_mandates_count, new_total_votes = checkDifference(differences, national_mandates, total_votes)
        if needs_redistribution:
            # Recalculate the national mandates using the updated total_votes
            qualifying_parties = {party: votes for party, votes in new_total_votes.items() if votes >= qualifying_threshold}
            new_total_seats = sum(national_mandates.values()) - reduction_of_mandates_count  
            national_mandates = sainte_lague(qualifying_parties, new_total_seats, 1.4)
        else:
            break
        iteration_count += 1
    return differences



def checkDifference(difference, national_mandates, total_votes):
    parties_to_remove = [party for party in difference if difference[party] < 0]
    needs_redistribution = False
    
    for party in parties_to_remove:
        if party in national_mandates:
            reduction_of_mandates_count = district_mandates[party] - national_mandates[party] # SInce the party is overreperesented we must also remove the number of district mandates they where overreperesented by, since they already have won them.
            national_mandates.pop(party, None)
            needs_redistribution = True
            
       

        if party in total_votes:
            total_votes.pop(party)
    print(needs_redistribution)
    return needs_redistribution, reduction_of_mandates_count, total_votes


# Kanskje endre dette etterpå til å kun returnere total og mandates for de under sperregrensen
def calculate_under_threshold_data(total_votes, district_mandates, vote_threshold):
    under_threshold_votes = {}
    under_threshold_mandates = {}

    # Identify parties under the threshold and calculate their votes and mandates
    for party, votes in total_votes.items():
        if votes < vote_threshold:
            under_threshold_votes[party] = votes
            under_threshold_mandates[party] = district_mandates.get(party, 0)

    # Sum up the total votes and mandates for these parties
    total_votes_under_threshold = sum(under_threshold_votes.values())
    total_mandates_under_threshold = sum(under_threshold_mandates.values())

    return (under_threshold_votes, under_threshold_mandates), (total_votes_under_threshold, total_mandates_under_threshold)

total_votes_count = sum(total_votes.values())
four_percent_threshold = total_votes_count * 0.04

under_threshold_data, totals_under_treshold = calculate_under_threshold_data(total_votes, district_mandates, four_percent_threshold)

qualifying_parties = {party: votes for party, votes in total_votes.items() if votes >= four_percent_threshold}
qualifying_total_votes = sum(qualifying_parties.values())

# Remove under-threshold votes from total_votes
for party in under_threshold_data[0]:
    total_votes.pop(party, None)

qualifying_national_mandates = numberOfTotalMandates - totals_under_treshold[1]

national_mandates = sainte_lague(qualifying_parties, qualifying_national_mandates, 1.4)


mandate_differences = adjust_mandates_until_balanced(national_mandates, district_mandates, total_votes, four_percent_threshold)


print("Mandate differences between national distribution and district mandates:")
for party, difference in mandate_differences.items():
    print(f"{party}: National vs. District difference = {difference} mandates")