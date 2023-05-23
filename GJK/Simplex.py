import numpy as np
from scipy.spatial import Delaunay

class Simplex():
    
    def __init__(self, simplex ):
        
        self.simplex   = simplex
        self.direction = -simplex[0]
        
    
    def SameDirection(self,vect_0,vect_1):
        
        return np.dot(vect_0,vect_1) > 0
    
    
    def NextSimplex(self):
        
        size = len(self.simplex)
        
        if   size == 2 :  
            return self.Line()
        elif size == 3 : 
            return self.Triangle()
        else           :  
            return self.Tetrahedron()
    
    
    
    def Line(self):
        
        a , b = self.simplex
        
        ab = b - a
        ao =   - a
        
        #if abs(np.linalg.norm(np.cross(ab,a)))< 1e-3:
        #    return True 
        
        if self.SameDirection(ab,ao) :
            
            self.direction = np.cross(np.cross(ab , ao) , ab )
            
        else : 
            
            self.simplex = [a]
            self.direction = ao
            
        return False
        
        
    def Triangle(self):
       
        a , b , c = self.simplex
        
        ab = b - a
        ac = c - a
        ao=    - a
        
        abc = np.cross(ab , ac)
        
        #if abs(a[0]*abc[0]+a[1]*abc[1]+a[2]*abc[2]) < 1e-2:
        #    return True 
        
        if self.SameDirection(np.cross(abc , ac),ao):
            if self.SameDirection(ac,ao):
                
                self.simplex = [a, c] 
                self.direction = np.cross(np.cross(ac,ao),ac)
                
            else :
                
                self.simplex = [a, b] 
                return self.Line()
            
        else :
            
            if self.SameDirection(np.cross(ab , abc),ao):  
                
                self.simplex = [a, b] 
                return self.Line()
            ## cas 3D 
            else : 
                if self.SameDirection(abc,ao):
                    self.direction = abc
                else :
                    self.simplex = [ a , c , b]
                    self.direction = -abc
                    
        return False
        
    
    def Tetrahedron(self):
        a , b , c , d = self.simplex
        
        ab = b - a
        ac = c - a
        ad = d - a
        ao =   - a
        
        abc = np.cross(ab,ac)
        acd = np.cross(ac,ad)
        adb = np.cross(ad,ab)
        
        
        #points = np.array(simp.simplex)
        #delau = Delaunay(points)
        
        #if delau.find_simplex([0,0,0])>=0 :
        #    return True 
        
        if self.SameDirection(abc , ao ):
            self.simplex = [a ,b ,c]
            return self.Triangle()
        
        if self.SameDirection(acd , ao):
            self.simplex = [a ,c ,d]
            return self.Triangle()
            
            
        if self.SameDirection(adb , ao):
            self.simplex = [a ,d ,b]
            return self.Triangle()
        
        return True

