
import pyvista as pv
import numpy as np

def centrer_0xy(path : str):
    mesh = pv.read(path)
    x_min, x_max, y_min, y_max, z_min, z_max = mesh.bounds
    mesh.points -= np.array([x_min,y_min,0])
    return mesh

def rotation_mesh(mesh, theta, phi):
    z=np.array([0,0,1])
    mesh_copy = mesh.rotate_vector(z, theta, inplace=False)
    # Z -> x vers y
    rad=np.deg2rad(theta)
    rot_theta = np.array([[np.cos(rad), -np.sin(rad), 0],
                        [np.sin(rad), np.cos(rad), 0],
                        [0, 0, 1]])

    x_prime = rot_theta @ np.array([1, 0, 0]).T
    y_prime = np.cross(z, x_prime.T)
    mesh_copy.rotate_vector(y_prime, phi, inplace=True)
    return mesh_copy

def midle_xy(mesh):
    points = mesh.points
    return np.array([points[:,0].mean(),points[:,1].mean(),0]).astype(int)