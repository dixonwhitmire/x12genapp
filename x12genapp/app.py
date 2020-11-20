from flask import Flask
from x12genapp.api import api_blueprint

app = Flask(__name__, instance_relative_config=True)
app.register_blueprint(api_blueprint, url_prefix='/genapp')
