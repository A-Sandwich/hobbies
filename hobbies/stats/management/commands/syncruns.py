from django.core.management.base import BaseCommand, CommandError
from garminconnect import Garmin, GarminConnectConnectionError, GarminConnectTooManyRequestsError, GarminConnectAuthenticationError
from datetime import date
from dateutil import parser
import os
import logging
import json
import time

class Command(BaseCommand):
    help = 'Syncs running data'

    def handle(self, *args, **options):
        print("Running command ☄️")
        client = self.authenticate_with_retry(5)
        activities = self.get_activities(client, 10)
        activityData = ActivityData()
        activityData = self.get_totals(activities, activityData)
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
            print(activities)
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

class ActivityDatum:
    duration = 0
    distance = 0
    calories = 0
    activity_type = ""

    def __init__(self, activity_type):
        self.activity_type = activity_type

    def log(self):
        print("You went", self.get_miles(),"miles while", self.activity_type, "for", self.get_hours(), "hours and burnt", self.calories, "calrories.")
    
    def get_miles(self):
        return self.distance / 1609.344
    
    def get_hours(self):
        return self.duration / 360.0

class ActivityData:
    running = ActivityDatum("running")
    walking = ActivityDatum("walking")
    newest_activity_id = None

    def parse_activity(self, activity, year):
        self.parse_activity_id(activity["activityId"])
        activity_type = activity["activityType"]["typeKey"]
        startTimeLocal = parser.parse(activity["startTimeLocal"])
        if year != startTimeLocal.year:
            return
        parsedActivity = self.get_activity_by_type(activity_type)

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

