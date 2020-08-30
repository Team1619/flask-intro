from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp

from app.auth.models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()
        if not self.user:
            self.username.errors.append("Username does not exist")
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append("Invalid password")
            return False

        return True


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3), Regexp("[a-zA-Z0-9]+")])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=40)])
    password_confirmation = PasswordField("Confirm password", validators=[
        DataRequired(), EqualTo("password", message="Passwords must match")])

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()
        if self.user:
            self.username.errors.append("Username already exists")
            return False

        return True
