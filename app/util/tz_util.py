from app.util.web_util import get_ip
import requests
import json
import pytz
from datetime import datetime


def get_location_dict(api_key, request=None, ip=None):
    # Build URL
    if ip == None:
        ip = get_ip(request)
    url_base = 'http://api.ipstack.com/'
    url = url_base + str(ip)
    url += '?access_key=' + api_key
    # Try to make the request and get the response, if not possible
    # return generic UTC time code
    try:
        r = requests.get(url)
    except:
        return {'country_name': None}
    return json.loads(r.text)


def get_tz_str(api_key, request=None, ip=None):
    loc_dict = get_location_dict(api_key=api_key, request=request, ip=ip)
    # If location request didn't go through successfully
    if loc_dict['country_name'] == None:
        return 'Etc/UTC'
    # Handling most common cases (Arg and SF)
    if loc_dict['country_name'].lower() == 'argentina':
        return 'America/Buenos_Aires'
    if loc_dict['country_code'] == 'US' and loc_dict['region_code'] == 'CA':
        return 'America/Los_Angeles'
    # All other cases
    if 'america' in loc_dict['continent_name'].lower():
        loc_dict['continent_name'] = 'America'
    continent = loc_dict['continent_name'].title().replace(' ', '_')
    country = loc_dict['country_name'].title().replace(' ', '_')
    return  continent + '/' + country


def get_tz(api_key, request=None, ip=None):
    tz_str = get_tz_str(api_key=api_key, request=request, ip=ip)
    # Try to return a tz object based on the continent/country code
    # If that doesn't exist, then return standard UTC tz obj
    try:
        return pytz.timezone(tz_str)
    except:
        return pytz.timezone('Etc/UTC')


def set_tz_date(indate, tz):
    if type(tz) == str:
        try:
            tz = pytz.timezone(tz)
        except:
            tz = pytz.timezone('Etc/UTC')
    return indate.astimezone(tz).date()


def set_tz_today(tz):
    if type(tz) == str:
        try:
            tz = pytz.timezone(tz)
        except:
            tz = pytz.timezone('Etc/UTC')
    return datetime.today().astimezone(tz).date()


