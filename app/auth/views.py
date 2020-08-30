from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_required, login_user

from app.auth.forms import LoginForm
from app.auth.models import User
from app.extensions import login_manager
from app.utils import flash_errors

blueprint = Blueprint("auth", __name__, url_prefix="/auth")

login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@blueprint.route("/")
@login_required
def index():
    return render_template("auth/index.html")


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            login_user(form.user)
            return redirect(url_for("auth.index"))
        else:
            flash_errors(form)
            return redirect(url_for("auth.login"))

    return render_template("auth/login.html", form=form)
