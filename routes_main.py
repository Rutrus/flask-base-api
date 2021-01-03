from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index_login.html')


@main.route('/radar')
def radar():
    return render_template('index.html')

@main.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')

@main.route('/cookies-policy')
def cookies_policy():
    return render_template('cookies-policy.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.display_name)
