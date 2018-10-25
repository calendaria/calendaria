from app import app
from app.util import tz_util


def choose_best_lang(request, langs, apikey=app.config['IPSTACK_API_KEY']):
    # First, try to do a best match
    lang = request.accept_languages.best_match(langs)
    if not lang:
        # If that doesn't work, try out "manually"
        lang = choose_lang_from_header(request)
        if not lang:
            # If that doesn't work try out by location
            lang = choose_lang_from_location(api_key=apikey, request=request)
            if not lang:
                # if nothing works, then return english by default
                lang = 'en'
    return lang


def choose_lang_from_location(api_key, request=None, ip=None):
    loc = tz_util.get_location_dict(api_key=api_key, request=request, ip=ip)
    lang = None
    for lan in loc['location']['languages']:
        if 'es' in lan['code']:
            lang = lan['code']
            break
        elif 'en' in lan['code']:
            lang = lan['code']
            break
    return lang


def choose_lang_from_header(request):
    lang = None
    for lan in request.accept_languages.values():
        if 'es' in lan[:2]:
            lang = 'es'
            break
        elif 'en' in lan[:2]:
            lang = 'en'
            break
    return lang

def get_ip(request):
    if request.headers.getlist("X-Forwarded-For"):
	    return request.headers.getlist("X-Forwarded-For")[0]
    else:
        return request.remote_addr