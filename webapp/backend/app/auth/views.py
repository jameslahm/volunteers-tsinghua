from . import auth
from flask import render_template, redirect
from flask import flash, url_for
from flask import request
from flask_login import login_user, login_required, logout_user
from ..model import Team,IntroCode
from .. import db

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if(request.method == 'POST'):
        email = request.form.get('email')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me')
        team = Team.query.filter_by(email=email).first()
        print(team)
        if team is not None and team.verify_password(password):
            login_user(team, remember=remember_me)
            if team.is_administrator():
                return redirect(url_for('admin.index'))
            return redirect(request.args.get('next') or url_for('main.index'))
        flash("Invalid username or password")
    return render_template(
        'auth/login.html'
    )


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if(request.method=='POST'):
        code=request.form.get('introcode')
        email=request.form.get('email')
        username=request.form.get('username')
        password=request.form.get('password')
        team=Team.query.filter_by(email=email).first()
        if team is not None:
            flash('The email have been registered')
            return redirect(url_for('auth.login'))
        else:
            print(code)
            introcode=IntroCode.verify_code(code)
            print(introcode)
            if introcode is None:
                flash('Code is not correct')
            else:
                flash('You have registered successfully')
                team=Team(email=email,teamName=username,password=password)
                db.session.add(team)
                db.session.commit()
                login_user(team,remember=True)
                return redirect(url_for('main.index'))
    return render_template(
        'auth/register.html'
    )


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('auth.login'))


