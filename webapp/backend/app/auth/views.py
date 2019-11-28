from . import auth
from flask import render_template, redirect
from flask import flash, url_for
from flask import request
from flask_login import login_user, login_required, logout_user
from ..model import Team,IntroCode
from .. import db
from utils import md5
import requests

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if(request.method == 'POST'):
        email = request.form.get('email')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me')
        team = Team.query.filter_by(email=email).first()
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
                team=Team(email=email,userName=username,password=password)
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


@auth.route('/auth/verifyThu<ticket>', methods=['GET'])
def verify_thu(ticket):
    AppID = 'ZHIZAITSINGHUA'
    ticket = str(ticket).replace('?ticket=', '')

    get_ip = requests.get("http://www.baidu.com", stream=True)
    user_ip_address = get_ip.raw._connection.sock.getsockname()[0]
    user_ip_address = str(user_ip_address).replace('.', '_')
    get_ip.close()

    verify_url = 'https://alumni-test.iterator-traits.com/fake-id-tsinghua/thuser/authapi/checkticket/{}/{}/{}'.format(
        AppID, ticket, user_ip_address
    )
    rsp = requests.get(verify_url)
    redirect('/profile')
    return rsp.json()


@auth.route('/auth/tsinghua')
def login_thu():
    AppID = 'ZHIZAITSINGHUA'
    SEQ = 0
    returnurl = 'auth.verify_thu'
    url = 'https://alumni-test.iterator-traits.com/fake-id-tsinghua/do/off/ui/auth/login/form/{}/{}?/{}'.format(
        md5(AppID), SEQ, returnurl
    )
    return redirect(url_for(url))
