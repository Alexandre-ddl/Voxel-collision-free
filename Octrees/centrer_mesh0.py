import open3d as o3d
import numpy as np

def centrer_mesh0(mesh):
    p_ini = mesh.get_center()
    p_ini[-1]=0
    vect = - p_ini
    
    z_min = mesh.get_min_bound()[-1]
    if abs(z_min)< 1e-9:
        vect-= np.array([0,0,z_min])
   
    mesh.translate(vect)