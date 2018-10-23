import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQL_DB_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}"
SQL_DB_URI = SQL_DB_URI.format(
    username=os.environ.get('USERNAME'),
    password=os.environ.get('MYSQL_DB_PASSWORD'),
    hostname=os.environ.get('MYSQL_DB_HOSTNAME'),
    databasename=os.environ.get('MYSQL_DB_NAME')
)

# Config object with all settings
class Config(object):
	# CSRF
	SECRET_KEY = os.environ.get('SECRET_KEY')
	# Debug
	DEBUG = True
	# DB
	# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_DATABASE_URI = SQL_DB_URI
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_POOL_RECYCLE = 299
	# Email
	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	ADMINS = ['calendariasup@gmail.com']
	SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
	# Languages and location
	LANGUAGES = ['en', 'en_US', 'es', 'es_ES', 'es_AR']
	IPSTACK_API_KEY = os.environ.get('IPSTACK_API_KEY')


