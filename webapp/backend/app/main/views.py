from flask import render_template,request,current_app, jsonify
from . import main
from flask_login import login_required,current_user
from flask import redirect,url_for
from werkzeug import secure_filename
from ..model import Activity,UserActivity,Team
from ..utils.functions import md5
import os
from .. import db
import requests


@main.route('/', methods=['GET','POST'])
@login_required
def index():
    if current_user.is_administrator():
        return redirect(url_for('admin.index'))
    if(request.method=='POST'):
        teamName=request.form.get('teamName')
        phone=request.form.get('phone')
        password=request.form.get('password')
        description=request.form.get('description')
        team=current_user
        team.teamName=teamName
        team.phone=phone
        team.password=password
        team.description=description
        db.session.commit()
    return render_template(
        'profile.html',team=current_user
    )


@main.route('/myactivity', methods=['GET','POST'])
@login_required
def myactivity():
    if(request.method=='POST'):
        starttime=request.form.get('starttime')
        managePerson=request.form.get('managePerson')
        managePhone=request.form.get('managePhone')
        team=current_user
        team.starttime=starttime
        team.managePerson=managePerson
        team.managePhone=managePhone
        db.session.commit()
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
        else:
            file=None
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


@main.route('/verifyThu', methods=['GET', 'POST'])
def verifyThu():
    ticket = request.args.get('ticket')

    get_ip = requests.get("http://www.baidu.com", stream=True)
    user_ip_address = get_ip.raw._connection.sock.getsockname()[0]
    user_ip_address = str(user_ip_address).replace('.', '_')
    get_ip.close()

    AppID = 'A16'
    verify_url = 'https://alumni-test.iterator-traits.com/fake-id-tsinghua/thuser/authapi/checkticket/{}/{}/{}'.format(
        AppID, ticket, user_ip_address
    )
    rsp = requests.get(verify_url)

    result = str(rsp).split(':')
    info = {'code': result[0][5:], 'zjh': result[1][4:], 'yhm': result[2][4:], 'xm': result[3][3:],
            'yhlb': result[4][5:], 'dw': result[5][3:], 'email': result[6][6:]}

    return jsonify(info)

    # return render_template(
    #     'profile.html', user_info=requests.get(verify_url).json()
    
    # )


@main.route('/tsinghua')
def login_thu():
    AppID = 'A16'
    SEQ = '669223961b70204ffbd023015ea9decb'
    returnurl = 'verifyThu'
    url = 'https://alumni-test.iterator-traits.com/fake-id-tsinghua/do/off/ui/auth/login/form/{}/{}?{}'.format(
        md5(AppID), SEQ, returnurl
    )
    return redirect(url)
