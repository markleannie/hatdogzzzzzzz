import json  # Add this import
import smtplib
import time
from enum import Enum
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_manager, LoginManager
from flask_login import login_required, current_user
from sqlalchemy import text
from datetime import datetime   
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer


local_server = True
app = Flask(__name__)
app.secret_key = 'management'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587 
app.config['MAIL_USE_TLS'] = True  
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = params['gmail-user']
app.config['MAIL_PASSWORD'] = params['gmail-password'] 
app.config['MAIL_TIMEOUT'] = 120

mail = Mail(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/management'
db = SQLAlchemy(app)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))


class TitleEnum(Enum):
    Prof = "Prof"
    Asst_Prof = "Asst. Prof"
    Assoc_Prof = "Assoc. Prof"
    Lecturer = "Lecturer"
    Sr_Lecturer = "Sr. Lecturer"
    Instructor = "Instructor"
    Teaching_Fellow = "Teaching Fellow"
    Research_Fellow = "Research Fellow"
    Dr = "Dr."
    PhD_Candidate = "Ph.D. Candidate"
    PhD = "Ph.D"
    MA = "M.A."
    MS = "M.S."
    MSc = "M.Sc."
    BA = "B.A."
    BSc = "B.Sc."
    Engr = "Engr."
    CPA = "CPA"
    RN = "RN"
    Attorney = "Attorney or Esq"
    Rev = "Rev."
    Emeritus = "Emeritus"
    Visiting_Professor = "Visiting Professor"
    Honorary_Professor = "Honorary Professor"
    Distinguished_Professor = "Distinguished Professor"
    Clinical_Professor = "Clinical Professor"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(150))
    title = db.Column(db.Enum(TitleEnum), nullable=True)
    office_hours = db.Column(db.String(255))
    marital_status = db.Column(db.String(50))
    contact_number = db.Column(db.String(15))
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    birthday = db.Column(db.Date)
    address = db.Column(db.String(255))
    bookings = db.relationship('Booking', backref='user', lazy=True)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_code = db.Column(db.String(20), nullable=False)
    course_title = db.Column(db.String(100), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)  # Reference to Room model
    class_code = db.Column(db.String(20), nullable=False)
    day = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    class_type = db.Column(db.String(20), nullable=False)
    semester_start = db.Column(db.Date, nullable=False)
    semester_end = db.Column(db.Date, nullable=False)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(50), nullable=False, unique=True)
    building = db.Column(db.String(100), nullable=True)
    capacity = db.Column(db.Integer, nullable=True)
    bookings = db.relationship('Booking', backref='room', lazy=True)
    
    def __init__(self, room_id, capacity, available_times):
        self.room_id = room_id
        self.capacity = capacity
        self.available_times = available_times 

    def book_room(self, day, time_slot):
        if time_slot in self.available_times.get(day, []):
            self.available_times[day].remove(time_slot)
            return True
        return False


@app.route('/')
def landingpage():
    return render_template('landingpage.html')


@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/userprofile')
def userprof():
    return render_template('userprof.html')

@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is connected'
    except:
        return 'My db is not connected'

@app.route('/buildings')
def buildings():
    return render_template('buildings.html')


@app.route('/rooms', methods=['GET'])
def rooms():
    room_query = request.args.get('room_name')  
    if room_query:
        rooms = Room.query.filter(Room.room_name.ilike(f'%{room_query}%')).all()
    else:
        rooms = Room.query.all()

    rooms_data = [{"room_name": room.room_name, "building": room.building, "capacity": room.capacity} for room in rooms]

    return render_template('rooms.html', rooms=rooms_data)


@app.route('/bookings', methods=['GET', 'POST'])
@login_required
def bookings():
    if request.method == 'POST':
        instructor_id = request.form['instructor_id'] 
        course_code = request.form['course_code']
        course_title = request.form['course_title']
        class_code = request.form['class_code']
        room = request.form['room']
        day = request.form['day']
        start_time = datetime.strptime(request.form['start_time'], '%H:%M').time()
        end_time = datetime.strptime(request.form['end_time'], '%H:%M').time()
        class_type = request.form['class_type']
        
        try:
            semester_start = datetime.strptime(request.form['semester_start'], '%Y-%m-%d').date()
            semester_end = datetime.strptime(request.form['semester_end'], '%Y-%m-%d').date()
        except ValueError:
            flash("Invalid date format for semester start or end.", "danger")
            return redirect(url_for('bookings'))

        today = time.strftime("%m-%d-%Y")

        combined_string = f"{today} {start_time}"

        try:
            selected_datetime = datetime.strptime(combined_string, "%m-%d-%Y %H:%M")
        except ValueError:
            flash("Invalid date or time format.", "danger")
            return redirect(url_for('bookings'))

        now = datetime.now()

        if selected_datetime < now:
            flash("You cannot book a room for a past date/time.", "danger")
            return redirect(url_for('bookings'))

        conflict = Booking.query.filter(
            Booking.room == room,
            Booking.day == day,
            Booking.start_time < end_time,
            Booking.end_time > start_time
        ).first()

        if conflict:
            flash(f"This room is already booked for {day}, {start_time}-{end_time}. Please choose another room or time.", 'error')
            return redirect('/bookings')

        max_duration = (semester_end - semester_start).days
        if max_duration > 180:
            flash("Booking duration exceeds the maximum allowed semester length of 6 months.", 'error')
            return redirect('/bookings')

        new_booking = Booking(
            user_id=instructor_id,  
            course_code=course_code,
            course_title=course_title,
            class_code=class_code,
            room=room,
            day=day,
            start_time=start_time,
            end_time=end_time,
            class_type=class_type,
            semester_start=semester_start,
            semester_end=semester_end
        )
        db.session.add(new_booking)
        db.session.commit()

        flash("Room booked successfully!", 'success')
        return redirect('/bookings')

    bookings = Booking.query.all()
    return render_template('bookings.html', bookings=bookings)

