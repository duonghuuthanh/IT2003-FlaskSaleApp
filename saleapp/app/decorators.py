from functools import wraps
from flask import redirect
from flask_login import current_user


def annonymous_user(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect("/")

        return f(*args, **kwargs)

    return decorated_func