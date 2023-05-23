import numpy as np
from Polytope import Polytope
from Support import support 


def EPA(A,B,simplex,eps):
    
    poly = Polytope(simplex)
    sup  = support(A, B, poly.historique_min[-1][0])
    position_relative = np.dot(poly.historique_min[-1][0],sup)
    
    i=0
    while (  (poly.historique_min[-1][1] < position_relative) & 
           
             (position_relative - poly.historique_min[-1][1] > eps ) &
           
             (i < 100)   ):
        
            poly.New_vertex(sup)

            poly.min_normale_norme()

            sup  = support(A, B, poly.historique_min[-1][0])
            position_relative = np.dot(poly.historique_min[-1][0],sup)
            i+=1
            
    return  poly , sup , i