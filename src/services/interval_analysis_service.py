from business_logic.model import *
from business_logic.algorithms.intervalar_methods import *
from business_logic.utils.utils import *
import copy as cp

dict = {
    'SI': SI_interval,
    'SIR': SIR_interval,
    'SIRS': SIRS_interval,
    'SEIR': SEIR_interval
}


class IntervalAnalysisService:
    def __init__(self,model_name,vars_initials,params,params_est,t,total_points,method,N,
                 params_min,params_max,interval_method,path) -> None:
        self.model_name = model_name
        self.vars_initials = vars_initials
        self.params_initials = params
        self.params = params
        self.params_est = []
        for i,item in enumerate(params_est):
            if(item):
                print(f'i {i} item {item} params_est {params_est[i]}')
                self.params_est.append(i)
        print(self.params)
        self.t = t
        self.total_points = total_points
        self.method = method
        self.N = N
        self.params_min = params_min
        self.params_max = params_max
        self.interval_method = interval_method
        self.path = path

    def solve_model(self):
        initials = cp.copy(self.params)
        for i in self.params_est:
            initials[i] = [self.params_min[i],self.params_max[i]]
            
        print(f'initials {initials}')
        mod = dict[self.model_name](vars_initials=self.vars_initials,params_initial=initials,params_est=self.params_est,N=self.N)
        sol_met = []
        if (self.interval_method=='Iterative'):
            inter = intervalar_methods("it",mod,read(self.path),self.total_points)
            sol_met = inter.solve()
        else:
            inter = intervalar_methods("it",mod,read(self.path),self.total_points)
            sol_met = inter.solve()

                
        val=sol_met.random_point()
        opt=[[sol_met[i].min,sol_met[i].max] for i  in self.params_est]
        sol = mod.numeric_solver([0,self.t],val,self.total_points,self.method) #punto random
        img = mod.print_numeric_solve([0,self.t],val,self.total_points,self.method)
        print(f'img {img} sol {sol} opt {opt}')
        return opt,sol