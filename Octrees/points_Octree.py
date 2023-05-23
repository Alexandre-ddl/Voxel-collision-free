import open3d as o3d
import numpy as np

def points_Octree(points , delta_max_deth):
    
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(np.full((len(points), 3), [1, 0, 0]))
    max_depth= np.floor(np.log(pcd.get_max_bound().max())/np.log(2)).astype(int)-delta_max_deth

    octree = o3d.geometry.Octree(max_depth)
    octree.convert_from_point_cloud(pcd)
    return octree