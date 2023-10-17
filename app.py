from flask import Flask
from flask_migrate import Migrate
from flask_smorest import Api

from db import db
import os
from dotenv import load_dotenv
from resources.user import blp as user_blp
import redis
from rq import Queue

app = Flask(__name__)
migrate = Migrate(app, db)

load_dotenv()

connection = redis.from_url(
    os.getenv('REDIS_URL')
)
app.queue = Queue("emails", connection=connection)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning

db.init_app(app)

app.config['API_TITLE'] = os.getenv('API_TITLE')
app.config['API_VERSION'] = os.getenv('API_VERSION')
app.config['OPENAPI_VERSION'] = '3.0.2'
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

api = Api(app)  # Move this line here

api.register_blueprint(user_blp)

if __name__ == '__main__':
    app.run(debug=True)
