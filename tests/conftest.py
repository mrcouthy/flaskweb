import pytest
import sys
import os

# Add project root to sys.path to allow imports from 'app'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User
from tests.test_config import TestConfig

@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for each test session."""
    app = create_app(config_class=TestConfig)
    with app.app_context():
        db.create_all()
        # You can create any initial data needed for all tests here
        # Example: Create a default admin and regular user
        if User.query.filter_by(username='admin_test').first() is None:
            admin = User(username='admin_test', email='admin_test@example.com', role='admin')
            admin.set_password('admin_password')
            db.session.add(admin)

        if User.query.filter_by(username='user_test').first() is None:
            user = User(username='user_test', email='user_test@example.com', role='user')
            user.set_password('user_password')
            db.session.add(user)
        db.session.commit()

    yield app

    # Clean up / reset database after test session
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(scope='function')
def init_database(app):
    """Clear and re-initialize database for each function-scoped test if needed,
       or ensure it's clean before each test.
       For session-scoped app fixture with pre-populated data,
       this might involve more targeted cleanup or transaction rollbacks."""
    with app.app_context():
        # This ensures tables are created but doesn't drop them per function
        # as the app fixture is session-scoped.
        # If tests modify data and need a clean slate per test (not session),
        # a more granular approach or transaction management is needed.
        # For now, assuming tests either don't conflict or manage their own data creation/deletion.
        # db.create_all() # Already done in app fixture
        pass

    yield db

    # If you need to clean up specific tables or reset state after each test function:
    # with app.app_context():
        # db.session.remove()
        # db.drop_all()
        # db.create_all()
        # This part is tricky with session-scoped app fixture.
        # Usually, you'd run tests in transactions and roll back,
        # or fully recreate db per test (slower).
        # For this setup, we rely on tests to clean up if they add conflicting data,
        # or we ensure initial data is sufficient and non-conflicting.
        # pass # This pass was causing an indentation error.


@pytest.fixture(scope='function')
def new_user_data():
    """Provides data for a new user registration."""
    return {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'newpassword'
    }
