
import pyvista as pv
import numpy as np


"""center at 0 in the XY plane the mesh """
def centrer_0xy(path : str):
    """
    
    Args :
    
        path (str) : path to the slt file
    
    Return :
    
        mesh : the object centered at 0 in the XY plane 
    
    """
    
    mesh = pv.read(path)
    x_min, x_max, y_min, y_max, z_min, z_max = mesh.bounds
    mesh.points -= np.array([x_min,y_min,0])
    return mesh




""" rotation of the mesh according to 2 vectors """
def rotation_mesh(mesh, theta, phi):
    """
    
    Args :
    
        mesh        : path to the slt file
        theta (float) : rotation angle in the XY plane (in degrees)
        phi (float)   : rotation angle in the ZX' plane (in degrees)
        
    Return :
    
        mesh_copy : a copy of the mesh with rotation
    
    """
    
    z=np.array([0,0,1])
    mesh_copy = mesh.rotate_vector(z, theta, inplace=False) # rotation of the mesh around the Z axis
    
 
    rad=np.deg2rad(theta) # works with radiant angles 
    rot_theta = np.array([[np.cos(rad), -np.sin(rad), 0],
                        [np.sin(rad), np.cos(rad), 0],
                        [0, 0, 1]])  # rotation matrix in the Z axis (in the XY plane)

    x_prime = rot_theta @ np.array([1, 0, 0]).T # calculation of the vector X'
    
    y_prime = np.cross(z, x_prime.T) # calculation of the vector Y' 
    
    mesh_copy.rotate_vector(y_prime, phi, inplace=True) # rotation of the mesh around the Y' axis
    return mesh_copy





""" translation of an object from initial to final position """
def translation(object, position_ini, position_fin):  
    """
    
    Args :
    
        object  (numpy array , mesh , pvista_array)  : object described by coordinate points 
        position_ini (numpy array) : initial position 
        position_fin (numpy array) : final position
        
    Return :
    
        object : object with new position
    
    """
    object += (position_fin - position_ini)

    return object


    
    
""" returns the X and Y center of the mesh object  """
def midle_xy(mesh):
    """

    Args :

    mesh 

    Return :

    (numpy array) : the center of the point in the XY plane

    """
        
    points = mesh.points
    return np.array([points[:,0].mean(),points[:,1].mean(),0]).astype(int)



"""
Same as rotation_mesh but this time for objects associated to coordinates (x,y,z)
not mesh object.
"""
def rotation_point(object : np.array, theta, phi, corection = False):
        """
    
        Args :
    
                object ( numpy array ):
                theta (float) : rotation angle in the XY plane (in rad)
                phi (float)   : rotation angle in the ZX' plane (in rad) 
                corection (bool) : 
                        if you are in the modified frame for the voxels
                        and you are on a non-integer coordinate, you must 
                        associate the voxel in which the coordinates are located.
                        for that we take the whole part of each coordinate 
                        in x , y , z. (np.floor) ex: in x 3.3    3 
                                                        y 5.2 -> 5
                                                        z 6.7    6
             
        Return :
    
                object_rot (numpy array) : 
                        the coordinates of the object after rotation 
    
        """
        object=object.copy()
        z=np.array([0,0,1])
        # Z -> x to y
        rot_theta = np.array([[np.cos(theta), -np.sin(theta), 0],
                            [np.sin(theta), np.cos(theta), 0],
                            [0, 0, 1]])

        object_rot = rot_theta @ object.T

        x_prime = rot_theta @ np.array([1, 0, 0]).T
        y_prime = np.cross(z, x_prime.T)

        # Y' -> z to x'
        # rotation matrix for a rotation around any unit vector Y' (wikipédiat)
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