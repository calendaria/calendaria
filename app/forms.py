from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


# Form to login
class LoginForm(FlaskForm):
	email = StringField('Email',
		validators=[DataRequired(), Email('Enter a valid email address')],
		render_kw={"placeholder": "email",
			"class": "form-control"})

	password = PasswordField('Password',
		validators=[DataRequired()],
		render_kw={"placeholder": "password",
			"class": "form-control"})

	remember_me = BooleanField('Remember me',
		render_kw={"class": "form-check-input",
			"type": "checkbox",
			"id": "remember_me"})


# Form to login in spanish
class LoginESForm(FlaskForm):
	email = StringField('Email',
		validators=[DataRequired(), Email('Direccion de email invalida')],
		render_kw={"placeholder": "email",
			"class": "form-control"})

	password = PasswordField('Contraseña',
		validators=[DataRequired()],
		render_kw={"placeholder": "contraseña",
			"class": "form-control"})

	remember_me = BooleanField('Remember me',
		render_kw={"class": "form-check-input",
			"type": "checkbox",
			"id": "remember_me"})



# Form to register a new user
class RegistrationForm(FlaskForm):
	email = StringField('Email address',
		validators=[DataRequired(), Email('Enter a valid email address')],
		render_kw={"placeholder": "email",
			"class": "form-control",
			"id": "register-email"})

	dob = DateField('Date of Birth',
		validators=[DataRequired()],
		render_kw={"class": "form-control",
			"id": "register-bday",
			"placeholder": "mm/dd/yyyy",
			"onkeypress": "return false"},
		format="%m/%d/%Y")

	first_name = StringField('First name',
		validators=[DataRequired()],
		render_kw={"placeholder": "first name",
			"class": "form-control",
			"id": "register-fname"})

	password = PasswordField('Set your password',
		validators=[DataRequired()],
		render_kw={"placeholder": "password",
			"class": "form-control",
			"id": "register-pword"})

	password2 = PasswordField('Repeat password',
		validators=[DataRequired(), EqualTo('password')],
		render_kw={"placeholder": "repeat password",
			"class": "form-control",
			"id": "register-pword2"})

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('An account with that email already exists.')

	def validate_password(self, password):
		if len(password.data) < 8:
			raise ValidationError('Password must contain at least 8 characters.')



# Form to register a new user spanish
class RegistrationESForm(FlaskForm):
	email = StringField('Email',
		validators=[DataRequired(), Email('Direccion de email invalida')],
		render_kw={"placeholder": "email",
			"class": "form-control",
			"id": "register-email"})

	dob = DateField('Fecha de nacimiento',
		validators=[DataRequired()],
		render_kw={"class": "form-control",
			"id": "register-bday-es",
			"placeholder": "dd/mm/yyyy",
			"onkeypress": "return false"},
		format="%d/%m/%Y")

	deriv_date = DateField('Fecha de derivación',
		validators=[DataRequired()],
		render_kw={"class": "form-control",
			"id": "derivdate-register-es",
			"placeholder": "dd/mm/yyyy",
			"onkeypress": "return false"},
		format="%d/%m/%Y")

	first_name = StringField('Nombre',
		validators=[DataRequired()],
		render_kw={"placeholder": "primer nombre",
			"class": "form-control",
			"id": "register-fname"})

	password = PasswordField('Contraseña',
		validators=[DataRequired()],
		render_kw={"placeholder": "contraseña",
			"class": "form-control",
			"id": "register-pword"})

	password2 = PasswordField('Repeat password',
		validators=[DataRequired(), EqualTo('password')],
		render_kw={"placeholder": "repita contraseña",
			"class": "form-control",
			"id": "register-pword2"})

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Una cuenta con este email ya ha sido registrado.')

	def validate_password(self, password):
		if len(password.data) < 8:
			raise ValidationError('La contraseña debe de tener al menos 8 caracteres.')


# Check date in spanish
class CheckDateESForm(FlaskForm):
	checkdate = DateField('Fecha de nacimiento',
					validators=[DataRequired()],
					render_kw={"class": "form-control",
							   "id": "check-date-es",
							   "placeholder": "dd/mm/yyyy",
							   "onkeypress": "return false"},
					format="%d/%m/%Y")

# Update the profile information
class UpdateProfileForm(FlaskForm):
	email = StringField('Email address',
		validators=[DataRequired(), Email('Enter a valid email address')],
		render_kw={"placeholder": "email",
			"class": "form-control",
			"id": "update-email"})

	dob = DateField('Date of Birth',
		validators=[DataRequired()],
		render_kw={"class": "form-control",
			"id": "update-bday",
			"placeholder": "mm/dd/yyyy",
			"onkeypress": "return false"},
		format="%m/%d/%Y")

	first_name = StringField('First name',
		validators=[DataRequired()],
		render_kw={"placeholder": "first name",
			"class": "form-control",
			"id": "update-fname"})


# Update the profile information spanish
class UpdateProfileESForm(FlaskForm):
	email = StringField('Email',
		validators=[DataRequired(), Email('Direccion de email invalida')],
		render_kw={"placeholder": "email",
			"class": "form-control",
			"id": "update-email"})

	dob = DateField('Fecha de nacimiento',
		validators=[DataRequired()],
		render_kw={"class": "form-control",
			"id": "update-bday-es",
			"placeholder": "dd/mm/yyyy",
			"onkeypress": "return false"},
		format="%d/%m/%Y")

	deriv_date = DateField('Fecha de derivación',
		validators=[DataRequired()],
		render_kw={"class": "form-control",
			"id": "derivdate-register-es",
			"placeholder": "dd/mm/yyyy",
			"onkeypress": "return false"},
		format="%d/%m/%Y")

	first_name = StringField('Nombre',
		validators=[DataRequired()],
		render_kw={"placeholder": "primer nombre",
			"class": "form-control",
			"id": "update-fname"})


# Reset Password request
class ResetPasswordRequestForm(FlaskForm):
	email = StringField('Email address',
		validators=[DataRequired(), Email('Enter a valid email address')],
		render_kw={"placeholder": "email",
			"class": "form-control",
			"id": "register-email"})


# Reset Password request
class ResetPasswordRequestESForm(FlaskForm):
	email = StringField('Email',
		validators=[DataRequired(), Email('Direccion de email invalida')],
		render_kw={"placeholder": "email",
			"class": "form-control",
			"id": "register-email"})


# Reset Password
class ResetPasswordForm(FlaskForm):
	password = PasswordField('Set your password',
		validators=[DataRequired()],
		render_kw={"placeholder": "password",
			"class": "form-control",
			"id": "register-pword"})

	password2 = PasswordField('Repeat password',
		validators=[DataRequired(), EqualTo('password')],
		render_kw={"placeholder": "repeat password",
			"class": "form-control",
			"id": "register-pword2"})

	def validate_password(self, password):
		if len(password.data) < 8:
			raise ValidationError('Password must contain at least 8 characters.')


# Reset Password spanish
class ResetPasswordESForm(FlaskForm):
	password = PasswordField('Actualice su contraseña',
		validators=[DataRequired()],
		render_kw={"placeholder": "contraseña",
			"class": "form-control",
			"id": "register-pword"})

	password2 = PasswordField('Repita su contraseña',
		validators=[DataRequired(), EqualTo('password')],
		render_kw={"placeholder": "repita contraseña",
			"class": "form-control",
			"id": "register-pword2"})

	def validate_password(self, password):
		if len(password.data) < 8:
			raise ValidationError('La contrasena debe de tener al menos 8 caracteres.')