@app.route('/check-availability', methods=['POST'])
@login_required
def check_availability():
    data = request.get_json()
    room = data['room']
    day = data['day']
    start_time = datetime.strptime(data['start_time'], '%H:%M').time()
    end_time = datetime.strptime(data['end_time'], '%H:%M').time()

    # Check for conflicts
    conflict = Booking.query.filter(
        Booking.room == room,
        Booking.day == day,
        Booking.start_time < end_time,
        Booking.end_time > start_time
    ).first()

    return jsonify({'available': conflict is None})


@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_authenticated:
        # Query bookings and join with User to get the instructor (assuming current_user is the instructor)
        bookings = db.session.query(Booking).join(User).filter(User.id == current_user.id).all()
    else:
        bookings = []

    return render_template('dashboard.html', query=bookings)


@app.route('/editprofile')
def editprofile():
    return render_template('editprofile.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get the form data
        username = request.form.get('username')
        firstname = request.form.get('firstname')
        middlename = request.form.get('middlename')
        lastname = request.form.get('lastname')
        department = request.form.get('department')
        title = request.form.get('title')

        # Validate title enum
        # Map title with spaces to the TitleEnum keys
        try:
            title_enum = TitleEnum[title.replace('.', '').replace(' ', '_')]
        except KeyError:
            return render_template('signup.html', error="Invalid title selected")


        office_hours = request.form.get('officehours')
        contact_number = request.form.get('contact')
        age = request.form.get('age')
        birthday = request.form.get('birthday')
        address = request.form.get('address')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if all fields are filled
        if not all([username, firstname, middlename, lastname, department, title, office_hours, contact_number, age, birthday, address, email, password]):
            flash("Please fill in all required fields", "danger")
            return render_template('signup.html')

        # Convert birthday to datetime object
        try:
            birthday_date = datetime.strptime(birthday, '%Y-%m-%d')
        except ValueError:
            flash("Invalid birthday format. Please use YYYY-MM-DD.", "danger")
            return render_template('signup.html')

        # Calculate the expected age from the birthday
        today = datetime.today()
        expected_age = today.year - birthday_date.year
        if today.month < birthday_date.month or (today.month == birthday_date.month and today.day < birthday_date.day):
            expected_age -= 1  # If the birthday hasn't occurred yet this year, subtract 1 from the age

        # Initialize an error list
        error_messages = []

        # Check if the age matches the birthday
        if int(age) != expected_age:
            error_messages.append(f"The age you entered ({age}) does not match your birthday ({birthday_date.date()}).")

        # Check if email or username already exists in the database
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()

        if existing_user:
            if existing_user.email == email:
                error_messages.append('The email address is already in use. Please use a different email.')
            if existing_user.username == username:
                error_messages.append('The username is already taken. Please choose a different username.')

        # If there are errors, display them
        if error_messages:
            for message in error_messages:
                flash(message, 'danger')
            return render_template('signup.html')  # Return to the signup page with error messages

        encpassword = generate_password_hash(password)

        # Create a new user and commit to the database
        new_user = User(
            username=username,
            first_name=firstname,
            middle_name=middlename,
            last_name=lastname,
            department=department,
            title=title_enum,
            office_hours=office_hours,
            contact_number=contact_number,
            age=age,
            birthday=birthday_date,
            address=address,
            email=email,
            password=encpassword
        )

        # Add the new user to the session and commit the transaction
        db.session.add(new_user)
        db.session.commit()

        flash('Successfully signed up!', 'success')
        return redirect(url_for('login'))  # Redirect to login page after successful signup

    return render_template('signup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login Successful", "primary")
            return redirect(url_for('base'))  # Redirect to dashboard after login
        else:
            flash("Invalid credentials. Please try again.", "danger")
            return redirect(url_for('login'))  # Redirect back to login

    return render_template('login.html')


@app.route('/forgotpass', methods=['GET', 'POST'])
def forgotpass():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            # Generate the reset token
            serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
            token = serializer.dumps(email, salt='password-reset-salt')
            reset_link = url_for('resetpass', token=token, _external=True)

            # Send the email with the reset link
            mail.send_message(
                subject='Password Reset Request',
                sender=params['gmail-user'],
                recipients=[email],
                body=f"To reset your password, visit the following link: {reset_link}"
            )

            flash("A password reset link has been sent to your email address.", "info")
            return redirect(url_for('login'))
        else:
            flash("Email address not found.", "danger")
            return render_template('forgotpass.html')

    return render_template('forgotpass.html')


@app.route('/resetpass/<token>', methods=['GET', 'POST'])
def resetpass(token):
    try:
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)  # Token expires after 1 hour
    except:
        flash("The password reset link is invalid or has expired.", "danger")
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = generate_password_hash(new_password)
            db.session.commit()
            flash("Your password has been reset successfully.", "success")
            return redirect(url_for('login'))
        else:
            flash("User not found.", "danger")
            return redirect(url_for('login'))

    return render_template('resetpass.html', token=token)

@app.route('/logout')   
@login_required
def logout():
    logout_user()
    session.clear()  # This will ensure session is cleared after logout
    flash("You have been logged out", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
