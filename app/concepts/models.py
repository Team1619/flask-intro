from app.extensions import db


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    concepts = db.relationship('Concept', backref='category', lazy=True)


class Concept(db.Model):
    __tablename__ = 'concepts'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    name = db.Column(db.String(128))


class UserConceptProgress(db.Model):
    __tablename__ = 'user_concept_progress'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    concept_id = db.Column(db.Integer, db.ForeignKey('concepts.id'), primary_key=True)
    progress = db.Column(db.String)
