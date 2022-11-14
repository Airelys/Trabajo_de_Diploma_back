from pandas import Interval 
#from sympy import*
import math
import random as rd
#from interval import interval

class interval(Interval):
    def __new__(cls,inf:float,sup:float=None,void:bool=False)-> None:
        _sup=sup
        if sup is None:
            _sup=inf
            obj=super().__new__(cls,inf,inf,'both')
            
        else:
            obj=super().__new__(cls,inf,sup,'both')
            

        obj.__init__(inf,sup,void)
        return obj
    
    def __init__(self,inf,sup,void=False):
        super().__init__(inf,sup,'both')
        
        self.min=inf
        self.max=sup
        self.void=void
        
    def _contains(self, element):
        if self.void:
            return False
        
        else:
            super()._contains(element)
        
    def __equals__(self,other):
        if type(other)==type(0):
            return self.max==self.min and self.min==other
        
        else:
            if type(self)!=type(other):
                raise TypeError
            
            else:
                return self.min==other.min and self.max==other.max
        
    def __add__(self,other):
        return interval(self.min+other.min,self.max+other.max)
    
    def __sub__(self,other):
       
        return interval(self.min-other.max,self.max-other.min)
    
    def __mul__(self,other):
        
        return interval(min(self.min*other.min,self.min*other.max,self.max*other.min,self.max*other.max),max(self.min*other.min,self.min*other.max,self.max*other.min,self.max*other.max))
    
    def __rmul__(self, other):
       
        return self * other
    
    def __div__(self, other):
        
        if not (0 in other):
            return self*interval(1/other.max,1/other.min)
        
        elif 0 in self and 0 in other:
            return interval(-math.min,math.min)
        
        elif self.max > 0 and other.min<other.max and other.max==0:
            return interval(self.max/other.min,math.min)
        
        elif self.max < 0 and other.min<0 and 0<other.max:
            return interval(-math.min,self.max/other.max).union(interval(self.max/other.min,math.min))
        
        elif self.max<0 and 0 == other.min and other.min<other.max:
            return interval(-math.min,self.max/other.max)
        
        elif self.max<0 and other.min<other.max and 0 == other.min:
            return interval(-math.min,self.min/other.min)
        
        elif 0 < self.min and other.min<0 and 0<other.max:
            return interval(-math.min,self.min/other.min).union(interval(self.min/other.max,math.min))
        
        elif 0 < self.min and 0 == other.min and other.min<other.max:
            interval(self.min/other.max,math.min)
            
        elif not (0 in self) and other==0:
            return interval(0,0,True)
              
    __truediv__ = __div__
    
    def __and__(self,other):
        if self.overlaps(other):
            return interval(max(self.min,other.min),min(self.max,other.max))
        
    def __str__(self):
        return f'[{self.min},{self.max}]'
    
    def m_point(self):
        if self.max-self.min<=1e-10:
            return self.min
        
        else:
            return (self.max+self.min)/2 
    
    def function(self,f):
        if self.min==self.max:
            return interval(f(self.min),f(self.min))
        
        values=[0 for i in range(10)]
        values[7]=f(self.m_point())
        values[8]=f(self.min)
        values[9]=f(self.max)
        
        for i in range(7):
            values[i]=rd.uniform(self.min,self.max)
            
        f_values=[f(values[i]) for i in range(10)]
        return interval(min(f_values),max(f_values))

        