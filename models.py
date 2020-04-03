from app import db

class Roll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(64), index=True, unique=True)
    die = db.Column(db.Integer, index=False, unique=False)
    result = db.Column(db.Integer, index=False, unique=False)

    def __repr__(self):
        return '<User {}>'.format(self.name)