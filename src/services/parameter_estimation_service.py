from business_logic.model import *
from business_logic.algorithms.classical_methods import *
from business_logic.algorithms.metaheuristics import *
from business_logic.utils.utils import *

dict = {
    'SI': SI,
    'SIR': SIR,
    'SIRS': SIRS,
    'SEIR': SEIR
}


class ParameterEstimationService:
    def __init__(self,name_model,vars_initials,params,params_est,interval_est,t,total_points,method,N,
                 params_min,params_max,classical_method,metaheuristic,path,iter,particle,cognitive,
                 social,inercia,population,crossing,scaled) -> None:
        self.name_model = name_model
        self.vars_initials = vars_initials
        self.params = params
        self.params_est = params_est
        self.interval_est = interval_est
        self.t = t
        self.total_points = total_points
        self.method = method
        self.N = N
        self.params_min = params_min
        self.params_max = params_max
        self.classical_method = classical_method
        self.metaheuristic = metaheuristic
        self.path = path
        self.iter = iter
        self.particle = particle
        self.cognitive = cognitive
        self.social = social
        self.inercia = inercia
        self.population = population
        self.crossing = crossing
        self.scaled = scaled

    def solve_model(self):
        model = dict[self.name_model](self.vars_initials,self.params,params_est=self.params_est,N=self.N)
        opt = []

        if(self.classical_method!=''and self.metaheuristic!=''):
            sol_met = []
            if (self.metaheuristic=='PSO'):
                metaheuristic = PSO(model,read(self.path),self.total_points,[self.params_min,self.params_max],self.iter,self.particle,
                                self.cognitive,self.social,self.inercia)
                sol_met = metaheuristic.solve()
            else:
                metaheuristic = DifferentialEvolution(model,read(self.path),self.total_points,[self.params_min,self.params_max],
                                                  self.iter,self.population,self.crossing,self.scaled)
                sol_met = metaheuristic.solve()

            classical = ClassicalMethods(self.classical_method,model,read(self.path),self.total_points,sol_met)
            opt = classical.solve()

        elif(self.classical_method!=''):
            classical = ClassicalMethods(self.classical_method,model,read(self.path),self.total_points,self.params)
            opt = classical.solve()

        else:
            if (self.metaheuristic=='PSO'):
                metaheuristic = PSO(model,read(self.path),self.total_points,[self.params_min,self.params_max],self.iter,self.particle,
                                self.cognitive,self.social,self.inercia)
                opt = metaheuristic.solve()
            else:
                metaheuristic = DifferentialEvolution(model,read(self.path),self.total_points,[self.params_min,self.params_max],
                                                  self.iter,self.population,self.crossing,self.scaled)
                opt = metaheuristic.solve()
                
        sol = model.numeric_solver([0,self.t],opt,self.total_points,self.method)
        img = model.print_numeric_solve([0,self.t],opt,self.total_points,self.method)
        return opt,sol