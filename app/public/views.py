from flask import Blueprint, render_template

blueprint = Blueprint('public', __name__, url_prefix='/')


@blueprint.route("/")
def index():
    return render_template("public/index.html")
