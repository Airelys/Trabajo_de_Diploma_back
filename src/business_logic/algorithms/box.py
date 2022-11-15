import copy as cp
from business_logic.algorithms.my_interval import interval
from sympy import*
import random as rd

class box:
    #Constructor
    def __init__(self,intervals:list)->None:
        self.intervals=tuple(intervals)
        self.count=len(intervals)
        self.min=[0 for i in self.intervals]
        for i in range(len(self.intervals)):
            self.min[i]=self.intervals[i].min
            
        self.max=[0 for i in self.intervals]   
        for i in range(len(self.intervals)):
            self.max[i]=self.intervals[i].max 
                 
    #Overloads
    def __len__(self):
        return self.count
    
    def __getitem__(self, pos):
        return self.intervals[pos]
    
    def __add__(self,other):
        if self.count != other.count:
            raise Exception("The dimensions are not equals")
        
        sol=[0 for i in range(len(self.intervals))]
        for i in range(len(sol)):
            sol[i]=self.intervals[i]+other.intervals[i]
            
        return box(sol)
            
    def __mul__(self, other):
        if self.count != other.count:
            raise Exception("The dimensions are not equals")
        
        sol=[0 for i in range(len(self.intervals))]
        for i in range(len(sol)):
            sol[i]=self.intervals[i]*other.intervals[i]
            
        return box(sol)
            
    def __sub__(self, other):
        s=other * box([-1 for i in range(other.count)])
        return self + s
        
    def __truediv__(self,other):
        if self.count != other.count:
            raise Exception("The dimensions are not equals")
        
        d=[0 for i in range(len(other.intervals))]
        
        for i in range(len(other.intervals)):
            d[i]=self.intervals[i]/other.intervals[i]

        return box(d)
        
    def __str__(self):
        return f'box[{self.intervals}]'
    
    def __and__(self, other):
        if self.count != other.count:
            raise Exception("The dimensions are not equals")
        
        x=[0 for i in range(self.count)]
        
        for i in range(self.count):
            x[i]=self[i]&other[i]
            
        print(x)
        return box(x)
        
    def __iter__(self):
        return self.intervals
     
    #Properties   
    def sum(self):
        sum=0
        for i in self.intervals:
            sum+=i
            
        return sum
    
    def grad(self,f):
        def grad_aux(x):
            
            return 2*(f([i+1 for i in x])-f([1 for i in x]))

        g=self.function(grad_aux)
        return box([g/i for i in self.intervals])
        
    def m_point(self):
        m_point=[0 for i in range(len(self.intervals))]
        for i in range(len(self.intervals)):
            m_point[i]=self.intervals[i].m_point()
            
        return m_point
    
    def cut_in(self,pos:int,point:float):
        if pos>self.count:
            raise IndexError("Pos most be a valid position in the box")
        
        if point in self.intervals[pos]:
            
            ui=[0 for i in range(len(self.intervals))]
            oi=[0 for i in range(len(self.intervals))]
            
            for j in range(len(self.intervals)):
                if j==pos:
                    ui[j]=interval(self.intervals[pos].min,point)
                    oi[j]=interval(point,self.intervals[pos].max)
                    
                else:
                    ui[j]=cp.deepcopy(self.intervals[j])
                    oi[j]=cp.deepcopy(self.intervals[j])
                    
            ui=box(ui)
            oi=box(oi)
            return [ui,oi]
           
    def function(self,f,points:list=[]):
        
        values=[[0 for i in range(self.count)] for i in range(10)]
        values[-3]=self.m_point()
        values[-2]=self.min
        values[-1]=self.max
        
        for i in range(7):
            for j in range(self.count):
                values[i][j]=rd.uniform(self[j].min,self[j].max)
                
        #print(f'values {values}')
            
        f_values=[f(values[i]) for i in range(len(values))]
        return interval(min(f_values),max(f_values))      
    
    def random_point(self):
        r=[0 for i in range(self.count)]  
        for i in range(self.count):
            r[i]=rd.uniform(self[i].min,self[i].max)
            
        return r
            


