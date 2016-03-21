from functools import wraps
from flask import redirect, url_for, request
from flask import session as login_session
from flask import abort


# Protect against csrf
def csrf_protect(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == "POST":
            token = login_session.pop('_csrf_token', None)
            if not token or token != request.form.get('_csrf_token'):
                abort(403)
        return f(*args, **kwargs)
    return decorated_function
