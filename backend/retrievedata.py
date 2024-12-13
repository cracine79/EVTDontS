import os
from flask_restx import Namespace, Resource
from flask import request, jsonify, current_app
from models import User
from itsdangerous import URLSafeTimedSerializer
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from werkzeug.security import generate_password_hash, check_password_hash
from exts import db


retrieve_ns = Namespace('retrieve', description = 'A namespace for data retrieval')

def generate_reset_token(email, secret_key, salt):
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(email, salt=salt)

def send_reset_email(email, token, domain, sender_email, username):
    reset_url = f"{domain}/reset-password?token={token}"
    message = Mail(
        from_email=sender_email,
        to_emails=email,
        subject="Password Reset Request",
        html_content=f"""
        <p>Hello, {username}</p>
        <p>We received a request to reset your password. If you made this request, please click the link below:</p>
        <a href="{reset_url}">Reset Your Password </a>
        <p>If you did not request a password reset, you can safely ignore this email.</p>
        <p>Thanks,</p>
        <p>EVTDS Help</p>

        """
    )

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(f"EMail sent!  Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")
        raise e

def send_username_email(email, sender_email, username):
    message = Mail(
        from_email = sender_email,
        to_emails = email,
        subject="EVTDS Username Retrieval",
        html_content=f"""
        <p>Hello,</p>
        <p>We have recieved a request to retrieve your username for www.evtds.com.  We're not judging you.</p>
        <p>Your username is:</p>
        <p>{username}<p>
        <p>If you did not request an email with your username, then you can safely ignore this email and go about your day.</p>
        <p>Thanks,</p>
        <p>EVTDS Help</p>
        """
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(f"EMail sent!  Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")
        raise e
    

def verify_reset_token(token, secret_key, salt, max_age=3600):
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        email=serializer.loads(token, salt=salt, max_age=max_age)
        return email
    except Exception as e:
        print(f"Token verification error: {e}")
        return None
    
@retrieve_ns.route('/username')
class RetrieveUsername(Resource):
    def post(self):
        data=request.get_json()
        email = data.get('email')
        user = User.query.filter_by(email=email).first()

        if user is None:
            return({"message": f"There is no current user with the email address: {email} on file.  Please check"}), 404
        else:
            username = user.username
            try:
                send_username_email(email, 'admin@evtds.com', username)
                return ({"message": "Username retrieval email sent"}), 200
            except Exception as e:
                return ({"error": "Failed to send email"}), 500

@retrieve_ns.route('/password')
class RetrievePassword(Resource):
    def post(self):
        app_domain = current_app.config['APP_DOMAIN']
       
        data=request.get_json()
        email = data.get('email')
        token = generate_reset_token(email, current_app.config['SECRET_KEY'], 'password-reset-salt')
        user = User.query.filter_by(email = email).first()

        if user is None:
            return({"message": f"There is no current user with the email address: {email} on file.  Please check"}), 404
        else:
            username = user.username
            try:
                send_reset_email(email, token, app_domain, 'admin@evtds.com', username)
                return ({"message": "Password reset email sent"}), 200
            except Exception as e:
                return ({"error": "Failed to send email"}), 500

            
@retrieve_ns.route('/validate-token')
class ValidateToken(Resource):
    def post(self):
        data = request.get_json()
        token = data.get('token')
        email = verify_reset_token(token, secret_key = current_app.config['SECRET_KEY'], salt='password-reset-salt')

        if email:
            return ({"message": "Token is valid", "email": email}), 200
        else:
            return({"error": "Invalid or expired token"}), 400


@retrieve_ns.route('/reset-password')
class ResetPassword(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email = email).first()

        if user is None:
            return({"message": f"There is an error finding the user associated with this password reset request"}), 404
        else:
            password_hash = generate_password_hash(password)
            user.password_hash = password_hash
            db.session.commit()
            return ({"message": "Password successfully updated!"}), 200