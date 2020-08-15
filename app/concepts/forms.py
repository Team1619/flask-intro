from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class NewCategoryForm(FlaskForm):
    category = StringField("Category", validators=[DataRequired(), Length(min=3, max=128)])


class NewConceptForm(FlaskForm):
    category = StringField("Category", validators=[DataRequired(), Length(min=3, max=128)])
    concept = StringField("Concept", validators=[DataRequired(), Length(min=3, max=128)])
