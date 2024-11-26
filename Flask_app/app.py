# from flask import Flask, render_template, request, flash, session, redirect, url_for
# from werkzeug.security import generate_password_hash, check_password_hash
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine
# from db_create import User, ToDo  # Import the User and ToDo models from your models file

# app = Flask(__name__)
# app.secret_key = "supersecretkey"  # Replace with a secure, random key

# # Set up the database engine and session
# engine = create_engine("sqlite:///todo.db")  # Ensure this points to your actual database file
# Session = sessionmaker(bind=engine)
# db_session = Session()

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         hashed_password = generate_password_hash(password, method='sha256')

#         new_user = User(username=username, password=hashed_password)
#         try:
#             db_session.add(new_user)
#             db_session.commit()
#             flash('Signup successful! Please login.', 'success')
#             return redirect(url_for('login'))
#         except:
#             db_session.rollback()
#             flash('Username already exists. Please choose a different one.', 'danger')

#     return render_template('signup.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         user = db_session.query(User).filter_by(username=username).first()
#         if user and check_password_hash(user.password, password):
#             session['user_id'] = user.id
#             flash('Login successful!', 'info')
#             return redirect(url_for('dashboard'))
#         else:
#             flash('Invalid username or password', 'danger')

#     return render_template('login.html')

# @app.route('/dashboard')
# def dashboard():
#     user_id = session.get('user_id')
#     if not user_id:
#         return redirect(url_for('login'))
#     todos = db_session.query(ToDo).filter_by(user_id=user_id).all()
#     return render_template('dashboard.html', todos=todos)

# @app.route('/add_task', methods=['POST'])
# def add_task():
#     user_id = session.get('user_id')
#     if not user_id:
#         return redirect(url_for('login'))
#     title = request.form['title']
#     description = request.form['description']
#     new_task = ToDo(title=title, description=description, done=False, user_id=user_id)
#     db_session.add(new_task)
#     db_session.commit()
#     return redirect(url_for('dashboard'))

# @app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
# def edit_task(task_id):
#     user_id = session.get('user_id')
#     if not user_id:
#         return redirect(url_for('login'))
#     task = db_session.query(ToDo).filter_by(id=task_id, user_id=user_id).first()
#     if request.method == 'POST':
#         task.title = request.form['title']
#         task.description = request.form['description']
#         task.done = request.form.get('done') == 'on'
#         db_session.commit()
#         return redirect(url_for('dashboard'))
#     return render_template('edit_task.html', task=task)

# @app.route('/delete_task/<int:task_id>')
# def delete_task(task_id):
#     user_id = session.get('user_id')
#     if not user_id:
#         return redirect(url_for('login'))
#     task = db_session.query(ToDo).filter_by(id=task_id, user_id=user_id).first()
#     db_session.delete(task)
#     db_session.commit()
#     return redirect(url_for('dashboard'))

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     flash('You have been logged out.', 'info')
#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from Flask_app.db_create import User, ToDo  # Import the User and ToDo models from your models file

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Replace with a secure, random key

# Set up the database engine and session
engine = create_engine("sqlite:///todo.db")  # Ensure this points to your actual database file
Session = sessionmaker(bind=engine)
db_session = Session()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')

        new_user = User(username=username, password=hashed_password)
        try:
            db_session.add(new_user)
            db_session.commit()
            flash('Signup successful! Please login.', 'success')
            return redirect(url_for('login'))
        except:
            db_session.rollback()
            flash('Username already exists. Please choose a different one.', 'danger')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = db_session.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'info')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    todos = db_session.query(ToDo).filter_by(user_id=user_id).all()
    return render_template('dashboard.html', todos=todos)

@app.route('/add_task', methods=['POST'])
def add_task():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    title = request.form['title']
    description = request.form['description']
    new_task = ToDo(title=title, description=description, done=False, user_id=user_id)
    db_session.add(new_task)
    db_session.commit()
    return redirect(url_for('dashboard'))

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    task = db_session.query(ToDo).filter_by(id=task_id, user_id=user_id).first()
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        task.done = request.form.get('done') == 'on'
        db_session.commit()
        return redirect(url_for('dashboard'))
    return render_template('edit_task.html', task=task)

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    task = db_session.query(ToDo).filter_by(id=task_id, user_id=user_id).first()
    db_session.delete(task)
    db_session.commit()
    return redirect(url_for('dashboard'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
