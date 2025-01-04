import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask_restx import Namespace, Resource
from flask import request, jsonify, current_app

mail_ns = Namespace('mail', description = "A namespace for mail")

def send_mail(subject, email, body, sender_email):
    message = Mail(
        from_email = sender_email, 
        to_emails =sender_email,
        subject=f"EVTDS EMAIL from {email}",
        html_content=f"""
        <p>You have received an email from {email}</p>
        <p>The Subject Is</p>
        <p>{subject}</p>
        <p>The content is:</p>
        <p>{body}</p>
        """
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(f"Email sent!  Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")
        raise e
    
@mail_ns.route('/send')
class SendMail(Resource):
    def post(self):
        data=request.get_json()
        email = data.get('email')
        body = data.get('body')
        subject = data.get('subject')

        try:
            send_mail(subject, email, body, 'admin@evtds.com')
            return({"message":"Email Sent Successfully"}), 200
        except Exception as e:
            return ({"error": "Failed to send email !"}), 500
    


# Debug environment variable

# message = Mail(
#     from_email='admin@evtds.com',
#     to_emails='charleelracine@gmail.com',
#     subject='Test',
#     html_content='Does it work?')

# try:
#     sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
#     response = sg.send(message)

# except Exception as e:
#     print("Error:", str(e))
