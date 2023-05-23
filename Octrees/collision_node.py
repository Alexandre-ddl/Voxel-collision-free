import open3d as o3d
import numpy as np


def collision_node(node1, node2, dictionnaire_1 , dictionnaire_2 , vect_translat_1, vect_translat_2):
    
    depth1 , origin1 , size1 = dictionnaire_1[node1]['infos']
    depth2 , origin2 , size2 = dictionnaire_2[node2]['infos']
    
    min_1 , max_1 = origin1 + vect_translat_1 , origin1 + size1 + vect_translat_1
    min_2 , max_2 = origin2 + vect_translat_2 , origin2 + size2 + vect_translat_2
    
    i=0
    collision = True 

    while i<3 and collision : 
    
        collision = not ( (max_2[i] <= min_1[i]) or (min_2[i] >= max_1[i]) )
        i+=1
        
    return collision  