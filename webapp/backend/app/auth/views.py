from . import auth
from flask import render_template

@auth.route('/login', methods=['GET'])
def login():
    return render_template(
        'login.html'
    )


@auth.route('/signup', methods=['GET'])
def signup():
    return render_template(
        'signup.html'
    )
