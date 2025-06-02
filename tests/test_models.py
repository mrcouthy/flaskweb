import pytest
from app.models import User
from app import db

def test_password_hashing(app):
    """Test password hashing and verification."""
    with app.app_context():
        u = User(username='testuser_model', email='test_model@example.com')
        u.set_password('cat')
        assert u.check_password('cat')
        assert not u.check_password('dog')

def test_default_user_role(app):
    """Test that a new user gets the default 'user' role."""
    with app.app_context():
        u = User(username='test_default_role', email='test_default_role@example.com')
        # SQLAlchemy default values might be populated when the object is added to the session
        # or upon flush. For an in-memory object not yet part of a session,
        # the default specified in Column() might not be explicitly set on the Python object yet.
        db.session.add(u)
        db.session.commit() # Commit to ensure defaults are applied if they are db-side
        assert u.role == 'user'
        # Clean up by deleting the user
        db.session.delete(u)
        db.session.commit()

def test_admin_user_role(app):
    """Test setting the 'admin' role."""
    with app.app_context():
        # User created in conftest.py
        admin_user = User.query.filter_by(username='admin_test').first()
        assert admin_user is not None
        assert admin_user.role == 'admin'

def test_user_representation(app):
    """Test the __repr__ method of User."""
    with app.app_context():
        u = User(username='repr_user', email='repr@example.com')
        db.session.add(u)
        db.session.commit()
        assert repr(u) == '<User repr_user>'
        # Clean up
        db.session.delete(u)
        db.session.commit()

def test_unique_username(app):
    """Test that usernames are unique."""
    with app.app_context():
        u1 = User(username='unique_user', email='unique1@example.com')
        db.session.add(u1)
        db.session.commit()

        u2 = User(username='unique_user', email='unique2@example.com')
        try:
            db.session.add(u2)
            db.session.commit()
            assert False, "SQLAlchemy should have raised an IntegrityError for unique username constraint"
        except Exception as e: # Catching a general exception to see what SQLAlchemy throws
            db.session.rollback()
            assert "UNIQUE constraint failed: user.username" in str(e) or "Duplicate entry" in str(e) or "violates unique constraint" in str(e)

        # Clean up
        db.session.delete(u1)
        db.session.commit()


def test_unique_email(app):
    """Test that emails are unique."""
    with app.app_context():
        u1 = User(username='user_unique_email1', email='unique_email@example.com')
        db.session.add(u1)
        db.session.commit()

        u2 = User(username='user_unique_email2', email='unique_email@example.com')
        try:
            db.session.add(u2)
            db.session.commit()
            assert False, "SQLAlchemy should have raised an IntegrityError for unique email constraint"
        except Exception as e: # Catching a general exception
            db.session.rollback()
            assert "UNIQUE constraint failed: user.email" in str(e) or "Duplicate entry" in str(e) or "violates unique constraint" in str(e)

        # Clean up
        db.session.delete(u1)
        db.session.commit()
