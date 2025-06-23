from flask import Flask
from flask_restful import Api
from main.mensagers.whatsapp import Whatsapp


app = Flask(__name__)
api = Api(app)

api.add_resource(Whatsapp, '/pedraobot/whatsapp')
