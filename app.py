from flask import Flask
from flask_migrate import Migrate
from config import Config
from models.User import db
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

# Configuração do Flask-CORS
CORS(app, origins=["http://localhost:3000", "http://localhost:5003"])

db.init_app(app)
migrate = Migrate(app, db)

def register_routes(app):
    from routes.users import register_auth_routes
    register_auth_routes(app)

register_routes(app)

if __name__ == '__main__':
    app.run()