from business_logic.model import *

dict = {
    'SI': SI,
    'SIR': SIR,
    'SIRS': SIRS,
    'SEIR': SEIR
}


class SolveEpidemiologicalModelsService:
    def __init__(self,name_model,vars_initials,params,params_est,t,total_points,method,N) -> None:
        self.name_model = name_model
        self.vars_initials = vars_initials
        self.params = params
        self.params_est = params_est
        self.t = t
        self.total_points = total_points
        self.method = method
        self.N = N
        print(f"name: {name_model} vars_initials {vars_initials} params {params} params_est {params_est} t {t} total_points {total_points} method {method} N {N}")

    def solve_model(self):
        model = dict[self.name_model](vars_initials=self.vars_initials,params_initial=self.params,params_est=self.params_est,N=self.N)
        sol = model.numeric_solver([0,self.t],self.params,self.total_points,self.method)
        img = model.print_numeric_solve([0,self.t],self.params,self.total_points,self.method)
        return sol