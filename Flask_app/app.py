from flask import Flask, render_template, request, flash, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db_create import User  # Import the User model from your models file

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
        username = request.form['username']
        password = request.form['password']
        user = db_session.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db_session.add(new_user)
        db_session.commit()
        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)

