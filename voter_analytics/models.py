import datetime
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from django.db.models import Q
import csv

class Voter(models.Model):
    last_name = models.TextField(blank=False)
    first_name = models.TextField(blank=False)
    street_num = models.IntegerField(blank=False)
    street_name = models.TextField(blank=False)
    apt_num = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField(blank=False)
    date_of_reg = models.DateField(blank=False)
    party = models.TextField(blank=False)
    precinct_num = models.CharField(max_length=10, blank=False)

    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()

    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Precinct {self.precinct_num}"

    @staticmethod
    def load_data(csv_file_path):
        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert date fields
                date_of_birth = datetime.strptime(row['Date of Birth'], "%Y-%m-%d").date()
                date_of_registration = datetime.strptime(row['Date of Registration'], "%Y-%m-%d").date()
                
                # Convert election participation to boolean
                v20state = row['v20state'] == 'TRUE'
                v21town = row['v21town'] == 'TRUE'
                v21primary = row['v21primary'] == 'TRUE'
                v22general = row['v22general'] == 'TRUE'
                v23town = row['v23town'] == 'TRUE'
                
                # Calculate voter score
                voter_score = sum([v20state, v21town, v21primary, v22general, v23town])
                
                # Create Voter instance
                Voter.objects.create(
                    last_name=row['Last Name'],
                    first_name=row['First Name'],
                    street_num=row['Residential Address - Street Number'],
                    street_name=row['Residential Address - Street Name'],
                    apt_num=row.get('Residential Address - Apartment Number', None),
                    zip_code=row['Residential Address - Zip Code'],
                    date_of_birth=date_of_birth,
                    date_of_reg=date_of_registration,
                    party=row['Party Affiliation'],
                    precinct_num=row['Precinct Number'],  # No integer conversion
                    v20state=v20state,
                    v21town=v21town,
                    v21primary=v21primary,
                    v22general=v22general,
                    v23town=v23town,
                    voter_score=voter_score
                )