from flask_restful import Resource
from flask_jsonpify import jsonify
from services.solve_epidemiological_models_service import*

class SolveEpidemiologicalModels(Resource):
    def __init__(self,name,vars_initials,params,params_est,interval_est,t,total_points,method) -> None:
        self.model = SolveEpidemiologicalModelsService(name,vars_initials,params,params_est,interval_est,t,total_points,method)

    def solve(self):
        sol,img = self.model.solve_model()
        return jsonify({'sol':sol,'img':img})
        

    