from django.db import models
from datetime import datetime

class Location(models.TextChoices):
    POP = "Pop"
    NORDIC = "Nordic"
    OTA = "Ota"
    BARRYS = "Barrys"


class Sport(models.TextChoices):
    PADEL = "Padel"
    TENNIS = "Tennis"
    SQUASH = "Squash"
    HIIT = "Hiit"


class SlotRule(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    week_days = models.CharField(
        max_length=20,
        choices=DAYS_OF_WEEK,
        help_text="Day(s) of the week when this rule applies"
    )

    start_time = models.TimeField(help_text="Start time of the rule")
    end_time = models.TimeField(help_text="End time of the rule")

    sport = models.CharField(
        max_length=20,
        choices=Sport.choices,
        help_text="Sport for the rule"
    )

    def __str__(self):
        return f"{self.week_days} {self.start_time} - {self.end_time}"


class Slot(models.Model):
    start_datetime = models.DateTimeField(help_text="Start date and time of the slot")
    end_datetime = models.DateTimeField(help_text="End date and time of the slot")
    sport = models.CharField(
        max_length=20,
        choices=Sport.choices,
        help_text="Sport for the slot"
    )
    is_booked = models.BooleanField(default=False, help_text="Whether the slot is booked")
    location = models.CharField(
        max_length=20,
        choices=Location.choices,
        help_text="Location of the slot"
    )
    slot_rule = models.ForeignKey(SlotRule, on_delete=models.DO_NOTHING, null=True, help_text="Slot rule for the slot")

    def __str__(self):
        return f"{self.start_datetime} - {self.end_datetime} {self.sport} {self.location}"



