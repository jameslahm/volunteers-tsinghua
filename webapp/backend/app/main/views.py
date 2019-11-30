from flask import render_template,request,current_app
from . import main
from flask_login import login_required,current_user
from flask import redirect,url_for
from ..model import Activity,UserActivity


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
    # page=request.args.get('page',1,type=int)
    page=1
    pagination=Activity.query.filter_by(team=current_user).order_by(Activity.starttime.desc()).paginate(
        page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False
    )
    activities=pagination.items
    return render_template(
        'myactivity.html',activities=activities,pagination=pagination
    )

@main.route('/createactivity', methods=['GET', 'POST'])
@login_required
def createactivity():
    return render_template(
        'createactivity.html'
    )



@main.route('/information', methods=['GET', 'POST'])
@login_required
def information():
    return render_template(
        'information.html'
    )

