from app import app, db, moment
from app.models import User
from flask import (render_template, flash, redirect, url_for,
    request, make_response, session)
from app.forms import (LoginForm, LoginESForm, RegistrationForm,
    RegistrationESForm, UpdateProfileForm,
	UpdateProfileESForm, ResetPasswordForm, ResetPasswordESForm,
	ResetPasswordRequestForm, ResetPasswordRequestESForm)
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.util import date_utils
from app.email import send_password_reset_email, sendgrid_password_reset_email
from datetime import datetime, timedelta, date
from flask_babel import get_locale
import locale
from tzlocal import get_localzone
from app.util.tz_util import (get_location_dict, get_tz_str,
    get_tz, set_tz_date, set_tz_today)
from app.util.web_util import choose_best_lang
from app.util import export_utils
import pyexcel as pe
import requests
import json


# Define Locale keys for the server
EN_LC = 'en_US'
ES_LC = 'es_ES'

# API Keys and languages, only spanish and english supported
SUP_LANGUAGES = app.config['LANGUAGES']
IPSTACK_API_KEY = app.config['IPSTACK_API_KEY']


# Entry point is the calendar now
@app.route('/')
@app.route('/es')
@app.route('/index')
@app.route('/es/index')
@login_required
def index():
	# Get user's local time by using IPstack API
	tz = get_tz(IPSTACK_API_KEY, request=request)
	# Set the locale based on language to display the right language for dates
	locale.setlocale(locale.LC_TIME, ES_LC)
	calendar = {}
	calendar['today'] = set_tz_today(tz)
	calendar['year'] = datetime.today().year
	calendar['round'] = date_utils.round_nbr(calendar['today'])
	calendar['step'] = date_utils.step(calendar['today'])
	calendar['quad_name_es'] =  date_utils.quadrant_name(calendar['today'])
	calendar['days_alive'] = date_utils.day_diff(calendar['today'],
	    current_user.dob.date())
	calendar['rnd_1_11'] = date_utils.create_calendar(calendar['year'])
	calendar['rnd_12_22'] = date_utils.create_calendar(calendar['year'], from_round=12, to_round=22)
	return render_template('es/calendar.html', calendar=calendar)


@app.route('/es/date/<int:year>/<int:daynbr>')
@login_required
def date_details(year, daynbr):
	# Set the locale
	locale.setlocale(locale.LC_TIME, ES_LC)
	d = date_utils.daynbr_to_date(daynbr, year)
	dates = date_utils.date_vals(d, deriv_date=current_user.deriv_date.date())
	dates['days_alive'] = date_utils.day_diff(dates['date'], current_user.dob.date())
	return render_template('es/date_details.html', dates=dates)


# Calendar view
@app.route('/quadrant/<int:year>/<int:daynbr>')
@login_required
def quadrant(year, daynbr):
    # Get/Set user's local language
	# lang = choose_best_lang(request, SUP_LANGUAGES)
	lang = 'es'
	if 'es' in lang.lower():
		return redirect(url_for('quadrant_es', year=year, daynbr=daynbr))
	# Get user's local time by using IPstack API
	tz = get_tz(IPSTACK_API_KEY, request=request)
	# Set the locale based on language to display the right language for dates
	locale.setlocale(locale.LC_TIME, EN_LC)
	# Save all dates info in dict
	dates = {}
	dates['today'] = set_tz_today(tz)
	dates['days_alive'] = date_utils.day_diff(dates['today'],
	    current_user.dob.date())
	dates['round'] = date_utils.round_nbr(dates['today'])
	dates['quad'] = date_utils.quadrant(dates['today'])
	dates['daynbr'] = date_utils.daynbr(dates['today'])
	dates['is_rof'] = date_utils.rof(dates['today'])
	# Quadrant grid
	grid = date_utils.round_vals_from_date(dates['today'])
	# Set title
	title = current_user.first_name + " Home"
	# Save date in session for export
	session['date_str'] = dates['today'].strftime('%d-%b-%Y')
	return render_template('index.html', title=title, dates=dates, grid=grid)


