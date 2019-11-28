from flask import render_template
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
    activities=Activity.query.filter_by(team=current_user).all()
    return render_template(
        'myactivity.html',activities=activities
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

