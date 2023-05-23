import open3d as o3d
import numpy as np
import copy as copy

def rotation(mesh , theta, phi):
    """
    
    Args : angle (rad)
    
    """
    z=np.array([0,0,1])
    mesh_r = copy.deepcopy(mesh)
    
    R_z = mesh.get_rotation_matrix_from_axis_angle(z * theta)
    x_prime = R_z @ np.array([1, 0, 0]).T
    mesh_r.rotate(R_z,np.array([0,0,0]))
    
    y_prime = np.cross(z, x_prime)
    R_y = mesh.get_rotation_matrix_from_axis_angle(y_prime * phi)
    mesh_r.rotate(R_y,np.array([0,0,0]))
    
    return mesh_r