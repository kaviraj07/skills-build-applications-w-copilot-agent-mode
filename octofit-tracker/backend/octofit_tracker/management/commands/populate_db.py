from django.core.management.base import BaseCommand
import json
from pathlib import Path
from django.conf import settings
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the database with test data from test_data.json'

    def handle(self, *args, **kwargs):
        # Load test data from JSON file
        test_data_path = Path(__file__).resolve().parent.parent.parent / 'test_data.json'
        
        # Debugging: Print the resolved path for test_data.json
        self.stdout.write(f"Resolved test data path: {test_data_path}")
        
        # Debugging: Print the raw content of the test_data.json file
        with open(test_data_path, 'r', encoding='utf-8') as file:
            raw_content = file.read()
            self.stdout.write(f"Raw content of test_data.json: {raw_content}")
            
            # Debugging: Check file encoding and content length
            self.stdout.write(f"File encoding: {file.encoding}")
            self.stdout.write(f"File content length: {len(raw_content)}")
            
            test_data = json.loads(raw_content)

        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop existing collections
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Populate users
        db.users.insert_many(test_data['users'])

        # Populate teams
        db.teams.insert_many(test_data['teams'])

        # Populate activities
        db.activities.insert_many(test_data['activities'])

        # Populate leaderboard
        db.leaderboard.insert_many(test_data['leaderboard'])

        # Populate workouts
        db.workouts.insert_many(test_data['workouts'])

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
