import pyvista as pv
import numpy as np
import math

class Voxels():
    
    def __init__(self, scale_print, scale_voxel):
        
        self.scale_print = scale_print
        self.scale_voxel = scale_voxel

        self.nb_voxels = math.ceil(scale_print/scale_voxel)
        
        self.voxels = np.zeros((self.nb_voxels,self.nb_voxels,self.nb_voxels))

        self.midle = (np.array([1.,1.,0.])*self.nb_voxels/2).astype(int)

    def Voxelise_object(self,object):
        # Path = object
        mesh =  object    #pv.read(Path)

        x_min, x_max, y_min, y_max, z_min, z_max = mesh.bounds

        voxels = pv.voxelize(mesh, density=self.scale_voxel, check_surface=False)

        surface = voxels.extract_surface()
        surface_points = surface.points
        surface_points -= np.array([x_min,y_min,z_min]) 
        surface_points = np.divide(surface_points, self.scale_voxel).astype(int)
        surface_points += np.array([160,160,0]) 
        return surface_points

    def add_density(self, coord):

        self.voxels[coord[:,0],coord[:,1],coord[:,2]]=1

    def substracted_density(self,coord):
        
        self.voxels[coord[:,0],coord[:,1],coord[:,2]]=0

    def density(self, coord):
        density_bool = self.voxels[coord[:,0],coord[:,1],coord[:,2]]==1
        return np.any(density_bool)
    

    def translation(self, object, position_ini, position_fin):  
        # scale : In the good referential
        object += (position_fin - position_ini)

        return object
    

    def rotation(self, object : np.array, theta, phi, corection = False):
        
        object=object.copy()
        z=np.array([0,0,1])
        # Z -> x vers y
        rot_theta = np.array([[np.cos(theta), -np.sin(theta), 0],
                            [np.sin(theta), np.cos(theta), 0],
                            [0, 0, 1]])

        object_rot = rot_theta @ object.T

        x_prime = rot_theta @ np.array([1, 0, 0]).T
        y_prime = np.cross(z, x_prime.T)

        # Y' -> z vers x'
        I=np.eye(3)
        y_x=y_prime[0]
        y_y=y_prime[1]
        y_z=y_prime[2]
        P=np.array([ [ y_x*y_x, y_x*y_y, y_x*y_z],
                    [ y_x*y_y, y_y*y_y, y_y*y_z],
                    [ y_x*y_z , y_y*y_z, y_z*y_z]])
        
        Q=np.array([[0,-y_z,y_y],
                    [y_z,0,-y_x],
                    [-y_y, y_x,0]])
        
        Rot = P + np.cos(phi)*(I-P)+np.sin(phi)*Q

        object_rot = Rot @ object_rot
        if corection :
            return np.floor(object_rot).T
        return object_rot.T
        
       

