from config import db

class User (db.Model):

    # __table__ = "User"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(250), nullable = False)
    email = db.Column(db.String(250), unique = True, nullable = False)
    password = db.Column(db.String(250), nullable = False)

    def __repr__(self) :
        return f"User ('{self.id}','{self.name}','{self.email}')"