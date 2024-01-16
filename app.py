from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from twilio.rest import Client
from decouple import config
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/db5'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Load Twilio credentials from environment variables
account_sid = config('TWILIO_ACCOUNT_SID')
auth_token = config('TWILIO_AUTH_TOKEN')
twilio_phone_number = config('TWILIO_PHONE_NUMBER')

app.template_folder = 'templates'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    verification_code = db.Column(db.String(6))

# Create tables
with app.app_context():
    db.create_all()

# Function to send SMS verification code using Twilio
def send_sms_verification_code(phone, code):
    phone_number = f"+91{phone}"
    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            to=phone,
            from_=twilio_phone_number,
            body=f'Your verification code is: {code}'
        )

        print(f"Verification code sent successfully to {phone}")
    except Exception as e:
        print(f"Error sending verification code to {phone}: {e}")

@app.route('/')
def index():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['password']

    # Generate a random verification code
    verification_code = secrets.token_hex(3).upper()

    # Hash the password before storing it
    #hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    new_user = User(username=username, email=email, phone=phone, password=password, verification_code=verification_code)

    try:
        db.session.add(new_user)
        db.session.commit()

        # Send SMS verification code
        send_sms_verification_code(phone, verification_code)

        # Redirect to the verification page
        return redirect(url_for('verify'))
    except Exception as e:
        print(f"Error committing to the database: {e}")
        db.session.rollback()  # Rollback the transaction in case of an error
        return "Error during signup"

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        entered_code = request.form['verification_code']

        # Retrieve the user by verification code
        user = User.query.filter_by(verification_code=entered_code).first()

        if user:
            # Verification successful, you can update the user's status or perform other actions
            return f"Verification successful for user: {user.username}"

    return render_template('verification.html')

if __name__ == '__main__':
    app.run(debug=True)
