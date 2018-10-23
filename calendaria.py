from app import app, db
from app.models import User

# Create app context to use on shell
@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User}