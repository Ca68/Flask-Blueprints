from app import db
from datetime import datetime as dt

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=dt.utcnow)
    date_updated = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        from app.blueprints.authentication.models import User

        # To make this efficient, we're going to store the user inside of a variable so we don't have to make multiple db queries
        # just to propagate our user's information
        user = User.query.get(self.user_id)

        data = {
            'id': self.id,
            'body': self.body,
            'date_created': self.date_created,
            'date_updated': self.date_updated,
            'user': {
                'id': self.user_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
        }
        return data

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<Post: {self.body[:30]}>'


