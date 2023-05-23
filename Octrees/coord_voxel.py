import open3d as o3d
import numpy as np


def coord_voxel(Voxel_object):
    voxels_coords = Voxel_object.get_voxels()
    grid_indices = np.array([voxel.grid_index for voxel in voxels_coords])
    return grid_indices