from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required, login_user, logout_user
from flask_wtf import FlaskForm

from app.auth.forms import LoginForm, RegisterForm
from app.auth.models import User
from app.extensions import login_manager, db
from app.utils import flash_errors

blueprint = Blueprint("auth", __name__, url_prefix="/auth")

login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@blueprint.route("/")
@login_required
def index():
    users = User.query.all()
    return render_template("auth/index.html", users=users)


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


@blueprint.route("/logout", methods=["POST"])
@login_required
def logout():
    form = FlaskForm(request.form)
    if form.validate_on_submit():
        logout_user()
        return redirect(url_for("concept.index"))
    else:
        flash_errors(form)
        return redirect(url_for("concept.index"))


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            user = User(form.username.data, form.password.data)
            db.session.add(user)
            db.session.commit()

            login_user(user)
            flash(f"Created user with username {user.username}", "info")
            return redirect(url_for("auth.index"))
        else:
            flash_errors(form)
            return redirect(url_for("auth.register"))

    return render_template("auth/register.html", form=form)
