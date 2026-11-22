"""Rate limits for the endpoints that can be abused (password guessing, email flooding).

Strict limits are keyed on the *account* (username or email in the request), so a whole classroom
sharing one school IP isn't locked out; per-IP limits are generous backstops.

Storage defaults to in-process memory. On Heroku each gunicorn worker keeps its own counts, so the
effective limit is (limit x workers). Set RATELIMIT_STORAGE_URI to a Redis URL to share counts.
"""
from flask import request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)


def json_field_key(field):
    """Rate-limit key from a JSON body field, e.g. the username being logged into."""
    def key():
        data = request.get_json(silent=True) or {}
        value = str(data.get(field) or '').strip().lower()
        # Fall back to the IP when the field is missing so empty requests still get limited
        return f'{field}:{value}' if value else f'ip:{get_remote_address()}'
    return key


TOO_MANY = "Too many attempts. Please wait a few minutes and try again."

# Each resource uses these as its `decorators` list (flask-restx applies them to every method)
LOGIN_LIMITS = [
    limiter.limit("10 per minute;50 per hour", key_func=json_field_key('username'), error_message=TOO_MANY),
    limiter.limit("100 per minute", error_message=TOO_MANY),
]
SIGNUP_LIMITS = [
    limiter.limit("60 per hour", error_message="Too many sign-ups from this network. Please try again later."),
]
ACCOUNT_EMAIL_LIMITS = [
    limiter.limit("3 per hour", key_func=json_field_key('email'),
                  error_message="We've already sent a few emails to that address. Please check your inbox (and spam) or try again in an hour."),
    limiter.limit("20 per hour", error_message=TOO_MANY),
]
VALIDATE_TOKEN_LIMITS = [limiter.limit("30 per minute", error_message=TOO_MANY)]
SET_PASSWORD_LIMITS = [limiter.limit("10 per minute", error_message=TOO_MANY)]
CONTACT_LIMITS = [
    limiter.limit("5 per hour", error_message="You've sent several messages already. Please try again in a little while."),
]
