from flask import render_template,request,current_app, jsonify
from . import main
from flask_login import login_required,current_user
from flask import redirect,url_for
from werkzeug import secure_filename
from ..model import Activity,UserActivity,Team
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
        if(password):
            team.password=password
        team.description=description
        avatar=request.files['avatar']
        if avatar and allowed_file(avatar.filename):
            filename = secure_filename(avatar.filename)
            if(filename.find('.')!=-1):
                filename='teamavatar_'+str(team.id)+'_'+filename
            else:
                filename='teamavatar_'+str(team.id)+'_.'+filename
            avatar.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename).replace('\\','/'))
            file='/static/img/'+filename
            team.avatar=file
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
        id=request.form.get('id')
        content=request.form.get('content')
        activitie=Activity.query.filter_by(id=id).first()
        activitie.starttime=starttime
        activitie.managePerson=managePerson
        activitie.managePhone=managePhone
        activitie.content=content

        thumb=request.files['thumb']
        qrcode=request.files['qrcode']
        if thumb and allowed_file(thumb.filename):
            filename = secure_filename(thumb.filename)
            if(filename.find('.')!=-1):
                filename='activitythumb_'+str(activitie.id)+'_'+filename
            else:
                filename='activitythumb_'+str(activitie.id)+'_.'+filename
            thumb.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename).replace('\\','/'))
            file='/static/img/'+filename
            activitie.thumb=file
        if qrcode and allowed_file(qrcode.filename):
            filename = secure_filename(qrcode.filename)
            if(filename.find('.')!=-1):
                filename='activityqrcode_'+str(activitie.id)+'_'+filename
            else:
                filename='activityqrcode_'+str(activitie.id)+'_.'+filename
            qrcode.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename).replace('\\','/'))
            qrcode='/static/img/'+filename
            activitie.qrcode=qrcode
        db.session.commit()
    
    page=request.args.get('page',1,type=int)
    pagination=Activity.query.filter_by(team=current_user).order_by(Activity.starttime.desc()).paginate(
        page,per_page=current_app.config['FLASK_ACTIVITY_PER_PAGE'],error_out=False
    )
    activities=pagination.items
    return render_template(
        'myactivity.html',activities=activities,pagination=pagination,team=current_user
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
        qrcode=request.files['qrcode']
        type='creating'
        first=Activity.query.order_by(Activity.id.desc()).first()
        if first:
            id=first.id+1
        else:
            id=1
        if thumb and allowed_file(thumb.filename):
            filename = secure_filename(thumb.filename)
            if(filename.find('.')!=-1):
                filename='activitythumb_'+str(id)+'_'+filename
            else:
                filename='activitythumb_'+str(id)+'_.'+filename
            thumb.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename).replace('\\','/'))
            file='/static/img/'+filename
        else:
            file=None
        if qrcode and allowed_file(qrcode.filename):
            filename = secure_filename(qrcode.filename)
            if(filename.find('.')!=-1):
                filename='activitythumb_'+str(id)+'_'+filename
            else:
                filename='activitythumb_'+str(id)+'_.'+filename
            qrcode.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename).replace('\\','/'))
            qrcode='/static/img/'+filename
        else:
            qrcode=None
        activity=Activity(title=title,location=location,starttime=startdate+" "+starttime,endtime=enddate+" "+endtime,totalRecruits=totalRecruits, \
            content=content,managePerson=managePerson,manageEmail=manageEmail,managePhone=managePhone,thumb=file,team=current_user,type=type,qrcode=qrcode)
        db.session.add(activity)
        db.session.commit()
        return redirect(url_for('main.myactivity'))
    return render_template(
        'createactivity.html',team=current_user
    )



@main.route('/information', methods=['GET', 'POST'])
@login_required
def information():
    activities=Activity.query.filter_by(team=current_user).order_by(Activity.isRead).all()
    return render_template(
        'information.html',activities=activities,team=current_user,UserActivity=UserActivity
    )

