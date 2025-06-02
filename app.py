from app import create_app, db
from app.models import User

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

def create_admin_user():
    # Check if admin user exists
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin = User(username='admin', email='admin@example.com', role='admin')
        admin.set_password('admin') # Set a default password
        db.session.add(admin)
        db.session.commit()
        print('Admin user created.')
    else:
        # Ensure admin role is set, in case it was changed manually or by an older version
        if admin_user.role != 'admin':
            admin_user.role = 'admin'
            db.session.commit()
            print('Admin user role updated.')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
        create_admin_user() # Create a default admin user
    app.run(debug=True)
