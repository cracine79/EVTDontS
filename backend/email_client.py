"""Send email through Resend's HTTP API (https://resend.com/docs/api-reference/emails/send-email).

Needs RESEND_API_KEY in the environment (backend/.env locally, `heroku config:set` in production).
The sender address must be on a domain verified in Resend (evtds.com).
"""
import json
import os
import urllib.error
import urllib.request

RESEND_URL = 'https://api.resend.com/emails'
DEFAULT_SENDER = "Economics Videos That Don't Suck <admin@evtds.com>"
ADMIN_EMAIL = 'admin@evtds.com'


class EmailError(Exception):
    pass


def send_email(to, subject, html, reply_to=None, sender=DEFAULT_SENDER):
    """Send one email. Raises EmailError if Resend rejects it or can't be reached."""
    api_key = os.environ.get('RESEND_API_KEY')
    if not api_key:
        raise EmailError('RESEND_API_KEY is not set')

    payload = {
        'from': sender,
        'to': [to] if isinstance(to, str) else list(to),
        'subject': subject,
        'html': html,
    }
    if reply_to:
        payload['reply_to'] = reply_to

    req = urllib.request.Request(
        RESEND_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'evtds-app/1.0',
        },
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode('utf-8') or '{}')
            print(f"Email sent to {payload['to']} (id {result.get('id')})")
            return result
    except urllib.error.HTTPError as e:
        detail = e.read().decode('utf-8', 'replace')
        print(f'Error sending email: HTTP {e.code}: {detail}')
        raise EmailError(f'Resend returned HTTP {e.code}: {detail}') from e
    except urllib.error.URLError as e:
        print(f'Error sending email: {e.reason}')
        raise EmailError(f'Could not reach Resend: {e.reason}') from e
