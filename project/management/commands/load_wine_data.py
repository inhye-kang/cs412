import pandas as pd
from project.models import LookupWine
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Import wines from CSV for lookup'

    def handle(self, *args, **kwargs):
        csv_file = 'project/data/winedatashort.csv'
        
        data = pd.read_csv(csv_file)
        
        # Strip whitespace from column headers
        data.columns = data.columns.str.strip()
        
        # Strip whitespace from string cells only
        for col in data.select_dtypes(include='object').columns:
            data[col] = data[col].str.strip()

        # Iterate through rows and create LookupWine objects
        for _, row in data.iterrows():
            LookupWine.objects.create(
                wine=row['wine'],
                winery=row['winery'],
                category=row['category'],
                varietal=row['varietal'],
                appellation=row['appellation'],
                alcohol=row['alcohol'],
                price=row['price'],
                rating=row['rating'],
                reviewer=row['reviewer'],
                review=row['review']
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully imported wines into LookupWine.'))
