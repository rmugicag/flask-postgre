from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=db.func.current_timestamp())

    @classmethod
    def create(cls, user):
        new_user = User(email=user["email"],
                        password=user["password"],
                        name=user["name"])
        return new_user.save()

    def update(self):
        self.save()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()

            return self
        except:
            return False

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()

            return True
        except:
            return False

    def to_json(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "name": self.name,
            "created_at": self.created_at
        }
