import numpy as np


class Polytope():
    
    def __init__(self,simplex):
        
        self.vertexs = simplex.copy()
        
        self.ind_max = 3
        
        self.faces = [ [0, 1, 2] ,
                       [0, 3, 1] ,
                       [0, 2, 3] ,
                       [1, 3, 2] ]
        
        normales = []
        normes   = []
        
        for face in self.faces:
            normale , norme = self.normal(face)
            
            normales.append(normale)
            normes.append(norme)
        
        self.normales = normales
        self.normes = normes
        
        self.historique_min=[]
        self.min_normale_norme()
            
        
    def Edge(self,face):
        
        return [{face[0],face[1]},{face[1],face[2]},{face[2],face[0]}]    
    
    def add_face(self,face):
        
        self.faces.append(face)
        normale , norme = self.normal(face)
        
        self.normales.append(normale)
        self.normes.append(norme)
        
    def remove_face(self,face):
        
        index = self.faces.index(face)
        
        del self.faces[index]
        del self.normales[index]
        del self.normes[index]
        
    def min_normale_norme(self):
        
        minimum_normes = min(self.normes)
        minimum_index = self.normes.index(minimum_normes)
        
        self.historique_min.append((self.normales[minimum_index] , minimum_normes))
    
        
    def normal(self , face):
        
        a , b , c = [self.vertexs[index] for index in face]
        ab = b - a 
        ac = c - a 
        oa = a

        abc = np.cross( ab , ac)
        
            
        abc = abc / np.linalg.norm(abc)

        D = np.dot( abc , oa )

        if D <= 0 :
            abc = - abc
            D   = - D

        return abc  , D
    
    
    def New_vertex(self , vertex):
        self.vertexs.append(vertex)
        self.ind_max+=1
        edges =[]
        
        Remove=[]
        
        
        
        for ind , face in enumerate(self.faces) : 
            centroid_face = (self.vertexs[face[0]]+self.vertexs[face[1]]+self.vertexs[face[2]])/3
            if np.dot(vertex-centroid_face , self.normal(face)[0]) > 0 :
                
                Remove.append(face)
             
                for edge in self.Edge(face):
            
                    if edge not in edges :
                        edges.append(edge)
                    else : 
                        edges.remove(edge)
       
        for face in Remove:
            self.remove_face(face)
            
        for edge in edges :
            edge=tuple(edge)
            face = [edge[0],edge[1],self.ind_max]
            self.add_face(face)   