# Spanish index
@app.route('/es/quadrant/<int:year>/<int:daynbr>')
@login_required
def quadrant_es(year, daynbr):
    # Get/Set user's local language
	# lang = choose_best_lang(request, SUP_LANGUAGES)
	lang = 'es'
	if 'en' in lang.lower():
		return redirect(url_for('quadrant'))
	# Get user's local time by using IPstack API
	tz = get_tz(IPSTACK_API_KEY, request=request)
	# Set the locale based on language to display the right language for dates
	locale.setlocale(locale.LC_TIME, ES_LC)
	# Save all dates info to display in dict
	dates = {}
	dates['date'] = date_utils.daynbr_to_date(daynbr, year)
	dates['days_alive'] = date_utils.day_diff(dates['date'],
	    current_user.dob.date())
	dates['round'] = date_utils.round_nbr(dates['date'])
	dates['quad'] = date_utils.quadrant(dates['date'])
	dates['daynbr'] = date_utils.daynbr(dates['date'])
	dates['quad_name_es'] = date_utils.quadrant_name(dates['date'])
	dates['step'] = date_utils.step(dates['date'])
	dates['is_rof'] = date_utils.rof(dates['date'])
	# Quadrant grid
	if current_user.deriv_date:
	    grid = date_utils.round_vals_from_date(dates['date'],
	    	current_user.deriv_date.date())
	    session['deriv_date'] = current_user.deriv_date.strftime('%d-%b-%Y')
	else:
	    grid = date_utils.round_vals_from_date(dates['date'])
	    session['deriv_date'] = ''
	# Set title
	title = current_user.first_name + " Home"
	# Save date in session for export
	session['date_str'] = dates['date'].strftime('%d-%b-%Y')
	return render_template('es/index.html', title=title, dates=dates, grid=grid)


# Login to the website
@app.route('/login', methods=['GET', 'POST'])
def login():
	# lang = choose_best_lang(request, SUP_LANGUAGES)
	lang = 'es'
	if 'es' in lang.lower():
		return redirect(url_for('login_es'))
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password. Please try again')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title="Login", form=form)


