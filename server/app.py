from flask import Flask
from auth import auth_api
from team import team_api
from individual import individual_api
from config import DEBUG

from firebase_admin import credentials
from firebase_admin import firestore

app = Flask(__name__)
app.register_blueprint(auth_api, url_prefix='/auth')
app.register_blueprint(team_api, url_prefix='/team')
app.register_blueprint(individual_api, url_prefix='/individual')

@app.route("/")
def hello():
    return "Hello world"

if __name__ == "__main__":
    app.run(debug=DEBUG)