from flask import Flask, render_template, request, flash, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db_create import User, ToDo  # Import the User and ToDo models from your models file

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Replace with a secure, random key

# Set up the database engine and session
engine = create_engine("sqlite:///todo.db")  # Ensure this points to your actual database file
Session = sessionmaker(bind=engine)
db_session = Session()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve data from the form
        username = request.form.get('username')
        password = request.form.get('password')
        # Query the database to find the user with the given username
        user = db_session.query(User).filter_by(username=username).first()
        # Check if the user exists and if the password matches
        if user and check_password_hash(user.password, password):
            # Store the user's ID in the session
            session['user_id'] = user.id
            flash('Login successful!', 'info')
            return redirect(url_for('dashboard'))  # Redirect to the dashboard
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = db_session.query(User).filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'danger')
            return redirect(url_for('signup'))
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db_session.add(new_user)
        db_session.commit()
        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))
    # Retrieve the user's to-dos from the database
    user_id = session['user_id']
    user = db_session.query(User).get(user_id)
    return render_template('dashboard.html', todos=user.todos)

@app.route('/add_task', methods=['POST'])
def add_task():
    # Check if the user is logged in
    if 'user_id' not in session:
        flash('Please log in to add tasks.', 'warning')
        return redirect(url_for('login'))
    # Retrieve data from the form
    title = request.form['title']
    description = request.form['description']
    category = request.form['category']
    due_date = request.form['due_date']
    user_id = session['user_id']
    # Create a new task
    new_task = ToDo(title=title, description=description, category=category, due_date=due_date, user_id=user_id)
    db_session.add(new_task)
    db_session.commit()
    flash('Task added successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)