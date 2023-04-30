import numpy as np

def Vector_Creation(theta, angle_max):
    qotient = int(angle_max // theta) + 1
    Circle = {i: [] for i in range(qotient)}
    Circle[0]=np.array([0])
    for i in range(1,qotient):
        u=np.cos(theta)
        v=np.cos(i*theta)
        v=v*v
        sigma=np.arccos((u-v)/(1-v))
        qotient = int(2*np.pi // sigma) + 1
        Circle[i] = np.array([ k*sigma for k in range(qotient)])
    return Circle