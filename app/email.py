from flask_mail import Message
from flask import render_template, url_for
from app import app, mail
from threading import Thread
import sendgrid
from sendgrid.helpers.mail import *

def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
	msg = Message(subject, sender=sender, recipients=recipients)
	msg.body = text_body
	msg.html = html_body
	# mail.send(msg)
	Thread(target=send_async_email, args=(app, msg)).start()


# Send email via flask
def send_password_reset_email(user, loc):
	if 'es' in loc.lower():
		title = '[Calendaria] Actualice su contraseña'
		email_txt_temp = 'es/email/reset_password.txt'
		email_html_temp = 'es/email/reset_password.html'
	else:
		title = '[Calendaria] Reset your password'
		email_txt_temp = 'email/reset_password.txt'
		email_html_temp = 'email/reset_password.html'

	token = user.get_reset_password_token()
	send_email(title,
		sender=app.config['ADMINS'][0],
		recipients=[user.email],
		text_body=render_template(email_txt_temp, user=user, token=token),
		html_body=render_template(email_html_temp, user=user, token=token))


# Send email via sendgrid (we are going to use this one)
def sendgrid_password_reset_email(user, loc):
	token = user.get_reset_password_token()
	if 'es' in loc.lower():
		title = '[Calendaria] Actualice su contraseña'
		body = user.first_name + ",\n"
		body += '\n\nPara actualizar su contraseña haga click en el siguiente link:\n'
		body += '\n' + str(url_for('reset_password_es', token=token, _external=True))
		body += '\n\nSi ud. no ha solicitado un cambio de contraseña, puede ignorar este email.'
		body += '\n\nSinceramente,'
		body += '\nCalendaria Team'
	else:
		title = '[Calendaria] Reset your password'
		body = 'Testing'
		body = user.first_name + ",\n"
		body += '\n\nTo reset your password click the following link:\n'
		body += '\n' + str(url_for('reset_password', token=token, _external=True))
		body += '\n\nIf you have not requested to change your password please disregard this email.'
		body += '\n\nSincerely,'
		body += '\nCalendaria Team'

	sg = sendgrid.SendGridAPIClient(apikey=app.config['SENDGRID_API_KEY'])
	from_email = Email('no-reply@calendaria.com')
	to_email = Email(user.email)
	subject = title
	content = Content('text/plain', body)
	mail = Mail(from_email, subject, to_email, content)
	response = sg.client.mail.send.post(request_body=mail.get())
