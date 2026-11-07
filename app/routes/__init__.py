from functools import wraps
from flask import abort, flash, redirect, session, url_for


def current_user():
    return {"role": session.get("role"), "id": session.get("uid")}


def role_required(*roles):
    """Server-side authorization on every protected route."""
    def deco(fn):
        @wraps(fn)
        def wrapper(*a, **k):
            if "role" not in session:
                flash("Please log in first.", "error")
                return redirect(url_for("main.login"))
            if session["role"] not in roles:
                abort(403)
            return fn(*a, **k)
        return wrapper
    return deco
