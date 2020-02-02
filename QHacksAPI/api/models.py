from . import db

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100))
    response = db.Column(db.String(100))
    score = db.Column(db.Integer)
