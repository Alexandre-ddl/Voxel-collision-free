import open3d as o3d
import numpy as np
from collision_node import collision_node


def collision_octree(octree1,octree2, vect_translat_1  = np.array([0,0,0]) , vect_translat_2= np.array([0,0,0])):
    #dic_octree1={}
    #dic(octree1,dic_octree1)
    first_key_1 = next(iter(octree1))
    
    #dic_octree2={}
    #dic(octree2,dic_octree2)
    first_key_2 = next(iter(octree2))
    
    collision = []
    
    def where_collision(node1, node2, dictionnaire_1, dictionnaire_2):
            test_1 = not dictionnaire_1[node1]['enfants']
            test_2 = not dictionnaire_2[node2]['enfants']
    
            if test_1 and test_2:
                collision.append((node1, node2))
            elif not test_1:
                for child in dictionnaire_1[node1]['enfants']:
                    if collision_node(child, node2, dictionnaire_1, dictionnaire_2 , vect_translat_1 , vect_translat_2):
                        where_collision(child, node2, dictionnaire_1, dictionnaire_2)
            elif not test_2:
                for child in dictionnaire_2[node2]['enfants']:
                    if collision_node(node1, child, dictionnaire_1, dictionnaire_2 , vect_translat_1 , vect_translat_2):
                        where_collision(node1, child, dictionnaire_1, dictionnaire_2)
    
    where_collision(first_key_1, first_key_2, octree1, octree2)            
        
    
    return collision 