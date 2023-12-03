from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager


from .blueprints.site.routes import site
from .blueprints.auth.routes import auth
from .blueprints.api.routes import api
from config import Config
from .models import db, login_manager
from .helpers import JSONEncoder


app = Flask(__name__)
app.config.from_object(config)
jwt = JWTManager(app)


login_manager.init_app(app)
login_manager.login_view ='auth.signin'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Please sign in to access this page.'


# @app.route("/")
# def hello_world():
#    return "<p>Hello, World!</P>"

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)



db.init_app(app)
migrate = Migrate(app, db)
app.json_encoder = JSONEncoder
cors = CORS(app)

