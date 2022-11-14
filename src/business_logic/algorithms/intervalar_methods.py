from numpy import double
from business_logic.model import Epidemiological_model
from business_logic.objective_function import ObjectiveFunction
from business_logic.algorithms.box import box
from business_logic.algorithms.my_interval import interval 
from multiprocessing import Process

#[box,last index cutted, max value of f,repetition]

#Elimination's tests
def midpoint_test(f, X:box, minf:double)->list:
    test=f(X.m_point()) #pasar datos de la función
    if  test < minf:
        return [True,test]
        
    
    else:
        return [False,0]
    
def monotony_test(f, X:box)->bool:
    Y=X.grad(f)
        
    yi=Y.min
    ys=Y.max
    
    for i in range(len(X)):
        if yi[i]>0 or ys[i]<0:
            return True
        
    return False

def feasibility_test(f, X:box):  
    Y=X.function(f)
    ys=Y.max
    
    for i in ys:
        if ys[i]>0:
            return True
    
    return False

    
class intervalar_methods:
    def __init__(self, method:str, model:Epidemiological_model, data: list, total_points:float) -> None:
        self.method = method
        self.objective_function = ObjectiveFunction(model,data,total_points)
        self.model=model
        
    def solve(self):
        params_est=self.model.params_est
        X=[0 for i in range(len(self.model.params_initial))]
        for i in range(len(self.model.params_initial)):
            if type(self.model.params_initial[i])==type([]):
                X[i]=interval(self.model.params_initial[i][0],self.model.params_initial[i][1])
                
            else:
                X[i]=interval(self.model.params_initial[i],self.model.params_initial[i])
        
        X=box(X)
        
        
        sol_list=set([X])
        fun=X.function(self.objective_function.objective_function).min
        #print(fun)
        
        if len(params_est):
            intervalar_optimization(X,params_est[0],[],sol_list,1e-10,self.objective_function.objective_function,fun,0,params_est)
            sol_list=list(sol_list)
            if len(sol_list)==0:
                return X
            
            elif len(sol_list)==1:
                return sol_list[0] 
            
            else:
                sol=sol_list[0]
                for i in sol_list[1:]:
                    sol&=i
                    
                return sol
            
        else:
            return X
            
    
def intervalar_optimization(X:box,index:int,work_list:list,sol_list:set,epsilon:double,f,minf:double,n:int,params_est:list):
    #print(f'index {index}')
    if index>X.count:
        y=X.function(f)
        if y.min-minf<=epsilon:
            minf=y.min         
            sol_list.add(X)
        return
    
    if X[index].max-X[index].min <= epsilon:
        y=X.function(f)
        if y.min - minf<= epsilon:
                minf=y.min
                sol_list.add(X)
        return
    
    Y=X.cut_in(index,X[index].m_point())
    
    
    for y in Y:
        monotony=True
        mp_test=midpoint_test(f,y,minf)
        for k in y.intervals:
            if 0 in k:
                monotony=False
                break
        
        if mp_test[0]:
            minf=mp_test[1]
            continue
        
        elif monotony:
            if monotony_test(f,y):
                continue
        
        else:
            g=y.function(f).max
            if len(work_list) == 0:
                work_list.append([y,index,g,n])
                continue
                
            for i in range(len(work_list)):
                if g < work_list[i][2]:
                    work_list.insert(i,[y,index,g,n])
                    break
            
        while len(work_list) > 0:
            act_box=work_list[0]
            work_list.remove(work_list[0])
            new_index=act_box[1]
            
            for i in range(len(params_est)):
                if params_est[i]==index:
                    if i+1<len(params_est):
                        new_index=params_est[i+1]
                    
                    break  
                
            if new_index==act_box[1] and act_box[3]<3/len(params_est):
                intervalar_optimization(act_box[0],act_box[1],work_list,sol_list,epsilon,f,minf,act_box[3]+1,params_est)
                
                            
            elif act_box[3]<3/len(params_est):
                intervalar_optimization(act_box[0],act_box[1],work_list,sol_list,epsilon,f,minf,act_box[3]+1,params_est)
                intervalar_optimization(act_box[0],new_index,work_list,sol_list,epsilon,f,minf,act_box[3],params_est)
                
            else:
                intervalar_optimization(act_box[0],act_box[1]+1,work_list,sol_list,epsilon,f,minf,act_box[3]+1,params_est)
            
            g=act_box[0].function(f)
            if g.min-minf<=epsilon:
                minf=g.min
                sol_list.add(act_box[0])
 
def multiprocess_auxiliar():
    
    
    pass
                   
def intervalar_optimization_threading(X:box,index:int,work_list:list,sol_list:set,epsilon:double,f,minf:double,n:int,params_est:list):
    process=[0 for i in range(2)]
    