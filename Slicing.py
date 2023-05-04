import pyvista as pv
import numpy as np
import networkx as nx


from creation_vector import Vector_Creation
from mesh_tools import centrer_0xy , rotation_mesh , midle_xy ,translation


def slice_voxel(voxel , axis : str, position):
    """
    Args : 
    
        voxel (np array) 
        axis (str)     : can be 'x' , 'y' or 'z'
        position (int) : where you want to slice the voxel 
        
    Return : 
    
        voxel[mask](np array) : the slice 
    
    
    """
    if axis == 'x':
        mask = voxel[:,0]==position
    elif axis == 'y':
         mask = voxel[:,1]==position
    elif axis == 'z':
        mask = voxel[:,2]==position
    
    return voxel[mask] 



def min_max_axis(voxel , axis : str , min_max : str):
    """
    Args : 
    
        voxel (np array) 
        axis (str)     : can be 'x' , 'y' or 'z'
        min_max (str) : can be 'min' or 'max'
        
    Return : 
    
        (int) : the max or min of the axis chosen for the voxel model
    
    
    """
    if axis == 'x':
        return getattr(voxel[:,0], min_max)()
    elif axis == 'y':
        return getattr(voxel[:,1], min_max)()
    elif axis == 'z':
        return getattr(voxel[:,2], min_max)()
 

""" from numpy array to set """
def coordinate_set( voxel , axis):
    """
    Args : 
    
        voxel (np array) 
        axis (str)     : can be 'x' , 'y' or 'z'
        
    Return : 
    
        (set) : set of each position of the numpy array
    
    
    """
    if axis == 'x':
        return {(y, z) for y, z in voxel[:,1:]}
    elif axis == 'y':
        return {(x, z) for x, z in voxel[:,0::2]}
    elif axis == 'z':
        return {(x, y) for x, y in voxel[:,0:2]}

    
""" test to check if there is a collision with sets on a specific layer """
def collision_set_layer(voxels_head_print_surface , voxels_collision_surface , axis , layer):
        """
        Args : 
    
            voxels_head_print_surface / voxels_collision_surface (np array)
            axis (str)    : can be 'x' , 'y' or 'z'
            layer (int) :  where you want to slice 
        
        Return : 
    
            (set) : set composed of the coordinates shared by the 2 slices
    
    
        """
        slice_head = slice_voxel (voxels_head_print_surface , axis, layer)
        slice_collision = slice_voxel( voxels_collision_surface , axis ,layer)
        
        set_head = coordinate_set(slice_head, axis)
        set_collision = coordinate_set(slice_collision , axis)
        
        return set_head & set_collision

    
""" test to check if there is a collision with np.intersect1d on a specific layer """
def collision_intersect_layer(voxels_head_print_surface , voxels_collision_surface , axis , layer):
        """
        Args : 
    
            voxels_head_print_surface / voxels_collision_surface (np array)
            axis (str)    : can be 'x' , 'y' or 'z'
            layer (int) :  where you want to slice 
        
        Return : 
    
             collision.size : indicates the number of elements in the collision list
    
    
        """
        slice_head = slice_voxel (voxels_head_print_surface , axis, layer)
        slice_collision = slice_voxel( voxels_collision_surface , axis ,layer)
        
        dtype = np.dtype([('x', int), ('y', int),('z', int)])
        slice_head = slice_head.view(dtype)
        slice_collision = slice_collision.view(dtype)

        
        collision = np.intersect1d(slice_head, slice_collision)
        
        return collision.size
    

""" test to check if there is a collision with sets or intersection on every layer """
def collision( voxels_head_print_surface , voxels_collision_surface , function ):
    """
    
    Args : 
    
        function : can be collision_set_layer or collision_intersect_layer
    
    """
    
    min_z_head_print = min_max_axis(voxels_head_print_surface, 'z','min')
    max_z_collision = min_max_axis(voxels_collision_surface, 'z','max')
    
    if max_z_collision < min_z_head_print:
        return False
    
    layer=0
    bound = max_z_collision- min_z_head_print
    collision= {}
    
    while not collision and layer < bound+1 : 
        
        
        collision = function(voxels_head_print_surface , voxels_collision_surface , 'z' ,min_z_head_print +layer)
        
        layer+=1
    
    return collision

