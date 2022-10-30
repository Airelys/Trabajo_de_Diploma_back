import enum
from business_logic.model import *

dict = {
    'SI': SI,
    'SIR': SIR,
    'SIRS': SIRS,
    'SEIR': SEIR
}


class SolveEpidemiologicalModelsService:
    def __init__(self,name_model,vars_initials,params,params_est,interval_est,t,total_points,method) -> None:
        self.name_model = name_model
        self.vars_initials = vars_initials
        self.params = params
        self.params_est = params_est
        self.interval_est = interval_est
        self.t = t
        self.total_points = total_points
        self.method = method

    def solve_model(self):
        model = dict[self.name_model](self.vars_initials,self.params,params_est=self.params_est)
        sol = model.numeric_solver([0,self.t],self.params,self.total_points,self.method)
        img = model.print_numeric_solve([0,self.t],self.params,self.total_points,self.method)
        return sol,img