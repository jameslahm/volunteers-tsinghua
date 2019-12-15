from . import auth
from flask import render_template, redirect
from flask import flash, url_for
from flask import request
from flask_login import login_user, login_required, logout_user
from ..model import Team,IntroCode
from .. import db
from ..email import send_mail

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
            if not introcode:
                flash('Code is not valid')
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

@auth.route('/reset',methods=['GET','POST'])
def password_reset_request():
    if(request.method=='POST'):
        email=request.form.get('email')
        team=Team.query.filter_by(email=email).first()
        token=team.generate_reset_token(3600)
        send_mail(team.email,'Reset your Password','auth/email/reset_password',team=team,token=token)
        flash('An email with instructions to reset your password has been sent to you')
        return redirect(url_for('auth.login'))
    else:
        return render_template('auth/password_reset_request.html')

@auth.route('/reset/<token>',methods=['GET','POST'])
def password_reset(token):
    team=Team.verify_reset_token(token)
    if(request.method=='GET'):
        return render_template('auth/password_reset.html')
    else:
        if(team):
            team.password=request.form.get('password')
            if(request.form.get('email')==team.email):
                db.session.commit()
                flash('Your password has been updated')
            else:
                flash('Email not correct')
                return redirect(url_for('auth.login'))
        return redirect(url_for('auth.login'))