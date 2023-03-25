from config import db
from app import app
from models.users import User
from routes.authentification_route import Authentification

app.app_context().push()
db.create_all()


app.register_blueprint(Authentification)


if __name__ == '__main__' :

    app.run(debug= True)