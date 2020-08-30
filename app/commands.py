import click
from flask.cli import with_appcontext
from sqlalchemy.orm import joinedload

from app.auth.models import User
from app.extensions import db
from app.concepts.models import Concept, UserConceptProgress, Category


@click.command('db-init')
@with_appcontext
def db_init():
    db.drop_all()
    db.create_all()

    alice = User('alice', 'password')
    bob = User('bob', '123456')
    chad = User('chad', 'hunter2')

    db.session.add(alice)
    db.session.add(bob)
    db.session.add(chad)
    db.session.commit()

    tool_category = Category(name='Tools')

    db.session.add(tool_category)
    db.session.commit()

    pycharm = Concept(category_id=tool_category.id, name='PyCharm')
    terminal = Concept(category_id=tool_category.id, name='Terminal')
    git = Concept(category_id=tool_category.id, name='Git')

    db.session.add(pycharm)
    db.session.add(terminal)
    db.session.add(git)
    db.session.commit()

    progress_entries = [
        UserConceptProgress(user_id=alice.id, concept_id=pycharm.id, progress='completed'),
        UserConceptProgress(user_id=alice.id, concept_id=git.id, progress='completed'),
        UserConceptProgress(user_id=alice.id, concept_id=terminal.id, progress='started'),

        UserConceptProgress(user_id=bob.id, concept_id=pycharm.id, progress='completed'),
        UserConceptProgress(user_id=bob.id, concept_id=terminal.id, progress='started'),

        UserConceptProgress(user_id=chad.id, concept_id=pycharm.id, progress='started'),
    ]

    for entry in progress_entries:
        db.session.add(entry)
    db.session.commit()


@click.command('print-concepts')
@with_appcontext
def print_concepts():
    concepts = db.session.query(Concept).options(joinedload(Concept.category)).all()
    for concept in concepts:
        print(concept.category.name)
        print(concept.name)
