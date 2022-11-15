from flask_restful import Resource
from flask import jsonify,send_file,request
from services.interval_analysis_service import*
import json
from PIL import Image
from numpy import asarray

class IntervalAnalysis(Resource):
    def __init__(self) -> None:
        res = request.get_json()
        print(res)
        self.s = IntervalAnalysisService(str(res['model_name']),
                                            list(res['vars_initials']),
                                            list(res['params']),
                                            list(res['params_est']),
                                            int(res['t']),
                                            int(res['total_points']),
                                            str(res['method']),
                                            int(res['N']),
                                            list(res['params_min']), 
                                            list(res['params_max']),  
                                            str(res['interval_method']), 
                                            str(res['path']))
    
    def post(self):
        opt,sol = self.s.solve_model()
        img = Image.open('model.png')
        return json.dumps({'opt': opt, 'sol': sol.tolist(), 'img': asarray(img).tolist()})