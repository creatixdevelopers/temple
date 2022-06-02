from flask import redirect, url_for, render_template

from app.utils import current_user
from . import dashboard


@dashboard.get('/login/')
def login():
    if (user := current_user()) and user.role.name == 'admin':
        return redirect(url_for('dashboard.index'))
    return render_template('dashboard/auth/index.html')


@dashboard.get('/forgot-password/')
def forgot_password():
    if (user := current_user()) and user.role.name == 'admin':
        return redirect(url_for('dashboard.index'))
    return render_template('dashboard/auth/forgot_password.html')


@dashboard.get('/reset-password/<string:token>/')
def reset_password(token: str):
    if (user := current_user()) and user.role.name == "admin":
        return redirect(url_for('dashboard.index'))
    return render_template('dashboard/auth/reset_password.html', token=token)
