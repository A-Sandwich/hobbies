from django.db import models

class ExerciseTotal(models.Model):
    exercise_type = models.CharField(max_length=50)
    duration = models.IntegerField(default=0)
    distance = models.IntegerField(default=0)
    calories = models.IntegerField(default=0)
    year = models.CharField(max_length=4)
    last_activity = models.DateTimeField(null=True)
    
    def __str__(self):
        return("You went " +
        str(round(self.get_miles())) +
        " miles while " +
        self.exercise_type +
        " for " +
        str(round(self.get_hours())) +
        " hours and burnt " +
        str(round(self.calories)) +
        " calrories in the year " +
        self.year)
    
    def get_miles(self):
        return self.distance / 1609.344
    
    def get_hours(self):
        return self.duration / 360.0
