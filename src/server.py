from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
from controllers.solve_epidemiological_models import*

app = Flask(__name__)
api = Api(app)

CORS(app)

@app.route("/")
def home():
    return jsonify({'text':'Wellcome to EaglePro!!'})

api.add_resource(SolveEpidemiologicalModels, '/SolveEpidemiologicalModels')

if __name__ == '__main__':
   app.run(port=8000)