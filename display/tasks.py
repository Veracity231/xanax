# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from json import loads
from requests import get
from .models import Member, Data, Faction
from time import sleep
import os

@shared_task
def add(x, y):
    return x + y


@shared_task
def populater():
    apikey = str(os.environ.get('XAN_APIKEY'))
    for this_faction in Faction.objects.all():
        faction_url = 'https://api.torn.com/faction/%s?selections=basic&key=%s' % (str(this_faction.faction_id), apikey)
        json_faction = loads(get(faction_url).text)
        this_faction.name = json_faction['name']
        this_faction.save()
        json_members = json_faction['members']
        for m in json_members:
            profile_url = 'https://api.torn.com/user/%s?selections=profile&key=%s' % (str(m), apikey)
            json_profile = loads(get(profile_url).text)
            try:
                this_member = Member.objects.get(member_id=int(m))
            except:
                this_member = Member()
                this_member.member_id = int(m)
            this_member.name = json_profile['name']
            this_member.age = int(json_profile['age'])
            this_member.level = int(json_profile['level'])
            this_member.faction_id = int(json_profile['faction']['faction_id'])
            this_member.days_in_faction = int(json_profile['faction']['days_in_faction'])
            print(this_member.name)
            this_member.save()

            bars_url = 'https://api.torn.com/user/?selections=bars&key=%s' % apikey
            json_bars = loads(get(bars_url).text)
            personalstats_url = 'https://api.torn.com/user/%s?selections=personalstats&key=%s' % (str(m), apikey)
            json_personalstats = loads(get(personalstats_url).text)['personalstats']
            d = Data()
            d.member_id = int(m)
            d.timestamp = int(json_bars['server_time'])
            try:
                d.xanax_used = int(json_personalstats['xantaken'])
            except KeyError:
                d.xanax_used = 0
            try:
                d.overdosed = int(json_personalstats['overdosed'])
            except KeyError:
                d.overdosed = 0
            d.save()
            sleep(2.0)

