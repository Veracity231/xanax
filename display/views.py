from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from json import loads
from requests import get, exceptions
from .models import Member, Data, Faction
from time import sleep

def index(request):
    return render(request, 'display/index.html', {'staff': request.user.is_staff and request.user.is_active})


def logout_user(request):
    logout(request)
    return render(request, 'display/index.html', {'staff': request.user.is_staff and request.user.is_active})


def login_screen(request):
    return render(request, 'display/login.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'display/index.html', {'staff': request.user.is_staff and request.user.is_active})
            else:
                return render(request, 'display/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'display/login.html', {'error_message': 'Invalid login'})
    return render(request, 'display/login.html')


def fill_context(json_object):
    try:
        db_member = get_object_or_404(Member, member_id=int(json_object['player_id']))
        db_data = Data.objects.filter(member_id=int(json_object['player_id']))
        db_faction = get_object_or_404(Faction, faction_id=int(db_member.faction_id))
    except:
        db_member = 'Not Found'
        db_data = None
        db_faction = None

    return {'member': db_member, 'faction': db_faction, 'data': db_data}


def check_api(request):
    if request.method == "POST":
        apikey = request.POST['apikey']
        if len(apikey) == 8:
            error_message = None
            try:
                profile_url = 'https://api.torn.com/user/?selections=profile&key=%s' % (apikey)
                profile_json = loads(get(profile_url).text)
            except exceptions.RequestException as e:
                error_message = str(e)
            if not error_message:
                try:
                    context = fill_context(profile_json)
                    context.update({'staff': request.user.is_staff and request.user.is_active, 'apikey': str(apikey)})
                    return render(request, 'display/index.html', context)
                except:
                    error_message = profile_json['error']['error']
            return render(request, 'display/index.html', {'error_message': error_message,
                                                          'staff': request.user.is_staff and request.user.is_active,
                                                          })
        else:
            return render(request, 'display/index.html', {'error_message': 'Not an API key',
                                                          'staff': request.user.is_staff and request.user.is_active,
                                                          })
    else:
        return render(request, 'display/index.html', {'staff': request.user.is_staff and request.user.is_active})


def all_members(json_object):
    db_member = Member.objects.all().order_by('member_id').order_by('faction_id')
    db_faction = Faction.objects.all().order_by('faction_id')
    db_data = None
    return {'member': db_member, 'faction': db_faction, 'data': db_data}


def show_all_members(request):
    if request.method == "POST":
        apikey = request.POST['apikey']
        if len(apikey) == 8:
            error_message = None
            try:
                profile_url = 'https://api.torn.com/user/?selections=profile&key=%s' % (apikey)
                profile_json = loads(get(profile_url).text)
            except exceptions.RequestException as e:
                error_message = str(e)
            if not error_message:
                try:
                    context = all_members(profile_json)
                    context.update({'staff': request.user.is_staff and request.user.is_active, 'apikey': str(apikey)})
#                    populater()
                    return render(request, 'display/all_members.html', context)
                except:
                    error_message = profile_json['error']['error']
            return render(request, 'display/index.html', {'error_message': error_message,
                                                          'staff': request.user.is_staff and request.user.is_active,
                                                          })
        else:
            return render(request, 'display/index.html', {'error_message': 'Not an API key',
                                                          'staff': request.user.is_staff and request.user.is_active,
                                                          })
    else:
        return render(request, 'display/index.html', {'staff': request.user.is_staff and request.user.is_active})

