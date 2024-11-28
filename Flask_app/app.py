from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db_create import User, ToDo
from datetime import datetime, time
import re

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

        # Password validation
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return redirect(url_for('signup'))
        
        if not re.search(r'[A-Z]', password):
            flash('Password must contain at least one uppercase letter.', 'danger')
            return redirect(url_for('signup'))
            
        if not re.search(r'[a-z]', password):
            flash('Password must contain at least one lowercase letter.', 'danger')
            return redirect(url_for('signup'))
            
        if not re.search(r'[0-9]', password):
            flash('Password must contain at least one number.', 'danger')
            return redirect(url_for('signup'))
            
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            flash('Password must contain at least one special character.', 'danger')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(username=username, password=hashed_password)
        try:
            db_session.add(new_user)
            db_session.commit()
            flash('Signup successful! Please login.', 'success')
            return redirect(url_for('login'))
        except:
            db_session.rollback()
            flash('Username already exists. Please choose a different one.', 'danger')

    logo_path = url_for('static', filename='images/logo.png')
    return render_template('signup.html', logo_path=logo_path)

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

    logo_path = url_for('static', filename='images/logo.png')
    return render_template('login.html', logo_path=logo_path)

@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    current_datetime = datetime.now()
    current_time = current_datetime.strftime('%I:%M:%S %p')
    
    # Get all todos and categorize them
    todos = db_session.query(ToDo)\
        .filter_by(user_id=user_id)\
        .order_by(ToDo.due_date.asc(), ToDo.due_time.asc())\
        .all()
    
    # Categorize tasks
    overdue_tasks = []
    due_today = []
    upcoming_tasks = []
    completed_tasks = []
    
    for todo in todos:
        if todo.done:
            completed_tasks.append(todo)
        elif todo.due_date:
            if todo.due_date < current_datetime.date():
                overdue_tasks.append(todo)
            elif todo.due_date == current_datetime.date():
                due_today.append(todo)
            else:
                upcoming_tasks.append(todo)
        else:
            upcoming_tasks.append(todo)
    
    # Calculate statistics
    stats = {
        'total': len(todos),
        'completed': len(completed_tasks),
        'overdue': len(overdue_tasks),
        'due_today': len(due_today),
        'upcoming': len(upcoming_tasks),
        'completion_rate': round((len(completed_tasks) / len(todos) * 100) if todos else 0, 1)
    }
    
    tasks_for_calendar = []
    for todo in todos:
        if todo.due_date:
            time_str = todo.due_time.strftime('%H:%M') if todo.due_time else ''
            
            # Enhanced status-based coloring
            if todo.done:
                color = '#28a745'  # Green for completed
            elif todo.due_date < current_datetime.date():
                color = '#dc3545'  # Red for overdue
            elif todo.due_date == current_datetime.date():
                color = '#ffc107'  # Yellow for due today
            else:
                color = '#007bff'  # Blue for upcoming
            
            display_text = f"{todo.title} - Due: {time_str}" if time_str else todo.title
            if todo.description:
                display_text = f"{display_text}\n{todo.description}"
            
            tasks_for_calendar.append({
                'title': display_text,
                'start': f"{todo.due_date.strftime('%Y-%m-%d')}T{time_str}" if time_str else todo.due_date.strftime('%Y-%m-%d'),
                'description': todo.description,
                'done': todo.done,
                'color': color,
                'display': 'block',
                'className': f"calendar-event {'task-completed' if todo.done else ''}",
                'allDay': True,
                'overflow': 'auto'
            })
    
    logo_path = url_for('static', filename='images/logo.png')
    return render_template('dashboard.html', 
                         todos=todos,
                         overdue_tasks=overdue_tasks,
                         due_today=due_today,
                         upcoming_tasks=upcoming_tasks,
                         completed_tasks=completed_tasks,
                         stats=stats,
                         logo_path=logo_path,
                         current_date=current_datetime,
                         current_time=current_time,
                         tasks_for_calendar=tasks_for_calendar)

@app.route('/add_task', methods=['POST'])
def add_task():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    title = request.form['title']
    description = request.form['description']
    due_date_str = request.form['due_date']
    due_time_str = request.form['due_time']
    
    due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
    due_time = datetime.strptime(due_time_str, '%H:%M').time() if due_time_str else None
    
    new_task = ToDo(
        title=title,
        description=description,
        due_date=due_date,
        due_time=due_time,
        done=False,
        user_id=user_id
    )
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
        due_date_str = request.form['due_date']
        due_time_str = request.form['due_time']
        
        task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
        task.due_time = datetime.strptime(due_time_str, '%H:%M').time() if due_time_str else None
        
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
    logo_path = url_for('static', filename='images/logo.png')
    brand_info = {
        'name': 'G STATUS',
        'tagline': 'FASTEST AND MOST EFFICIENT TASK MANAGER'
    }
    features = [
        {
            'title': 'Smart Organization',
            'description': 'Organize your tasks efficiently with our intuitive interface.',
            'icon': 'fa-calendar-alt'
        },
        {
            'title': 'Real-Time Updates',
            'description': 'Stay on top of your tasks with instant updates and notifications.',
            'icon': 'fa-bolt'
        },
        {
            'title': 'Reliable Security',
            'description': 'Your data is protected with advanced security measures.',
            'icon': 'fa-shield-alt'
        },
        {
            'title': 'Progress Tracking',
            'description': 'Monitor your productivity with comprehensive tracking tools.',
            'icon': 'fa-chart-line'
        }
    ]
    
    return render_template('index.html', 
                         logo_path=logo_path, 
                         features=features, 
                         brand_info=brand_info)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

# All rights reserved. This software is the confidential and proprietary information
# of G STATUS. © 2024 G STATUS. All rights reserved.
