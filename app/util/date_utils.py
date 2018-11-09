from datetime import timedelta, date
import math

# Generate a spanish version of the week day names
ES_WEEKDAYS = ["Domingo",
			   "Lunes",
			   "Martes",
			   "Miercoles",
			   "Jueves",
			   "Viernes",
			   "Sabado"]

# Dictionary with steps
STEPS = {
		1: "LO",
		2: "IN",
		3: "HU",
		4: "CO",
		5: "LO",
		6: "IN",
		7: "HU",
		8: "CO",
		9: "LO",
		10: "IN",
		11: "HU",
		12: "CO",
		13: "LO",
		14: "IN",
		15: "HU",
		16: "CO"
}


# Days difference between 2 dates
def day_diff (date1, date2):
	return (date1 - date2).days


# Return the day of the year
def daynbr(indate):
	try:
		return indate.timetuple().tm_yday
	except:
		return "Invalid input"


# Return the week number
def weeknbr(indate):
	if daynbr(indate)%7 == 0:
		return int( (daynbr(indate)/7) )
	else:
		return int( (daynbr(indate)/7) ) + 1


# Return day of the week (int)
def weekday(indate):
	return int( indate.strftime("%w") )


# Round
def round_nbr(indate):
	if daynbr(indate)%16 != 0:
		return int(daynbr(indate)/16) + 1
	else:
		return int(daynbr(indate)/16)


# Round day
def round_day_nbr(indate):
	if daynbr(indate)%16 != 0:
		return int(daynbr(indate)%16)
	else:
		return 16


# Quadrant
def quadrant(indate):
	if daynbr(indate)%4 != 0:
		return int(round_day_nbr(indate)/4) + 1
	else:
		return int(round_day_nbr(indate)/4)


def quadrant_name(indate, lang='es'):
	quad = quadrant(indate)
	quad_names = [
		{'es': 'LOGICO', 'en': 'LOGIC'},
		{'es': 'INHUMANO', 'en': 'INHUMAN'},
		{'es': 'HUMANO', 'en': 'HUMAN'},
		{'es': 'CONTEXTO', 'en': 'CONTEXT'},
	]
	return quad_names[quad-1][lang]


# Step name
def step(indate):
	return STEPS[round_day_nbr(indate)]


# Return day of the week (int) in spanish
def weekday_str_es(indate):
	return ES_WEEKDAYS[weekday(indate)]


# Return day of the week (int) in spanish
def weekday_str(indate):
	return indate.strftime("%A")


# Neg Freq: Day of year - Total nbr of years
def freq_neg(indate):
	diff = date(indate.year, 12, 31) - date(indate.year, 1, 1)
	diff -= timedelta(days=daynbr(indate))
	diff += timedelta(days=1)
	return diff.days


# GAP: Day nbr + Neg Freq
def gap(indate):
	return daynbr(indate) - freq_neg(indate)


# GAP date: Current date- gap
def gap_date(indate):
	return indate - timedelta(days=freq_neg(indate))


# Total days from Global Quarantine: 14 Oct 2014
def cg_tot_days(indate):
	cg_date = date(2012, 10, 14)
	diff = indate - cg_date
	return diff.days


# Calculate the Global Quarantine based on the CG Tot days
def cg(indate):
	return int(cg_tot_days(indate)/39) + 1

# Calculate the Global Quarantine day
def cg_day(indate):
	return cg_tot_days(indate)%39 + 1


# Total days from Personal Quarantine (Default is Dolores)
def cp_tot_days(indate, deriv_date=None):
	if not deriv_date:
		return None
	diff = indate - deriv_date
	return diff.days


# Calculate the Personal Quarantine based on the CP Tot days
def cp(indate, deriv_date=None):
	if not deriv_date:
		return None
	return int(cp_tot_days(indate, deriv_date)/39) + 1


# Calculate the Personal Quarantine day
def cp_day(indate, deriv_date=None):
	if not deriv_date:
		return None
	return cp_tot_days(indate, deriv_date)%39 + 1


# Total days from Fifth Stage date: 28 Aug 2016
def fs(indate):
	fs_date = date(2016, 8, 28)
	diff = indate - fs_date
	return diff.days

# Total days from AU date: 26 Aug 2017
def au(indate):
	au_date = date(2017, 8, 26)
	diff = indate - au_date
	return diff.days


# Calculate the days alive from certain date
def days_alive(indate, bday):
	diff = indate - bday
	return diff.days


