import open3d as o3d
import numpy as np


def Voxelize(mesh , voxel_size , number_of_points , centre0xy = False):
    
    point_cloud = mesh.sample_points_uniformly(number_of_points)
    if centre0xy : 
        vect = - point_cloud.get_min_bound() + voxel_size/2
        point_cloud.translate(vect)
    voxel_grid1 = o3d.geometry.VoxelGrid.create_from_point_cloud(point_cloud, voxel_size)
    
    return voxel_grid1
    