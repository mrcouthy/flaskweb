import os

basedir = os.path.abspath(os.path.dirname(__file__))

class TestConfig:
    TESTING = True
    SECRET_KEY = 'test-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'test_app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing forms easily
    LOGIN_DISABLED = False # Make sure login is not disabled for auth tests
    SERVER_NAME = 'localhost.localdomain' # To ensure url_for works correctly in tests without a request context
    APPLICATION_ROOT = '/'
