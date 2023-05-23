import numpy as np  
import networkx as nx

from rotation import rotation
from points_Octree import points_Octree
from parcourir_octree_dico import dic
from collision_octree import collision_octree
from mask_tab import mask_tab
from Voxelize import Voxelize
from coord_voxel import coord_voxel


import sys
sys.path.insert(0, '../')

from tqdm import tqdm
from Voxel_model import Voxels
from Path_create import Create_Path
from creation_vector import Vector_Creation
from mesh_tools import centrer_0xy , rotation_mesh , midle_xy , translation


def Free_path_octrees(vox, tool_path, tool_mesh , theta, position_head_layer_circle,Circle,G, layer_vertex , octree_haed_layer_circle , octree_collision , delta_max_deth ,number_of_points):

    
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
                for ind, delta in enumerate(Circle[j]):
                    
                    if i == 0 :
                        tool_r = rotation(tool_mesh,delta ,j*np.deg2rad(theta)) #tool_path[0]+np.array([0,0,6])
                        
                        tool_r_voxel = Voxelize(tool_r , vox.scale_voxel , number_of_points)
                        
                        voxel_r_voxel_coord= coord_voxel(tool_r_voxel)

                        voxel_r_voxel_coord = tool_r_voxel.origin + tool_r_voxel.voxel_size * voxel_r_voxel_coord
                        
                        voxel_r_voxel_coord+=np.array([0,0,6])
                        voxel_r_voxel_coord = np.floor(np.divide(voxel_r_voxel_coord,vox.scale_voxel)).astype(int)
                        
                        octree_tool = points_Octree(voxel_r_voxel_coord , delta_max_deth)
                        dic_octree_tool={}
                        dic(octree_tool,dic_octree_tool)
                        octree_haed_layer_circle[j].append(dic_octree_tool) 
                        
                        position_head_layer_circle[j].append(voxel_r_voxel_coord)
                        position = translation(voxel_r_voxel_coord,np.array([0,0,0]),tool_path[i])
                        
                        
                      
                    else :
                        
                        position_rotate = position_head_layer_circle[j][ind]
                        dic_octree_tool = octree_haed_layer_circle[j][ind]
                        
                        position = translation(position_rotate,tool_path[i-1],tool_path[i])
                    
                    
                    collision = collision_octree(dic_octree_tool, octree_collision, tool_path[i])
                   
                    mask = mask_tab(position, collision , dic_octree_tool, tool_path[i])
                    
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
    


