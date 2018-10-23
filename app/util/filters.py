from datetime import datetime


def nth(n):
	n = str(n)
	if (n[-1]=='1'):
	    if (n=='11'):
	        return n + "th"
	    return n + "st"
	elif (n[-1]=='2'):
	    if (n=='12'):
	        return n + "th"
	    return n + "nd"
	elif (n[-1]=='3'):
	    if (n=='13'):
	        return n + "th"
	    return n + "rd"
	else:
		return n + "th"


def to_date(str_date):
	return datetime.today()