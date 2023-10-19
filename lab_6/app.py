from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy

from models.database import db
from models.car import Car

SWAGGER_URL="/swagger"
API_URL="/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
  SWAGGER_URL,
  API_URL,
  config = {
    'app_name': 'Access API'
  }
)

def create_app():
  app = Flask(__name__)
  app.register_blueprint(swagger_ui_blueprint, url_prefix = SWAGGER_URL)

  # Configure SQLAlchemy to use SQLite
  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/cars'
  db.init_app(app)
  return app

if __name__ == '__main__':
  app = create_app()
  import routes
  app.run()