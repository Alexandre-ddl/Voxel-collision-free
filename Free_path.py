import pyvista as pv
import numpy as np  
import networkx as nx


from tqdm import tqdm
from Voxel_model import Voxels
from Path_create import Create_Path
from creation_vector import Vector_Creation
from mesh_tools import centrer_0xy , rotation_mesh , midle_xy , translation


def Free_path(vox, tool_path, surface, theta, position_head_layer_circle,Circle,G, layer_vertex , z_max_collision ):
        """
    
        Args :
            
            vox : Voxel model
            
            tool_path (numpy array): 
                coordinates (x,y,z) associated to each point of the path
                
            surface (pyvista array ~ numpy array): 
                coordinates of each voxel composing the printhead in 
                its original position (aligned with the Z axis) 
                
            theta (float): in degree
            
            position_head_layer_circle (dic) : 
                dictionary that lists each position of the print 
                head for each inclination :
                position_head_layer_circle[theta = 4][delta = 4] 
                = position of the print head for an angle 
                of 4 times theta and 4 times delta 
            
            Circle (dic) : 
                for each inclination theta 
                associates the list of possible angles 
                Circle[theta = 4][delta = 4] =  rotation in the XY plane of 
                4 times delta for an inclination to Z of 4 times theta 
                
            G (nx networkx) : graph 
            
            layer_vertex (dic) : 
                each key of the dictionary corresponds to a level
                of the graph and thus to a coordinate of the path. 
                Each vertex associated to a key corresponds to a position 
                of the print head without collision 
            
           
        Return :
        
            shortest_path (list) : 
                list of printhead positions with collision-free 
                 path [(0,4,4),...] 
                 0 -> position O on the tool_path
                 4 -> Circle 4 ( inclination of 4 times theta )
                 4 -> 4 times delta rotation in the XY plane
      
    
        """
        num_layers = len(tool_path)
        source = 's'
        target = 't'
        
        G.add_node(source)
        G.add_node(target)
        
        for i in tqdm(range(num_layers)):
            if i > 0:
                prev_layer = i - 1    
                prev_layer_vertices = layer_vertex[prev_layer]# Recover the vertices of the previous floor

            for j in Circle:
                for ind, delta in enumerate(np.rad2deg(Circle[j])):
                    
                    if i == 0 :
                        position_rotate = rotation_mesh(surface, delta,j*theta) 
                        position_rotate = np.floor(position_rotate.points).astype(int) # corrects the position of the surface after rotation 
                        position_head_layer_circle[j].append(position_rotate) # adds the print head positions for each vector to avoid recalculating them 
                        position = translation(position_rotate,np.array([0,0,0]),tool_path[i]) # translate to the first point of the path
                    else :
                        position_rotate = position_head_layer_circle[j][ind]
                        position = translation(position_rotate,tool_path[i-1],tool_path[i])
                        
                    mask = position[:,2]<= z_max_collision # only consider the points which can have collision (here only on Z but can add conditions on X and Y )
                    
                    if not vox.density(position[mask]): # if there is no density (no obstacle)
                        current_vertex = (i, j , ind)  #  name of the vertex
                        G.add_node(current_vertex, angle_z=j*theta) # create the summit with its attributes 
                        layer_vertex[i].append(current_vertex)  # Adds the vertex to the layer corresponding to its points in the path
                        if i > 0: 
                            for prev_vertex in prev_layer_vertices: # create links between floors if the angular condition is respected
                                angle = abs(G.nodes[prev_vertex]['angle_z']-G.nodes[current_vertex]['angle_z'])
                                if angle <= theta:
                                    G.add_edge(prev_vertex, current_vertex, weight=angle)
                        if i == 0:
                            G.add_edge(source, current_vertex, weight=0)
                        if i == num_layers-1:
                            G.add_edge(current_vertex,target ,weight=0)
                            
            vox.voxels[tool_path[i][0],tool_path[i][1],tool_path[i][2]]=1 #adds density at the point of passage of the print head  


       
        shortest_path = nx.dijkstra_path(G, source, target)
        
        return shortest_path    
    

    