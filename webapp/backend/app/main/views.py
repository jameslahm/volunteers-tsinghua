from flask import render_template
from . import main
from flask_login import login_required,current_user
from flask import redirect,url_for


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
        'profile.html'
    )


@main.route('/myactivity', methods=['GET'])
@login_required
def myactivity():
    return render_template(
        'myactivity.html'
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

