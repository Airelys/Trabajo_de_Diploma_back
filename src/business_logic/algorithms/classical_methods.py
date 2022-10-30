from scipy.optimize import minimize
from model import Epidemiological_model
from objective_function import ObjectiveFunction

'Newton-CG' , 'CG' , 'BFGS' , 'L-BFGS-B' 

class ClassicalMethods:
    def __init__(self, method:str, model: Epidemiological_model, data: list, total_points:float) -> None:
        self.method = method
        self.objective_function = ObjectiveFunction(model, data, total_points)
        self.params = []
        for i in model.params_est:
            self.params.append(model.params_initial[i])

    def solve(self):
        model = minimize(self.objective_function.objective_function, self.params, method=self.method, options={'disp': True})
        return model.x
