from flask_restful import Resource
from flask import jsonify,send_file,request
from services.parameter_estimation_service import*
import json
from PIL import Image
from numpy import asarray

class ParameterEstimation(Resource):
    def __init__(self) -> None:
        res = request.get_json()
        self.s = ParameterEstimationService(str(res['model_name']),
                                            list(res['vars_initials']),
                                            list(res['params']),
                                            list(res['params_est']),
                                            list(res['interval_est']),
                                            int(res['t']),
                                            int(res['total_points']),
                                            str(res['method']),
                                            int(res['N']),
                                            list(res['params_min']), 
                                            list(res['params_max']), 
                                            str(res['classical_method']), 
                                            str(res['metaheuristic']), 
                                            str(res['path']),
                                            int(res['iter']),
                                            int(res['particle']),
                                            float(res['cognitive']),
                                            float(res['social']),
                                            float(res['inercia']),
                                            float(res['population']),
                                            float(res['crossing']),
                                            float(res['scaled']))
    
    def post(self):
        opt,sol = self.s.solve_model()
        img = Image.open('model.png')
        return json.dumps({'opt': opt.tolist(), 'sol': sol.tolist(), 'img': asarray(img).tolist()})