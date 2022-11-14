from flask_restful import Resource
from flask import jsonify,send_file,request
from services.solve_epidemiological_models_service import*
import json
from PIL import Image
from numpy import asarray

class SolveEpidemiologicalModels(Resource):
    def __init__(self) -> None:
        res = request.get_json()
        print(res)
        self.s = SolveEpidemiologicalModelsService(str(res['model_name']),
                                                   list(res['vars_initials']),
                                                   list(res['params']),
                                                   list(res['params_est']),
                                                   int(res['t']),
                                                   int(res['total_points']),
                                                   str(res['method']), int(res['N']))
        print('aaaaaaaaaaaaaaaaaaaaaaa')
    
    def post(self):
        sol = self.s.solve_model()
        img = Image.open('model.png')
        return json.dumps({'sol': sol.tolist(), 'img': asarray(img).tolist()})
        

#bool para intervalos