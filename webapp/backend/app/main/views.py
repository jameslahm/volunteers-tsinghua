from flask import render_template,request,current_app
from . import main
from flask_login import login_required,current_user
from flask import redirect,url_for
from werkzeug import secure_filename
from ..model import Activity,UserActivity
from utils import md5
import os
from .. import db
import requests


@main.route('/', methods=['GET'])
@login_required
def index():
    if current_user.is_administrator():
        return redirect(url_for('admin.index'))
    return render_template(
        'profile.html',team=current_user
    )


@main.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template(
        'profile.html',team=current_user
    )


@main.route('/myactivity', methods=['GET'])
@login_required
def myactivity():
    page=request.args.get('page',1,type=int)
    pagination=Activity.query.filter_by(team=current_user).order_by(Activity.starttime.desc()).paginate(
        page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False
    )
    activities=pagination.items
    return render_template(
        'myactivity.html',activities=activities,pagination=pagination
    )


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

@main.route('/createactivity', methods=['GET', 'POST'])
@login_required
def createactivity():
    if request.method=='POST':
        title=request.form.get('title')
        location=request.form.get('location')
        startdate=request.form.get('startdate')
        enddate=request.form.get('enddate')
        starttime=request.form.get('starttime')
        endtime=request.form.get('endtime')
        totalRecruits=request.form.get('totalRecruits')
        content=request.form.get('content')
        managePerson=request.form.get('managePerson')
        manageEmail=request.form.get('manageEmail')
        managePhone=request.form.get('managePhone')
        thumb=request.files['thumb']
        if thumb and allowed_file(thumb.filename):
            filename = secure_filename(thumb.filename)
            thumb.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename).replace('\\','/'))
            file='/static/img/'+filename
        activity=Activity(title=title,location=location,starttime=startdate+" "+starttime,endtime=enddate+" "+endtime,totalRecruits=totalRecruits, \
            content=content,managePerson=managePerson,manageEmail=manageEmail,managePhone=managePhone,thumb=file,team=current_user)
        db.session.add(activity)
        db.session.commit()
        return redirect(url_for('main.myactivity'))
    return render_template(
        'createactivity.html'
    )



@main.route('/information', methods=['GET', 'POST'])
@login_required
def information():
    return render_template(
        'information.html'
    )

@main.route('/verifyThu<ticket>', methods=['GET'])
def verify_thu(ticket):
    AppID = 'wxf3aa74b41b1f555c'
    ticket = str(ticket).replace('?ticket=', '')

    get_ip = requests.get("http://www.baidu.com", stream=True)
    user_ip_address = get_ip.raw._connection.sock.getsockname()[0]
    user_ip_address = str(user_ip_address).replace('.', '_')
    get_ip.close()

    verify_url = 'https://alumni-test.iterator-traits.com/fake-id-tsinghua/thuser/authapi/checkticket/{}/{}/{}'.format(
        AppID, ticket, user_ip_address
    )
    return requests.get(verify_url).json()
    # return render_template(
    #     'profile.html', user_info=requests.get(verify_url).json()
    # )
    # rsp = requests.get(verify_url)
    # redirect('/profile')
    # return rsp.json()


@main.route('/tsinghua')
def login_thu():
    AppID = 'wxf3aa74b41b1f555c'
    SEQ = '669223961b70204ffbd023015ea9decb'
    returnurl = 'auth.verify_thu'
    url = 'https://alumni-test.iterator-traits.com/fake-id-tsinghua/do/off/ui/auth/login/form/{}/{}?/{}'.format(
        md5(AppID), SEQ, returnurl
    )
    return redirect(url)