# Check for if its a leap year
def is_leap_yr(indate):
	if isinstance(indate, date):
		year = indate.year
		return (( year%400 == 0) or (( year%4 == 0 ) and ( year%100 != 0)))
	else:
		year = indate
		return (( year%400 == 0) or (( year%4 == 0 ) and ( year%100 != 0)))


# Calculate the apparatus nbr
def apparatus_nbr(indate):
	return math.ceil(indate.year/4)


# Calculate the apparatus offset
def apparatus_offset(indate):
	return indate.year/4 - int(indate.year/4)


# Calculate the apparatus type based on the offset
def apparatus_type(indate):
	off = apparatus_offset(indate)
	if off == 0.0:
		return ('B', 'DECIDE')
	elif off == 0.25:
		return ('CT1', 'ASUME')
	elif off == 0.5:
		return ('CT2', 'ASIMILA')
	elif off == 0.75:
		return ('CT3', 'DESAFIA')
	else:
		raise ValueError('Offset values can only be 0, 0.25, 0.5, 0.75')


# Calculate apparatus f+
def apparatus_fplus(indate):
	off = apparatus_offset(indate)
	if off == 0.0:
		return 365*3 + daynbr(indate)
	elif off == 0.25:
		return daynbr(indate)
	elif off == 0.5:
		return 365 + daynbr(indate)
	elif off == 0.75:
		return 365*2 + daynbr(indate)


# Calculate apparatus f- based on f+
def apparatus_fneg(indate):
	return 1461 - apparatus_fplus(indate)


# Apparatus matrix (previous and next f+ and f- for all apparatus years)
def apparatus_matrix(indate):
	app_matrix = []
	off = apparatus_offset(indate)
	yr = indate.year
	if off == 0.25:
		yrs = [0, 1, 2, 3]
	elif off == 0.5:
		yrs = [-1, 0, 1, 2]
	elif off == 0.75:
		yrs = [-2, -1, 0, 1]
	elif off == 0.0:
		yrs = [-3, -2, -1, yr]
	for y in yrs:
		d = date(indate.year+y, indate.month, indate.day)
		app_matrix.append([apparatus_fplus(d)] + [apparatus_fneg(d)] + [d.year])
	return app_matrix


# Lived apparatus
def apparatus_lived(indate, bday):
	diff = indate.year - bday.year
	return math.ceil(diff/4)


# Check if the value is inside the Ring of Fire
def rof(indate):
	daynbr_ = daynbr(indate)
	if not is_leap_yr(indate) and daynbr_ > 352:
		return True
	elif is_leap_yr(indate) and daynbr_ > 353:
		return True
	else:
		return False


def rof_days(yr):
	d = date(yr, 1, 1)
	rof_days = []
	if is_leap_yr(d):
		for i in range(354, 367):
			rof_days += [(i, daynbr_to_date(i, yr))]
	else:
		for i in range(353, 366):
			rof_days += [(i, daynbr_to_date(i, yr))]
	return rof_days


