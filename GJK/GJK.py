import numpy as np
from Support import support 
from Simplex import Simplex


def GJK(A, B,simp):
    i=0 
    while i< 64:
        sup  = support(A, B, simp.direction)

        if np.dot(sup , simp.direction) <= 0:
            
            return False
        
        simp.simplex = [sup] + simp.simplex
        #print('sup : ', sup , 'simplex : ', simp.simplex)
        
        if simp.NextSimplex():
            return True   
         
        i+=1
        #print('taille : ',len(simp.simplex) ,'direction : ',simp.direction ,'i : ',i)
    return  i

