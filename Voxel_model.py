import pyvista as pv
import numpy as np
import math


class Voxels():
    
    def __init__(self, scale_print, scale_voxel):
        """
    
        Args :
    
            scale_print (float) : the size of the printing area
            scale_voxel (float) : the dimension of a voxel
    
        """
        
        self.scale_print = scale_print 
        self.scale_voxel = scale_voxel

        self.nb_voxels = math.ceil(scale_print/scale_voxel) 
        
        self.voxels = np.zeros((self.nb_voxels,self.nb_voxels,self.nb_voxels)) #creation of the voxel model initialized with a density value equal to 0 

        self.midle = (np.array([1.,1.,0.])*self.nb_voxels/2).astype(int) # calculation of the middle of the voxel in XY to center the printed object 
        
        
    def add_density(self, coord):
        """
    
        Args :
    
            coord (numpy array) : coordinate where density must 
                                  be added (there is one voxel)
            
    
        """

        self.voxels[coord[:,0],coord[:,1],coord[:,2]]=1

    def substracted_density(self,coord):
        """
    
        Args :
    
            coord (numpy array) : coordinates where the 
                                  density must be removed (there is no voxel)
            
    
        """
        
        self.voxels[coord[:,0],coord[:,1],coord[:,2]]=0

    def density(self, coord):
        """
    
        Args :
    
            coord (numpy array) : test to see if any of the 
                                  coordinates contain density 
            
        Return :
    
            (bool) : True -> there is density (equivalent to collision) 
            
            
        """
        
        density_bool = self.voxels[coord[:,0],coord[:,1],coord[:,2]]==1
        return np.any(density_bool)
 
    

        
       