# Calculate the whole round values for desired round and year
def round_vals(rnd, year, deriv_date=None, dob=None):
	'''
	We are going to calculate all the values for the round inside a dictionary.
	Each entry of the dictionary will have an array of length 16,
	corresponding to each round day
	'''
	# Create an empty dictionary and put the values that dont vary
	# across different rounds
	cal_dict = {}
	cal_dict['round_days'] = [i for i in range(1, 17)]
	cal_dict['steps'] = [STEPS[i] for i in range(1, 17)]
	cal_dict['round'] = [rnd for i in range(1, 17)]

	if not deriv_date:
		cp_tot_days_ = ['N/A']*16
		cp_ = ['N/A']*16
		cp_day_ = ['N/A']*16
	else:
		cp_tot_days_, cp_, cp_day_ = [], [], []

	if dob:
		days_lived, fp_nat, fn_nat, gap_nat, ftp, ftn = [], [], [], [], [], []
	else:
		days_lived = ['N/A']*16
		fp_nat = ['N/A']*16
		fn_nat = ['N/A']*16
		gap_nat = ['N/A']*16
		ftp = ['N/A']*16
		ftn = ['N/A']*16

	# Initialize the lists to put the different variables
	dates, dates_str, day_nbr, week_nbr, weekday = [], [], [], [], []
	freq_negs, gaps, gap_dates, gap_dates_str = [], [], [], []
	cg_tot_days_, cg_, cg_day_ = [], [], []
	fs_, au_, quads, quad_names_es = [], [], [], []
	af, aff  = [], []

	# Loop and check for the desired round
	init = date(year, 1, 1)
	for d in range(0, 365):
		curr_date = init + timedelta(days=d)
		# Get the date so that it works in spanish as well
		curr_day = curr_date.strftime("%d")
		curr_month = curr_date.strftime("%b")[:3].capitalize()
		curr_year = curr_date.strftime("%Y")
		# Capture the values for the current date
		if round_nbr(curr_date) == rnd:
			dates += [curr_date]
			dates_str += [curr_day + "-" + curr_month + "-" + curr_year]
			day_nbr += [daynbr(curr_date)]
			week_nbr += [weeknbr(curr_date)]
			weekday += [weekday_str(curr_date)]
			freq_negs += [freq_neg(curr_date)]
			gaps += [gap(curr_date)]
			# Need to get right the GAP dates for spanish
			gap_dates += [gap_date(curr_date)]
			gap_day = gap_date(curr_date).strftime("%d")
			gap_month = gap_date(curr_date).strftime("%b")[:3].capitalize()
			gap_year = gap_date(curr_date).strftime("%Y")
			gap_dates_str += [gap_day + "-" + gap_month + "-" + gap_year]
			cg_tot_days_ += [cg_tot_days(curr_date)]
			cg_ += [cg(curr_date)]
			cg_day_ += [cg_day(curr_date)]
			fs_ += [fs(curr_date)]
			au_ += [au(curr_date)]
			quads += [quadrant(curr_date)]
			quad_names_es += [quadrant_name(curr_date)]
			af += [daynbr(curr_date) + 4667]
			aff += [daynbr(curr_date) + 7664]
			if deriv_date:
				cp_tot_days_ += [cp_tot_days(curr_date, deriv_date)]
				cp_ += [cp(curr_date, deriv_date)]
				cp_day_ += [cp_day(curr_date, deriv_date)]
			if dob:
				days_lived += [days_alive(curr_date, dob)]
				fp_nat += [daynbr(dob)]
				fn_nat += [freq_neg(dob)]
				gap_nat += [daynbr(dob)-freq_neg(dob)]
				ftp += [daynbr(curr_date) + daynbr(dob)]
				ftn += [freq_neg(curr_date) + freq_neg(dob)]

	# Update the dictionary
	cal_dict['dates'] = dates
	cal_dict['dates_str'] = dates_str
	cal_dict['day_nbr'] = day_nbr
	cal_dict['week_nbr'] = week_nbr
	cal_dict['weekday'] = weekday
	cal_dict['freq_neg'] = freq_negs
	cal_dict['gap'] = gaps
	cal_dict['gap_date'] = gap_dates
	cal_dict['gap_date_str'] = gap_dates_str
	cal_dict['cg_tot_days'] = cg_tot_days_
	cal_dict['cg'] = cg_
	cal_dict['cg_day'] = cg_day_
	cal_dict['cp_tot_days'] = cp_tot_days_
	cal_dict['cp'] = cp_
	cal_dict['cp_day'] = cp_day_
	cal_dict['fs'] = fs_
	cal_dict['au'] = au_
	cal_dict['quads'] = quads
	cal_dict['quad_name_es'] = quad_names_es
	cal_dict['af'] = af
	cal_dict['aff'] = aff
	cal_dict['days_lived'] = days_lived
	cal_dict['fp_nat'] = fp_nat
	cal_dict['fn_nat'] = fn_nat
	cal_dict['gap_nat'] = gap_nat
	cal_dict['ftp'] = ftp
	cal_dict['ftn'] = ftn
	# Return the dictionary
	return cal_dict


# Return the round values for a specific date
def round_vals_from_date(indate, deriv_date=None, dob=None):
	rnd = round_nbr(indate)
	yr = indate.year

	return round_vals(rnd, yr, deriv_date, dob)


# Values for a particular quadrant given a date
def quadrant_n_vals(indate, quad_n, deriv_date=None, dob=None):
	quad = {}
	rnd_vals = round_vals_from_date(indate, deriv_date, dob)
	quad_n = int(quad_n)

	# Define the values to pull from dictionary lists
	if quad_n == 1:
		mini, maxi = 0, 4
	elif quad_n == 2:
		mini, maxi = 4, 8
	elif quad_n == 3:
		mini, maxi = 8, 12
	elif quad_n == 4:
		mini, maxi = 12, 16
	else:
		raise ValueError('Invalid Quadrant number. Should be an int from 1 to 4.')

	# Loop through the round vals and extract the quadrant
	for key in rnd_vals.keys():
		vals = rnd_vals[key][mini:maxi]
		quad[key] = vals

	# Return the quadrant dict
	return quad


