from datetime import timedelta, date

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

# Check if the value is inside the Ring of Fire
def rof(indate):
	daynbr_ = daynbr(indate)
	if not is_leap_yr(indate) and daynbr_ > 352:
		return True
	elif is_leap_yr(indate) and daynbr_ > 353:
		return True
	else:
		return False

# Calculate the whole round values for desired round and year
def round_vals(rnd, year):
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
	
	# Initialize the lists to put the different variables
	dates, dates_str, day_nbr, week_nbr, weekday = [], [], [], [], []
	freq_negs, gaps, gap_dates, gap_dates_str = [], [], [], []
	cg_tot_days_, cg_, cg_day_ = [], [], []
	fs_, au_, quads = [], [], []

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

	#Update the dictionary
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
	cal_dict['fs'] = fs_
	cal_dict['au'] = au_
	cal_dict['quads'] = quads
	
	# Return the dictionary
	return cal_dict

# Return the round values for a specific date
def round_vals_from_date(indate):
	rnd = round_nbr(indate)
	yr = indate.year
	
	return round_vals(rnd, yr)


# Values for a particular quadrant given a date
def quadrant_n_vals(indate, quad_n):
	quad = {}
	rnd_vals = round_vals_from_date(indate)
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
def quadrant_vals(indate):
	quads = {}
	for i in range(1, 5):
		quads['q' + str(i)] = quadrant_n_vals(indate, i)

	return quads
	

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
