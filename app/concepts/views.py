from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.orm import joinedload

from app.concepts.forms import NewCategoryForm
from app.concepts.models import Concept, Category
from app.extensions import db


blueprint = Blueprint('concept', __name__, url_prefix='/concepts')


@blueprint.route('/')
def index():
    items = []
    concepts = db.session.query(Concept).options(joinedload(Concept.category)).all()
    for concept in concepts:
        items.append([concept.category.name, concept.name])

    return render_template('concepts/index.html', items=items)


@blueprint.route('/create-category', methods=['GET', 'POST'])
def create_category():
    form = NewCategoryForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            category = Category(name=form.category.data)
            db.session.add(category)
            db.session.commit()
            flash(f"Created a category named {category.name}", "success")
            return redirect(url_for("concept.index"))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{getattr(form, field).label.text} - {error}", "danger")
            return redirect(url_for("concept.create_category"))

    return render_template('concepts/create-category.html', form=form)
