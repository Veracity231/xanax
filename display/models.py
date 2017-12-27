from django.db import models
from time import gmtime, strftime


class Faction(models.Model):
    faction_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Member(models.Model):
    member_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    level = models.IntegerField()
    faction_id = models.IntegerField()
    days_in_faction = models.IntegerField()

    def __str__(self):
        return self.name


class Data(models.Model):
    member_id = models.IntegerField()
    timestamp = models.IntegerField()
    xanax_used = models.IntegerField()
    overdosed = models.IntegerField()

    def __str__(self):
        return strftime("%Y-%m-%d %H:%M:%S", gmtime(self.timestamp))


