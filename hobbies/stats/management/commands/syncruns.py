from django.core.management.base import BaseCommand, CommandError
from garminconnect import Garmin, GarminConnectConnectionError, GarminConnectTooManyRequestsError, GarminConnectAuthenticationError
from datetime import date, tzinfo
from dateutil import parser
import os
import logging
import json
import time
from stats.models import ExerciseTotal

class Command(BaseCommand):
    help = 'Syncs running data'

    def handle(self, *args, **options):
        print("Running command ☄️")
        client = self.authenticate_with_retry(5)
        activities = self.get_activities(client, 300)
        activityData = self.load_from_db()
        activityData = self.get_totals(activities, activityData)
        activityData.save()
        activityData.log()
        print("Exiting")
    
    def authenticate_with_retry(self, retryLimit):
        retries = 0
        client = self.authenticate_garmin()
        while not client and retries <= retryLimit:
            time.sleep(0.5)
            retries += 1
            print("retrying attampt", retries)
            client = self.authenticate_garmin()
        return client
    
    def get_totals(self, activities, activityData):
        activities.reverse()
        current_year = date.today().year
        for activity in activities:
            activityData.parse_activity(activity, current_year)

        return activityData
    
    def authenticate_garmin(self):
        print("Authenticating...")
        email = os.environ.get('GARMIN_EMAIL')
        password = os.environ.get('GARMIN_PASSWORD')
        try:
            client = Garmin(email, password)
            client.login()
            return client
        except (
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError,
        ) as err:
            print("Error occurred during Garmin Connect Client init or login: %s" % err)
        except Exception:  # pylint: disable=broad-except
            print("Unknown error occurred during Garmin Connect Client init or login")
        return None

    def get_activities(self, client, limit):
        try:
            activities = client.get_activities(0,limit) # 0=start, 1=limit
            return activities
        except (
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError,
        ) as err:
            print("Error occurred during Garmin Connect Client get activities: %s" % err)
            quit()
        except Exception:  # pylint: disable=broad-except
            print("Unknown error occurred during Garmin Connect Client get activities")
            quit()

    def load_from_db(self):
        running_datum, _ = ExerciseTotal.objects.get_or_create(
            year = str(date.today().year),
            exercise_type = "running",
            defaults={
                "year": str(date.today().year),
                "exercise_type": "running"
            },
        )
        walking_datum, _ = ExerciseTotal.objects.get_or_create(
            year = str(date.today().year),
            exercise_type = "walking",
            defaults={
                "year": str(date.today().year),
                "exercise_type": "walking"
            },
        )

        return ActivityData(running_datum, walking_datum)

class ActivityData:
    running = None
    walking = None
    newest_activity_id = None

    def __init__(self, running_datum, walking_datum):
        self.running = running_datum
        self.walking = walking_datum

    def parse_activity(self, activity, year):
        self.parse_activity_id(activity["activityId"])
        activity_type = activity["activityType"]["typeKey"]
        startTimeLocal = parser.parse(activity["startTimeLocal"])
        if year != startTimeLocal.year:
            return
        parsedActivity = self.get_activity_by_type(activity_type)

        if not parsedActivity: # we return None if the activity is not a run or a walk
            return

        print(activity["startTimeLocal"])
        if not parsedActivity.last_activity or parsedActivity.last_activity.replace(tzinfo=None) < parser.parse(activity["startTimeLocal"]):
            parsedActivity.last_activity = parser.parse(activity["startTimeLocal"])
            parsedActivity.distance += activity["distance"]
            parsedActivity.calories += activity["calories"]
            parsedActivity.duration += activity["duration"]

        
    
    def get_activity_by_type(self, activity_type):
        if activity_type == "running":
            return self.running
        if activity_type == "walking":
            return self.walking
        return None
    
    def parse_activity_id(self, activity_id):
        if not self.newest_activity_id:
            self.newest_activity_id = activity_id

    def log(self):
        self.running.log()
        self.walking.log()
    
    def save(self):
        self.running.save()
        self.walking.save()


