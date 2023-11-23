from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy
from time import sleep
from random import randint

from raft import Raft
from models.database import db
from models.car import Car

SWAGGER_URL="/swagger"
API_URL="/static/swagger.json"

service_info = {
  "host": "127.0.0.1",
  "port": 8222
}

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
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///car_MD.db'
  db.init_app(app)
  return app

if __name__ == '__main__':
  app = create_app()
  sleep(randint(1, 5))
  crud = Raft(service_info).create_server()
  import routes
  app.run(service_info["host"], service_info["port"])