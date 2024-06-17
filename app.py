from datetime import datetime

from flask import Flask, render_template, url_for, redirect, jsonify
from flask import request, session, flash
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, validators
from wtforms import SubmitField, EmailField, DateField, SelectField, FieldList, FormField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import InputRequired, ValidationError, DataRequired, Email, Length

import db

# from MySQLdb import MySQLError

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mykali@localhost:3306/hotel_db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.Length(min=8, max=20),
        validators.EqualTo('confirm', message='Passwords must match')
    ], render_kw={"placeholder": "Password"})
    confirm = PasswordField('Repeat Password',
                            render_kw={"placeholder": "Confirm Password"})
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
    submit = SubmitField('Register')
    def validate_username(self, email):
        existing_user_username = User.query.filter_by(
            email=email.data).first()
        if existing_user_username:
            raise ValidationError(
                'That email already exists in our database. Please log in instead.')

class LoginForm(FlaskForm):
    email = StringField('Email Address', [validators.Length(min=6, max=255)])
    password = PasswordField('Password', [
        validators.DataRequired(),
    ])
    submit = SubmitField('Login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, login_form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', login_form=login_form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(register_form.password.data)
        new_user = User(email=register_form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', register_form=register_form)

@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    if 'email' in session and 'is_login' in session and session['is_login']:
        username = session['username']
    return render_template('home.html')


@app.route('/aboutus')
def about_us():
    return render_template('aboutUs.html')


@app.route("/contactus")
def contact():
    return render_template("user/contactUs.html")



@app.route("/experiences")
def experiences():
    return render_template("experience.html")


@app.route('/update_password', methods=['POST'])
@login_required
def update_password():
    if 'username' in session:
        username = session['username']
        new_password = request.form['new_password']
        if new_password:
            customer = db.Customer()
            customer.update_password(username, new_password)
            return redirect(url_for('login'))
        else:
            return "New password cannot be empty"

    else:
        return redirect(url_for('register'))

class BookingForm(FlaskForm):
    class DateRangeValidator:
        def __init__(self, check_in_date_field):
            self.check_in_date_field = check_in_date_field

        def __call__(self, form, field):
            check_in_date = form[self.check_in_date_field]
            if check_in_date.data and field.data and field.data <= check_in_date.data:
                raise ValidationError('Check out date must be later than check in date')

    check_in_date = DateField('Start Date')
    check_out_date = DateField('End Date', validators=[DateRangeValidator('check_in_date')])
    hid = IntegerField('Choose Your Hotel')
    room_capacity = SelectField("Number of Beds", choices=[
        ('', 'Select an option'),
        ('1', 'Single'),
        ('2', 'Double'),
        ('3', 'Triple'),
        ('4', 'Quadruple')
    ], default='', validators=[InputRequired(message='Please select your number of beds')])
    room_type = SelectField("Types of Room", default='', choices=[
        ('', 'Please select an option'),
        ('1', 'Standard'),
        ('2', 'Superior'),
        ('3', 'Deluxe'),
        ('4', 'Suite')
    ], validators=[InputRequired(message='Please select a room type')])
    apply_voucher = StringField('You have a voucher?')

class User(db.Model, UserMixin):
    """User model"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(64), nullable=True)
    date_of_registration = db.Column(db.Date, default=db.func.current_date(), nullable=False)

    def __repr__(self):
        return f"User('{self.email}', '{self.first_name}', '{self.last_name}')"

class EditUserForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=2, max=64)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=64)])
    phone_number = StringField("Phone Number", validators=[Length(max=64)])
    submit = SubmitField("Update")

@app.route("/user", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditUserForm(obj=current_user)
    admin_check = Admin.query.filter_by(admin_email=current_user.email).first()
    admin_check = not admin_check is None
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phone_number = form.phone_number.data
        db.session.commit()
        return redirect(url_for("profile"))
    return render_template("user/edit_profile.html", form=form, admin_check=admin_check)

@app.route("/profile")
@login_required
def profile():
    return render_template("user/profile.html", user=current_user)

class Hotel(db.Model):
    """Hotel model"""
    hid = db.Column(db.Integer, primary_key=True)
    hname = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    hotline = db.Column(db.String(64), nullable=False)
    services = db.Column(db.String(64), default='123456789', nullable=False)

    rooms = db.relationship('Room', backref='hotel', lazy=True)

    def __repr__(self):
        return f"Hotel('{self.hname}', '{self.address}')"

class Room(db.Model):
    """Room model"""
    rid = db.Column(db.Integer, primary_key=True)
    hid = db.Column(db.Integer, db.ForeignKey('hotel.hid'), nullable=False)
    room_type = db.Column(db.String(1), nullable=False)  # 1: Standard, 2: Superior, 3: Deluxe, 4: Suite
    room_capacity = db.Column(db.String(1), nullable=False)  # 1: Single, 2: Double, 3: Trio, 4: Family
    base_price = db.Column(db.Float, nullable=False)
    services = db.Column(db.String(3), nullable=False)  # 1: Wifi, 2: Separate Rooms, 4: Pet care

    def to_dict(self):
        return {
            'rid': self.rid,
            'hid': self.hid,
            'room_type': self.room_type,
            'price': self.base_price
        }
    def __repr__(self):
        return f"Room('{self.room_type}', '{self.room_capacity}', {self.base_price})"
class HotelBooking(db.Model):
    """Booking model"""
    __tablename__ = 'HOTEL_BOOKING'

    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rid = db.Column(db.Integer, db.ForeignKey('room.rid'), nullable=False)
    final_price = db.Column(db.Float, nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    payment_status = db.Column(db.String, nullable=False, default='pending')
    user = db.relationship('User', backref=db.backref('bookings', lazy=True))
    room = db.relationship('Room', backref=db.backref('bookings', lazy=True))

def search_room(hid, room_type, room_capacity):
    rooms = Room.query.filter_by(hid=hid, room_type=room_type, room_capacity=room_capacity).all()
    if rooms:
        return jsonify([room.to_dict() for room in rooms])
    else:
        return jsonify({"error": "No rooms found"}), 404

class Voucher(db.Model):
    __tablename__ = 'VOUCHERS'
    voucher = db.Column(db.String(64), primary_key=True)
    discount_percentage = db.Column(db.Integer)
    discount_amount = db.Column(db.Integer)

    def to_dict(self):
        return {
            'voucher': self.voucher,
            'discount_percentage': self.discount_percentage,
            'discount_amount': self.discount_amount
        }

    def __init__(self, voucher, discount_percentage, discount_amount):
        self.voucher = voucher
        self.discount_percentage = discount_percentage
        self.discount_amount = discount_amount

    def __repr__(self):
        return f"Voucher('{self.voucher}', {self.discount_percentage}, {self.discount_amount})"

def search_voucher(voucher_code):
    vouchers = Voucher.query.filter_by(voucher=voucher_code).all()
    if vouchers:
        return jsonify([voucher.to_dict() for voucher in vouchers])
    else:
        return jsonify({"error": "Voucher not found"}), 404

@app.route('/book_hotel', methods=['GET', 'POST'])
@login_required
def book_hotel():
    form = BookingForm()
    form.hid.data = request.args.get("hotel_id")
    if form.validate_on_submit():
        rid = search_room(form.hid.data, form.room_type.data, form.room_capacity.data)
        rid = rid.get_json()[0]
        rid, price = rid['rid'], rid['price']
        user_id = current_user.id
        if form.apply_voucher.data != '':
            voucher = search_voucher(form.apply_voucher.data)
            voucher = voucher.get_json()[0]
            price -= voucher['discount_amount']
            price *= 1-voucher['discount_percentage']
        hotel_booking = HotelBooking(
            id=user_id,
            rid=rid,
            final_price=price,
            check_in_date=form.check_in_date.data,
            check_out_date=form.check_out_date.data,  # or any other valid date
            payment_status='pending'
        )
        db.session.add(hotel_booking)
        db.session.commit()
        flash("You have successfully book your hotel! Redirecting to payment page.")
        return redirect(url_for('view_bookings'))
    return render_template('user/book_hotel.html', form=form)

@app.route('/payment')
@app.route('/user/payment')
def payment_page():
    # Payment page logic here
    return render_template('payment/payment.html')

@app.route('/payment/cancel')
def payment_cancel():
    return render_template('payment/cancel_booking.html')

@app.route('/myBookings', methods=['GET', 'POST'])
@login_required
def view_bookings():
    bookings = HotelBooking.query.filter_by(id=current_user.id).all()
    return render_template('user/list_bookings.html', bookings=bookings)


# ADMIN
class Admin(db.Model):
    """
    Admin model class
    """
    __tablename__ = 'ADMIN'
    aid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_name = db.Column(db.String(30), nullable=False)
    admin_email = db.Column(db.String(40), nullable=True)
    priviledge_level = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        """
        Returns a dictionary representation of the Admin object
        """
        return {
            'aid': self.aid,
            'admin_name': self.admin_name,
            'admin_email': self.admin_email,
            'priviledge_level': self.priviledge_level
        }

    def __repr__(self):
        return f"Admin('{self.admin_name}', '{self.admin_email}', {self.priviledge_level})"

def myAdmin():
    admin_check = Admin.query.filter_by(admin_email=current_user.email).first()
    if admin_check is None:
        raise ValidationError("You are not admin.")
    return admin_check

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    current_admin = myAdmin()
    return render_template("admin/dashboard.html", current_admin = current_admin)

@app.route('/admin/hotel_list')
def hotel_list():
    current_admin = myAdmin()
    hotels = Hotel.query.all()
    return render_template('admin/hotel_list.html', hotels=hotels)

@app.route('/hotels/<int:hotel_id>/edit', methods=['GET', 'POST'])
def edit_hotel(hotel_id):
    current_admin = myAdmin()
    hotel = Hotel.query.get_or_404(hotel_id)
    if request.method == 'POST':
        # Update hotel details
        hotel.hotel_name = request.form['hname']
        hotel.address = request.form['address']
        #...
        db.session.commit()
        return redirect(url_for('hotel_list'))
    return render_template('admin/edit_hotel.html', hotel=hotel)

@app.route('/hotels/<int:hotel_id>/delete', methods=['POST'])
def delete_hotel(hotel_id):
    current_admin = myAdmin()
    hotel = Hotel.query.get_or_404(hotel_id)
    db.session.delete(hotel)
    db.session.commit()
    return redirect(url_for('admin/hotel_list'))

@app.route('/rooms/<int:room_id>/edit', methods=['GET', 'POST'])
def edit_room(room_id):
    current_admin = myAdmin()
    room = Room.query.get_or_404(room_id)
    if request.method == 'POST':
        # Update room details
        room.room_type = request.form['room_type']
        room.room_capacity = request.form['room_capacity']
        room.base_price = request.form['base_price']
        #...
        db.session.commit()
        return redirect(url_for('edit_hotel', hotel_id=room.hid))
    return render_template('admin/edit_room.html', room=room)

@app.route('/rooms/<int:room_id>/delete', methods=['POST'])
def delete_room(room_id):
    current_admin = myAdmin()
    room = Room.query.get_or_404(room_id)
    db.session.delete(room)
    db.session.commit()
    return redirect(url_for('admin/edit_hotel', hotel_id=room.hid))

class AdminForm(FlaskForm):
    admin_name = StringField("Admin Name", validators=[DataRequired()])
    admin_email = StringField("Admin Email", validators=[DataRequired(), Email()])
    priviledge_level = IntegerField("priviledge Level", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route("/personnel", methods=["GET"])
def personnel():
    admins = Admin.query.all()
    return render_template("admin/personnel.html", admins=admins)

@app.route("/add_admin", methods=["GET", "POST"])
def add_admin():
    form = AdminForm()
    if form.validate_on_submit():
        admin = Admin(admin_name=form.admin_name.data, admin_email=form.admin_email.data, priviledge_level=form.priviledge_level.data)
        db.session.add(admin)
        db.session.commit()
        return redirect(url_for("personnel"))
    return render_template("admin/add_admin.html", form=form)

@app.route("/delete_admin/<int:aid>", methods=["POST"])
def delete_admin_post(aid):
    return redirect(url_for("confirm_delete_admin", aid=aid))

@app.route("/confirm_delete_admin/<int:aid>", methods=["GET"])
def confirm_delete_admin(aid):
    admin = Admin.query.get_or_404(aid)
    return render_template("admin/confirm_delete_admin.html", admin=admin)

@app.route("/confirm_delete_admin/<int:aid>", methods=["POST"])
def confirm_delete_admin_post(aid):
    admin = Admin.query.get_or_404(aid)
    db.session.delete(admin)
    db.session.commit()
    return redirect(url_for("personnel"))

@app.route("/edit_admin/<int:aid>", methods=["GET", "POST"])
def edit_admin(aid):
    admin = Admin.query.get_or_404(aid)
    form = AdminForm(obj=admin)
    if form.validate_on_submit():
        admin.admin_name = form.admin_name.data
        admin.admin_email = form.admin_email.data
        admin.priviledge_level = form.priviledge_level.data
        db.session.commit()
        return redirect(url_for("personnel"))
    return render_template("admin/edit_admin.html", form=form)

@app.route('/updateBooking')
@login_required
def updateBooking(bid):
    room = db.Room()
    user = db.User()
    username = session['username'] if 'username' in session and session['username'] != '' else ''
    if request.method == "POST":
        b = dict()
        b['bid'] = bid
        # save the value of check_in_date
        previous_check_in_date = b.get('check_in_date')
        previous_check_out_date = b.get('check_out_date')
        previous_room = b.get('room-number')
        # Users update the check_in_date, check_out_date, room_number
        b['check_in_date'] = request.form['date'] if request.form['date'] != '' else previous_check_in_date
        b['check_out_date'] = request.form['date'] if request.form['date'] != '' else previous_check_out_date
        b['room_number'] = request.form['room_number'] if request.form['room_number'] != '' else previous_room
        if booking.Update(b):
            print('Update successully')
            return redirect(url_for('viewBooking', bid=b['bid'], username=username))
        else:
            print('Error')
            return redirect(url_for('updateBooking', bid=b['bid'], username=username))
    return render_template('')


# @app.route('/cancel_booking')
# @login_required
# def cancel_booking():
#     bid = session['bid'] if 'bid' in session and session['bid'] != '' else ''
#     if not booking:
#         return render_template('error.html', message="No booking found.")
#     booking = db.Booking()
#     current_date = datetime.date.today()
#     total_price = db.Booking()
#
#     # taking the  days check in and value price of booking
#     check_in_date = booking.check_in_date
#     # number of money which the cutomer need to pay
#     total_price = booking.total_price
#
#     # Calculate the number of days the customer which before check_in_date
#     days_until_check_in = (check_in_date - current_date).days
#     # Calculate the cancellation fee based on the number of days until check-in
#     if days_until_check_in < 30:
#         cancellation_fee = total_price
#     elif days_until_check_in < 60:
#         cancellation_fee = total_price * 0.5
#     elif days_until_check_in < 90:
#         cancellation_fee = 0
#
#     # Update the total price in the booking to the cancellation fee
#     booking.total_price = cancellation_fee
#     db.session.commit()
#
#     return render_template('cancalBooking.html', cancellation_fee=cancellation_fee)


# admin

@app.route('/adding')
@login_required
def addingHotel():
    return render_template('/addingHotel')


@app.route('/exchangeRate')
@login_required
def exchangeRate():
    return render_template('exchangeRate')


@app.route('/apdateHotel')
@login_required
def apdateHotel():
    return render_template('/apdateHotel')


@app.route('/updatePrice')
@login_required
def updatePrice():
    return render_template('updatePrice')


@app.route('/removeHotel')
@login_required
def removeHotel():
    return render_template('removeHotel')


@app.route("/hotels", methods=["GET"])
@app.route('/list', methods=["GET"])
def get_hotels():
    limit = request.args.get('limit', 7, type=int)
    hotels = Hotel.query.limit(limit).all()
    return render_template("hotels/list.html", hotels=hotels, limit=limit)


if __name__ == "__main__":
    for i in range(2000, 20000):
        try:
            app.run(debug=True, port=i)
            break
        except OSError as e:
            print(f"Port {i} not available")
