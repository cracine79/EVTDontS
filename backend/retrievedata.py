import os
from flask_restx import Namespace, Resource
from flask import request, jsonify, current_app
from models import User
from itsdangerous import URLSafeTimedSerializer
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


retrieve_ns = Namespace('retrieve', description = 'A namespace for data retrieval')

def generate_reset_token(email, secret_key, salt):
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(email, salt=salt)

def send_reset_email(email, token, domain, sender_email, username):
    print('APIKKKKEY', os.environ.get('SENDGRID_API_KEY'))
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

@retrieve_ns.route('/password')
class RetrievePassword(Resource):
    def post(self):
        app_domain = current_app.config['APP_DOMAIN']
       
        data=request.get_json()
        email = data.get('email')
        token = generate_reset_token(email, current_app.config['SECRET_KEY'], 'password-reset-salt')
        user = User.query.filter_by(email = email).first()

        if user is None:
            print('no user')
            return({"message": f"There is no current user with the email address: {email} on file.  Please check"}), 404
        else:
            username = user.username
            try:
               
                send_reset_email(email, token, app_domain, 'admin@evtds.com', username)
                return ({"message": "Password reset email sent"}), 200
            except Exception as e:
                return ({"error": "Failed to send email"}), 500