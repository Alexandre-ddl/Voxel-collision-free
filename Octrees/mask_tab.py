import numpy as np


def mask_tab(tab, Collision , dic , vect = np.array([0,0,0])):

    conditions_and = []
    for ele in Collision:
        pos , size = dic[ele[0]]['infos'][1:]
        pos+=vect
        conditions_and.append([(tab[:,2] >= pos[2]) & (tab[:,2] <= pos[2] + size), 
                               (tab[:,1] >= pos[1]) & (tab[:,1] <= pos[1] + size),
                               (tab[:,0] >= pos[0]) & (tab[:,0] <= pos[0] + size)])
        
    conditions_and = [np.all(condition, axis=0) for condition in conditions_and]  # cond et ligne 
    mask = np.any(conditions_and, axis=0)  # condition ou collones
 
    return mask         