# Login to the website in spanish
@app.route('/es/login', methods=['GET', 'POST'])
def login_es():
	# lang = choose_best_lang(request, SUP_LANGUAGES)
	lang = 'es'
	if 'en' in lang.lower():
		return redirect(url_for('login'))
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginESForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Email o contrasena invalidos. Por favor intente de nuevo')
			return redirect(url_for('login_es'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('es/login.html', title="Ingresar", form=form)


# Register a new user
@app.route('/register', methods=['GET', 'POST'])
def register():
	# lang = choose_best_lang(request, SUP_LANGUAGES)
	lang = 'es'
	if 'es' in lang.lower():
		return redirect(url_for('register_es'))
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		new_user = User(email=form.email.data, first_name=form.first_name.data, dob=form.dob.data)
		new_user.set_password(form.password.data)
		db.session.add(new_user)
		db.session.commit()
		flash('Registration successfull! You can now log in')
		return redirect(url_for('login'))
	return render_template('register.html', title="Registration", form=form)


# Register a new user spanish
@app.route('/es/register', methods=['GET', 'POST'])
def register_es():
	# lang = choose_best_lang(request, SUP_LANGUAGES)
	lang = 'es'
	if 'en' in lang.lower():
		return redirect(url_for('register'))
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationESForm()
	if form.validate_on_submit():
		new_user = User(email=form.email.data, 
						first_name=form.first_name.data, 
						dob=form.dob.data,
						deriv_date=form.deriv_date.data)
		new_user.set_password(form.password.data)
		db.session.add(new_user)
		db.session.commit()
		flash('Ud. ha sido registrado correctamente.')
		return redirect(url_for('login'))
	return render_template('es/register.html', title="Crear nueva cuenta", form=form)


# Profile view
@app.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
	# lang = choose_best_lang(request, SUP_LANGUAGES)
	lang = 'es'
	if 'es' in lang.lower():
		return redirect(url_for('profile_es', user_id=current_user.id))
	title = current_user.first_name.capitalize() + " Profile"
	user = User.query.get(user_id)
	return render_template('profile.html', title=title, user=user)


# Profile view spanish
@app.route('/es/profile/<int:user_id>')
@login_required
def profile_es(user_id):
	# lang = choose_best_lang(request, SUP_LANGUAGES)
	lang = 'es'
	if 'en' in lang.lower():
		return redirect(url_for('profile', user_id=current_user.id))
	title = current_user.first_name.capitalize() + " Perfil"
	user = User.query.get(user_id)
	return render_template('es/profile.html', title=title, user=user)



# Update profile
@app.route('/profile/update/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update(user_id):
	# lang = choose_best_lang(request, SUP_LANGUAGES)
	lang = 'es'
	if 'es' in lang.lower():
		return redirect(url_for('profile_es', user_id=current_user.id))
	title = current_user.first_name + "Update Profile"
	form = UpdateProfileForm()
	if form.validate_on_submit():
		current_user.first_name = form.first_name.data
		current_user.email = form.email.data
		current_user.dob = form.dob.data
		db.session.commit()
		return redirect(url_for('profile', user_id=current_user.id))
	return render_template('update.html', title=title, form=form)


# Update profile spanish
@app.route('/es/profile/update/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update_es(user_id):
	# lang = choose_best_lang(request, SUP_LANGUAGES)
	lang = 'es'
	if 'en' in lang.lower():
		return redirect(url_for('profile', user_id=current_user.id))
	title = current_user.first_name + "Actualizar Perfil"
	form = UpdateProfileESForm()
	if form.validate_on_submit():
		current_user.first_name = form.first_name.data
		current_user.email = form.email.data
		current_user.dob = form.dob.data
		current_user.deriv_date = form.deriv_date.data
		db.session.commit()
		return redirect(url_for('profile', user_id=current_user.id))
	return render_template('es/update.html', title=title, form=form)


# Log users out by re-directing them to Login
@app.route('/logout')
def logout():
	logout_user()
	lang = choose_best_lang(request, SUP_LANGUAGES)
	if 'en' in lang.lower():
		flash('You have been successfully logged out.')
	else:
		flash('Ud. ha terminado la sesion.')
	return redirect(url_for('login'))


# Password change (required data)
@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
	# if current_user.is_authenticated:
	# 	return redirect(url_for('index'))
	lang = choose_best_lang(request, SUP_LANGUAGES)
	if 'es' in lang.lower():
		return redirect(url_for('reset_password_request_es'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			sendgrid_password_reset_email(user, lang)
		flash('Check your email for the instructions to reset your password')
		return redirect(url_for('login'))
	return render_template('reset_password_request.html', title='Reset Password', form=form)


# Password change (required data)
@app.route('/es/reset_password_request', methods=['GET', 'POST'])
def reset_password_request_es():
	# if current_user.is_authenticated:
	# 	return redirect(url_for('index'))
	lang = choose_best_lang(request, SUP_LANGUAGES)
	if 'en' in lang.lower():
		return redirect(url_for('reset_password_request'))
	form = ResetPasswordRequestESForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			sendgrid_password_reset_email(user, lang)
		flash('Se han enviado instrucciones a su correo para actualizar la contrasena.')
		return redirect(url_for('login'))
	return render_template('es/reset_password_request.html', title='Actualizar Contrasena', form=form)


# Reset password view
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
	# if current_user.is_authenticated:
	#	return redirect(url_for('index'))
	user = User.verify_reset_password_token(token)
	if not user:
		return redirect(url_for('index'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash('Your password has been reset.')
		return redirect(url_for('login'))
	return render_template('reset_password.html', form=form)


# Reset password view
@app.route('/es/reset_password/<token>', methods=['GET', 'POST'])
def reset_password_es(token):
	# if current_user.is_authenticated:
	#	return redirect(url_for('index'))
	user = User.verify_reset_password_token(token)
	if not user:
		return redirect(url_for('index'))
	form = ResetPasswordESForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash('Su contrasena ha sido actualizada.')
		return redirect(url_for('login'))
	return render_template('es/reset_password.html', form=form)


# Reset password from profile
@app.route('/reset_password_from_profile', methods=['GET', 'POST'])
@login_required
def reset_password_from_profile():
	form = ResetPasswordForm()
	if form.validate_on_submit():
		current_user.set_password(form.password.data)
		db.session.commit()
		flash('Your password has been reset.')
		return redirect(url_for('login'))
	return render_template('reset_password.html', form=form)


# Reset password from profile
@app.route('/es/reset_password_from_profile', methods=['GET', 'POST'])
@login_required
def reset_password_from_profile_es():
	form = ResetPasswordESForm()
	if form.validate_on_submit():
		current_user.set_password(form.password.data)
		db.session.commit()
		flash('Su contrasena ha sido modificada.')
		return redirect(url_for('login'))
	return render_template('es/reset_password.html', form=form)


@app.route('/download_csv')
def download_csv():
    # Figure out language to export
    lang = choose_best_lang(request, SUP_LANGUAGES)
    # There's a bug in this and sometimes lang come out as None (need to fix)
    if not lang:
        lang = 'en'
    elif 'es' in lang.lower():
        lang = 'es'
    else:
        lang = 'en'
    # Create the data for export based on the date of the previous request
    w_date = datetime.strptime(session['date_str'], '%d-%b-%Y').date()
    if not session['deriv_date']:
        data = export_utils.create_export_data(w_date, lang)
    else:
        d_date = datetime.strptime(session['deriv_date'], '%d-%b-%Y').date()
        data = export_utils.create_export_data(indate=w_date, lang=lang, deriv_date=d_date)
    sheet = pe.Sheet(data)
	# Create the http response to export
    output = make_response(sheet.csv)
    output.headers["Content-Disposition"] = "attachment; filename=calendaria.csv"
    output.headers["Content-type"] = "text/csv"
    return output


# Test view
@app.route('/test_date')
def test_date():
    d = date.today()
    utc_date = datetime.utcnow()
    moment_date = moment.create(utc_date)
    lz = str(get_localzone())
    return render_template('test_date.html', utc_date=utc_date, moment_date=moment_date, d=d, lz=lz)

# Test view
@app.route('/test_locale')
def test_locale():
	lang = choose_best_lang(request, SUP_LANGUAGES)
	langs = request.accept_languages.best_match(SUP_LANGUAGES)
	if request.headers.getlist("X-Forwarded-For"):
	    ip = request.headers.getlist("X-Forwarded-For")[0]
	else:
	    ip = request.remote_addr
	url = 'http://api.ipstack.com/' + str(ip)
	url += '?access_key=' + IPSTACK_API_KEY
	r = requests.get(url)
	j = json.loads(r.text)
	city = j['city']
	return render_template('test_locale.html', loc=lang, url=url, city=city, langs=langs)

# Test view
@app.route('/test_locale2')
def test_locale2():
    tz_str = get_tz_str(IPSTACK_API_KEY, request=request)
    tz = get_tz(IPSTACK_API_KEY, request=request)
    local_date = set_tz_date(datetime.utcnow(), tz)
    other_date = set_tz_date(datetime.utcnow(), 'Pacific/Auckland')
    return render_template('test_date2.html', tz_str=tz_str,
        local_date=local_date, other_date=other_date)



