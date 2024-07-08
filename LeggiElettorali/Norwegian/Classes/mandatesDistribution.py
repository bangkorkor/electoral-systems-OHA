import os
from Classes.adjustmentMandates import AdjustmentMandates
from Classes.districtMandates import DistrictMandates

class MandatesDistribution:
    def __init__(self, instance):
        # Initialize the necessary data from the given instance
        self.adjustment_mandates = AdjustmentMandates(instance)
        self.district_mandates = DistrictMandates(instance)

        self.vote_data = self.adjustment_mandates.vote_data
        self.total_district_seats = self.district_mandates.get_total_district_seats()
        self.total_mandates = DistrictMandates.TOTAL_MANDATES  # Total mandates
        self.total_votes_dict = self.calculate_total_votes()
        self.total_votes = sum(self.total_votes_dict.values())  # Sum of all votes
        self.qualifying_threshold = 0.04 * self.total_votes  # Threshold to qualify for adjustment mandates

        self.district_mandate_distribution = self.calculate_district_mandate_distribution()
        self.under_threshold_data, self.totals_under_threshold = self.calculate_under_threshold_data()
        self.qualifying_parties = self.get_qualifying_parties()
        self.qualifying_district_mandates = self.calculate_qualifying_district_mandates()
        self.qualifying_national_mandates = self.qualifying_district_mandates + 20  # Total district mandates for qualifying parties + 20 adjustment mandates
        self.national_mandates = self.calculate_national_mandates()
        self.mandate_differences = self.adjust_mandates_until_balanced()
        self.regional_quotients = self.calculate_regional_quotients()
        self.adjustment_mandates_distribution = self.assign_adjustment_mandates()
        self.party_percentages = self.adjustment_mandates.calculate_percentages()
        self.total_party_mandates = self.calculate_total_party_mandates()

    def calculate_total_votes(self):
        # Calculate the total number of votes for each party across all regions
        total_votes = {}
        for region_votes in self.vote_data.values():
            for party, votes in region_votes.items():
                total_votes[party] = total_votes.get(party, 0) + votes
        return total_votes

    def calculate_under_threshold_data(self):
        # Calculate the votes and mandates for parties under the threshold
        under_threshold_votes = {}
        under_threshold_mandates = {}
        for region, region_votes in self.vote_data.items():
            for party, votes in region_votes.items():
                if self.total_votes_dict[party] < self.qualifying_threshold:
                    if party not in under_threshold_votes:
                        under_threshold_votes[party] = 0
                    under_threshold_votes[party] += votes
                    under_threshold_mandates[party] = self.district_mandate_distribution.get(region, {}).get(party, 0)
        total_votes_under_threshold = sum(under_threshold_votes.values())
        total_mandates_under_threshold = sum(under_threshold_mandates.values())
        return (under_threshold_votes, under_threshold_mandates), (total_votes_under_threshold, total_mandates_under_threshold)

    def get_qualifying_parties(self):
        # Get parties that have votes above the qualifying threshold
        qualifying_parties = {}
        for party, votes in self.total_votes_dict.items():
            if votes >= self.qualifying_threshold:
                qualifying_parties[party] = votes
        return qualifying_parties

    def calculate_qualifying_district_mandates(self):
        # Calculate the number of district mandates for qualifying parties
        qualifying_district_mandates = 0
        for party in self.qualifying_parties:
            for region in self.district_mandate_distribution:
                qualifying_district_mandates += self.district_mandate_distribution[region].get(party, 0)
        return qualifying_district_mandates

    def sainte_lague(self, votes, total_seats, first_divisor):
        # Distribute seats using the Sainte-Laguë method
        seats = {party: 0 for party in votes}
        divisors = {party: first_divisor for party in votes}
        for _ in range(total_seats):
            highest_quota_party = max(votes, key=lambda party: votes[party] / divisors[party])
            seats[highest_quota_party] += 1
            divisors[highest_quota_party] = 2 * seats[highest_quota_party] + 1 if seats[highest_quota_party] > 1 else 3
        return seats

    def calculate_national_mandates(self):
        # Calculate the national mandates for qualifying parties
        return self.sainte_lague(self.qualifying_parties, self.qualifying_national_mandates, 1.4)

    def calculate_mandate_differences(self):
        # Calculate the difference between national and district mandates for each party
        differences = {}
        for party in self.qualifying_parties:
            national = self.national_mandates.get(party, 0)
            district = sum(self.district_mandate_distribution[region].get(party, 0) for region in self.district_mandate_distribution)
            differences[party] = national - district
        return differences

    def adjust_mandates_until_balanced(self):
        # Adjust mandates until all differences are non-negative
        iteration_count = 0
        while True:
            differences = self.calculate_mandate_differences()
            print(f"\nIteration {iteration_count} Differences: {differences}")
            if all(value >= 0 for value in differences.values()):
                break
            self.remove_overrepresented_parties(differences)
            self.national_mandates = self.calculate_national_mandates()
            iteration_count += 1
        return self.calculate_mandate_differences()  # Return the final differences

    def remove_overrepresented_parties(self, differences):
        # Remove parties that are overrepresented (negative difference)
        parties_to_remove = [party for party in differences if differences[party] < 0]
        
        for party in parties_to_remove:
            if party in self.total_votes_dict:
                del self.total_votes_dict[party]

        self.qualifying_parties = {party: votes for party, votes in self.total_votes_dict.items() if votes >= self.qualifying_threshold}
        self.qualifying_district_mandates = self.calculate_qualifying_district_mandates()
        self.qualifying_national_mandates = self.qualifying_district_mandates + 20

    def calculate_regional_quotients(self):
        # Calculate the regional quotients for adjustment mandates
        quotients = {}
        for region, region_votes in self.vote_data.items():
            region_mandates = self.district_mandates.get_district_mandates().get(region, 0)
            total_votes_in_region = sum(region_votes.values())
            average_votes_per_mandate = total_votes_in_region / region_mandates if region_mandates else 0

            # Calculate quotients only for qualified parties
            region_quotients = {}
            for party, votes in region_votes.items():
                if party in self.qualifying_parties:  # Check if party is in the qualifying_parties dict
                    base_quotient = votes / (2 * region_mandates + 1) if region_mandates else 0
                    normalized_quotient = base_quotient / average_votes_per_mandate if average_votes_per_mandate else 0
                    region_quotients[party] = normalized_quotient
            
            quotients[region] = region_quotients

        return quotients

    def flatten_sorted_quotients(self):
        # Flatten and sort quotients for adjustment mandate distribution
        flat_list = []
        for region, parties in self.regional_quotients.items():
            for party, quotient in parties.items():
                flat_list.append((region, party, quotient))
        return sorted(flat_list, key=lambda x: x[2], reverse=True)

    def assign_adjustment_mandates(self):
        # Assign adjustment mandates based on sorted quotients
        sorted_quotients = self.flatten_sorted_quotients()
        required_mandates = self.mandate_differences
        assignments = {}
        regions_assigned = set()
        party_mandates_assigned = {party: 0 for party in required_mandates}

        print("\nAdjustment Mandate Distribution Process:")

        for region, party, quotient in sorted_quotients:
            if region in regions_assigned:
                continue  # Skip if the region has already been assigned an adjustment mandate

            if party_mandates_assigned[party] >= required_mandates[party]:
                continue  # Skip if the party has already received all its adjustment mandates

            if party not in assignments:
                assignments[party] = []
            assignments[party].append(region)
            party_mandates_assigned[party] += 1
            regions_assigned.add(region)

            # Print detailed steps for adjustment mandate distribution
            print(f"Assigned adjustment mandate to {party} in {region} (Quotient: {quotient})")

            # Stop if all mandates are assigned
            if len(regions_assigned) == len(self.district_mandates.regions_data):
                break

        return assignments

    def calculate_district_mandate_distribution(self):
        # Calculate the distribution of district mandates
        district_distribution = {}
        total_distributed_seats = 0
        for region, region_votes in self.vote_data.items():
            total_seats = self.district_mandates.get_district_mandates()[region]
            district_distribution[region] = self.sainte_lague(region_votes, total_seats, 1.4)
            total_distributed_seats += total_seats
        if total_distributed_seats != self.total_district_seats:
            raise ValueError(f"Total distributed district mandates ({total_distributed_seats}) does not match expected total ({self.total_district_seats})")
        return district_distribution

    def calculate_total_party_mandates(self):
        # Calculate the total mandates for each party
        total_party_mandates = {}
        for region, mandates in self.district_mandate_distribution.items():
            for party, mandate_count in mandates.items():
                if party not in total_party_mandates:
                    total_party_mandates[party] = 0
                total_party_mandates[party] += mandate_count
        for party, adjustment_regions in self.adjustment_mandates_distribution.items():
            if party not in total_party_mandates:
                total_party_mandates[party] = 0
            total_party_mandates[party] += len(adjustment_regions)
        return total_party_mandates

    def calculate_district_vs_regional_differences(self):
        # Calculate the differences between district and regional mandates for each party
        differences = {}
        for party in self.qualifying_parties:
            district_mandates = sum(self.district_mandate_distribution[region].get(party, 0) for region in self.district_mandate_distribution)
            regional_mandates = self.national_mandates.get(party, 0)
            differences[party] = {
                'district_mandates': district_mandates,
                'regional_mandates': regional_mandates,
                'difference': regional_mandates - district_mandates
            }
        return differences

    def print_results(self):
        # Print the total party mandates distribution
        print("\nTotal Party Mandates Distribution:")
        for party, mandates in self.total_party_mandates.items():
            print(f'{party}: {mandates} total mandates')

        print(f"\nTotal mandates distributed: {sum(self.total_party_mandates.values())}")