# Calculate the value of all the quadrants given a date
def quadrant_vals(indate, deriv_date=None, dob=None):
	quads = {}
	for i in range(1, 5):
		quads['q' + str(i)] = quadrant_n_vals(indate, i, deriv_date, dob)

	return quads


# Create calendar (daynbrs) to display in Calendar page
def create_daynbr_grid(year, from_round=1, to_round=11):
	calendar = []
	# Create a structure with the correct day nbrs in order
	for i in range(to_round, from_round-1, -1):
		rnd = round_vals(i, 2018)
		calendar.append([i] + rnd['day_nbr'][8:12] + rnd['day_nbr'][4:8])
	for i in range(from_round, to_round+1):
		rnd = round_vals(i, 2018)
		calendar.append([i] + rnd['day_nbr'][:4] + rnd['day_nbr'][12:16])
	return calendar


# Create calendar (dates) to display in Calendar page
def create_calendar(year, from_round=1, to_round=11):
	cal = create_daynbr_grid(year=year, from_round=from_round, to_round=to_round)
	for row in cal:
		for i in range(len(row)):
			if i == 0:
				continue
			else:
				row[i] = daynbr_to_date(row[i], year)
	return cal


# Transform daynbr to date
def daynbr_to_date(daynbr, year):
	return (date(year, 1, 1) + timedelta(days=daynbr-1))


def date_vals(indate, deriv_date=None, dob=None):
	date_vals = {}
	date_vals['date'] = indate
	date_vals['quad_name_es'] = quadrant_name(indate)
	date_vals['step'] = step(indate)
	date_vals['round'] = round_nbr(indate)
	date_vals['quad'] = quadrant(indate)
	date_vals['round_day'] = round_day_nbr(indate)
	date_vals['day_nbr'] = daynbr(indate)
	date_vals['week_nbr'] = weeknbr(indate)
	date_vals['weekday'] = weekday_str(indate).capitalize()
	date_vals['freq_neg'] = freq_neg(indate)
	date_vals['gap_date'] = gap_date(indate)
	date_vals['gap'] = gap(indate)
	date_vals['fs'] = fs(indate)
	date_vals['au'] = au(indate)
	date_vals['cg'] = cg(indate)
	date_vals['cg_day'] = cg_day(indate)
	date_vals['cg_tot_days'] = cg_tot_days(indate)
	date_vals['is_rof'] = rof(date_vals['date'])
	if deriv_date:
		date_vals['cp_tot_days'] = cp_tot_days(indate, deriv_date)
		date_vals['cp'] = cp(indate, deriv_date)
		date_vals['cp_day'] = cp_day(indate, deriv_date)
	date_vals['app_nbr'] = apparatus_nbr(indate)
	date_vals['app_type'] = apparatus_type(indate)
	date_vals['app_offset'] = apparatus_offset(indate)
	date_vals['app_fp'] = apparatus_fplus(indate)
	date_vals['app_fn'] = apparatus_fneg(indate)
	date_vals['af'] = 4667 + daynbr(indate)
	date_vals['aff'] = 7664 + daynbr(indate)
	date_vals['app_matrix'] = apparatus_matrix(date_vals['date'])
	if dob:
		date_vals['days_alive'] = day_diff(date_vals['date'], dob)
		date_vals['app_nat_nbr'] = apparatus_nbr(dob)
		date_vals['app_nat_type'] = apparatus_type(dob)
		date_vals['app_nat_offset'] = apparatus_offset(dob)
		date_vals['app_nat_lived'] = apparatus_lived(date_vals['date'], dob)
		date_vals['fp_nat'] = daynbr(dob)
		date_vals['fn_nat'] = freq_neg(dob)
		date_vals['gap_nat'] = date_vals['fp_nat'] - date_vals['fn_nat']
		date_vals['ftp'] = date_vals['day_nbr'] + date_vals['fp_nat']
		date_vals['ftn'] = date_vals['freq_neg'] + date_vals['fn_nat']
	return date_vals


# Test Function
def testing(indate, n=1):
	for i in range(n):
		d = indate + timedelta(days=i)
		print("Date:", d, "|",
			  "DoY:", daynbr(d), "|",
			  "Rnd:", round_nbr(d), "|",
			  "Rnd Day:", round_day_nbr(d), "|",
			  "Step:", step(d), "|",
			  "Quadrant:", quadrant(d)
		)
