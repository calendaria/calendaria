def choose_best_lang(request, langs):
    return request.accept_languages.best_match(langs)

def get_ip(request):
    if request.headers.getlist("X-Forwarded-For"):
	    return request.headers.getlist("X-Forwarded-For")[0]
    else:
        return request.remote_addr