import numpy as np


""" create the list of vectors on the unit sphere """
def Vector_Creation(theta, angle_max):
    """
    
    Args :
    
        theta (float) : rotation angle in the ZX' plane (in rad)
        angle_max (float) : limit angle that the print head can take (in rad)
        
        
    Return :
        
        Circle (dic) : 
               for each inclination theta 
               associates the list of possible angles 
               Circle[theta = 4][delta = 4] =  rotation in the XY plane of 
               4 times delta for an inclination to Z of 4 times theta 
    
    """
    qotient = int(angle_max // theta) + 1
    Circle = {i: [] for i in range(qotient)}
    Circle[0]=np.array([0])
    for i in range(1,qotient):
        u=np.cos(theta)
        v=np.cos(i*theta)
        v=v*v
        delta=np.arccos((u-v)/(1-v))
        qotient = int(2*np.pi // delta) + 1
        Circle[i] = np.array([ k*delta for k in range(qotient)])
    return Circle