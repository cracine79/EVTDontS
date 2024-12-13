import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Debug environment variable

message = Mail(
    from_email='admin@evtds.com',
    to_emails='willemdefoexxx@gmail.com',
    subject='Testes Testes, One, Two, Three?',
    html_content='Hehe, hehe, hehe, hehe, heell yeah bro! For RIzzy')

try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)

except Exception as e:
    print("Error:", str(e))
