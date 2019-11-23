from flask import render_template
from . import main

@main.route('/', methods=['GET'])
def index():
    return render_template(
        'profile.html'
    )


@main.route('/myactivity', methods=['GET'])
def myactivity():
    return render_template(
        'myactivity.html'
    )


@main.route('/createactivity', methods=['GET', 'POST'])
def createactivity():
    return render_template(
        'createactivity.html'
    )


@main.route('/information', methods=['GET', 'POST'])
def information():
    return render_template(
        'information.html'
    )

