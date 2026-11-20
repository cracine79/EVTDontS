from html import escape

from flask import request
from flask_restx import Namespace, Resource

from email_client import ADMIN_EMAIL, EmailError, send_email

mail_ns = Namespace('mail', description = "A namespace for mail")


def send_mail(subject, email, body, sender_email=ADMIN_EMAIL):
    """Contact form: forward a visitor's message to the site's inbox. Replying goes to the visitor."""
    # Everything here is typed by a visitor, so escape it before putting it in HTML
    send_email(
        to=sender_email,
        subject=f"EVTDS EMAIL from {email}"[:200],
        reply_to=email if email and '@' in email else None,
        html=f"""
        <p>You have received an email from {escape(email or '')}</p>
        <p>The Subject Is</p>
        <p>{escape(subject or '')}</p>
        <p>The content is:</p>
        <p style="white-space: pre-line">{escape(body or '')}</p>
        """,
    )


@mail_ns.route('/send')
class SendMail(Resource):
    def post(self):
        data = request.get_json() or {}
        email = data.get('email')
        body = data.get('body')
        subject = data.get('subject')

        try:
            send_mail(subject, email, body)
            return({"message":"Email Sent Successfully"}), 200
        except EmailError:
            return ({"error": "Failed to send email !"}), 500
