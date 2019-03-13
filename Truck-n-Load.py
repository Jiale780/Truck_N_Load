from app import app, db
from app.models import User


@app.shell_context_processor
def make_shell_context():
    """This is used to make the 'flask shell' from the CLI work"""
    return {'db': db, 'User': User}
