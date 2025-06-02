import pytest
from flask import url_for, get_flashed_messages
from app.models import User
from app import db

# Helper function to log in a user
def login(client, username, password):
    return client.post(url_for('auth.login'), data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

# Helper function to log out a user
def logout(client):
    return client.get(url_for('auth.logout'), follow_redirects=True)


def test_register_new_user(client, new_user_data, app):
    """Test new user registration."""
    response = client.post(url_for('auth.register'), data=dict(
        username=new_user_data['username'],
        email=new_user_data['email'],
        password=new_user_data['password'],
        password2=new_user_data['password']
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Congratulations, you are now a registered user!' in response.data
    # Check user in database
    with app.app_context():
        user = User.query.filter_by(username=new_user_data['username']).first()
        assert user is not None
        assert user.email == new_user_data['email']
        # Clean up
        db.session.delete(user)
        db.session.commit()

def test_register_duplicate_username(client, new_user_data, app):
    """Test registration with a duplicate username."""
    # Create a user first
    with app.app_context():
        user = User(username=new_user_data['username'], email='someother@example.com')
        user.set_password(new_user_data['password'])
        db.session.add(user)
        db.session.commit()

    response = client.post(url_for('auth.register'), data=dict(
        username=new_user_data['username'], # Duplicate username
        email=new_user_data['email'],
        password=new_user_data['password'],
        password2=new_user_data['password']
    ), follow_redirects=True)
    assert response.status_code == 200 # Should render the form again
    assert b'Please use a different username.' in response.data

    with app.app_context(): # Clean up
        db.session.delete(user)
        db.session.commit()


def test_register_duplicate_email(client, new_user_data, app):
    """Test registration with a duplicate email."""
    with app.app_context():
        user = User(username='anotheruser', email=new_user_data['email']) # Duplicate email
        user.set_password(new_user_data['password'])
        db.session.add(user)
        db.session.commit()

    response = client.post(url_for('auth.register'), data=dict(
        username=new_user_data['username'],
        email=new_user_data['email'], # Duplicate email
        password=new_user_data['password'],
        password2=new_user_data['password']
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Please use a different email address.' in response.data

    with app.app_context(): # Clean up
        db.session.delete(user)
        db.session.commit()

def test_login_logout_valid_user(client, app):
    """Test login and logout for a valid pre-existing user."""
    # Uses 'user_test' created in conftest.py
    response = login(client, 'user_test', 'user_password')
    assert response.status_code == 200
    assert b'Hi, user_test!' in response.data # Assuming index shows username

    # Check profile access
    response = client.get(url_for('auth.profile'))
    assert response.status_code == 200
    # Make the assertion more specific to the HTML structure
    expected_html = b'<p class="card-text"><strong>Username:</strong> user_test</p>'
    assert expected_html in response.data, \
        f"Expected HTML '{expected_html.decode()}' not found in response. Data: {response.data.decode(errors='ignore')[:500]}"

    # Logout
    response = logout(client)
    assert response.status_code == 200
    assert b'Hi, Guest!' in response.data # Assuming index shows Guest after logout

    # Check profile access denied after logout
    response = client.get(url_for('auth.profile'), follow_redirects=True)
    assert response.status_code == 200 # Redirects to login
    assert b'Sign In' in response.data # Should be on login page
    assert b'Please log in to access this page.' in response.data # Flashed message from LoginManager

def test_login_invalid_user(client):
    """Test login with invalid credentials."""
    response = login(client, 'nonexistentuser', 'wrongpassword')
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data

def test_profile_access_unauthenticated(client):
    """Test /profile access when not authenticated."""
    response = client.get(url_for('auth.profile'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Sign In' in response.data # Should redirect to login
    assert b'Please log in to access this page.' in response.data


def test_admin_page_access_as_user(client, app):
    """Test /admin access as a regular user."""
    login(client, 'user_test', 'user_password') # Log in as regular user
    response = client.get(url_for('main.admin_page'))
    assert response.status_code == 403 # Forbidden
    logout(client)

def test_admin_page_access_as_admin(client, app):
    """Test /admin access as an admin user."""
    login(client, 'admin_test', 'admin_password') # Log in as admin
    response = client.get(url_for('main.admin_page'))
    assert response.status_code == 200
    assert b'Admin Dashboard' in response.data
    logout(client)

def test_admin_page_access_unauthenticated(client):
    """Test /admin access when not authenticated."""
    response = client.get(url_for('main.admin_page'), follow_redirects=True)
    assert response.status_code == 200 # Redirects to login
    assert b'Sign In' in response.data
    assert b'Please log in to access this page.' in response.data

def test_login_required_decorator_message(client):
    """Test that Flask-Login's default 'Please log in' message appears."""
    # Accessing a route protected by @login_required from Flask-Login
    # e.g. auth.profile or main.admin_page
    response = client.get(url_for('auth.profile'), follow_redirects=True)
    # Flask-Login redirects to login_view, which is 'auth.login'
    # The message is flashed before redirect.
    with client.session_transaction() as sess:
        flashed_messages = sess.get('_flashes', [])
    # After redirect, the new page (login) will render these messages
    # So we check response.data on the login page.
    assert b'Please log in to access this page.' in response.data

    # Also check for the message on the admin page when unauthenticated
    response = client.get(url_for('main.admin_page'), follow_redirects=True)
    with client.session_transaction() as sess:
        flashed_messages = sess.get('_flashes', [])
    assert b'Please log in to access this page.' in response.data
