import open3d as o3d
import numpy as np


def Voxel_Octree(voxel_model , delta_max_deth , voxel_size):
    
    max_depth = np.floor(np.log(voxel_model.get_max_bound().max()/voxel_size)/np.log(2)).astype(int) - delta_max_deth
    octree=voxel_model.to_octree(max_depth)
    
    return octree