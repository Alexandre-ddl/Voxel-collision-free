
import pyvista as pv
import numpy as np
import imageio
import os
from tqdm import tqdm
from mesh_tools import translation


""" creation of images for the video """
def create_images(free_path,position_head_layer_circle,tool_path,mesh_collision):
    """
    
    Args :
    
        free_path (list)   : 
        
                 list of printhead positions with collision-free 
                 path [(0,4,4),...] 
                 0 -> position O on the tool_path
                 4 -> Circle 4 ( inclination of 4 times theta )
                 4 -> 4 times delta rotation in the XY plane
                             
        position_head_layer_circle (dic) : 
                 
                 dictionary that lists each position                                
                 of the print head for each inclination 
                 position_head_layer_circle[theta = 4][delta = 4] = position of the 
                 print head for an angle of 4 times theta and 4 times delta 
                                           
        tool_path (numpy array): 
        
                 coordinates (x,y,z) associated to each point of the path
                 
        mesh_collision (mesh) : the object mesh 
    
    Return :
    
        images (list) :  list of images to create the video 
    
    """
    
    
    p = pv.Plotter(off_screen=True)
    images = []

    for ele in tqdm(free_path):
        p.clear()
        position  = position_head_layer_circle[ele[1]][ele[2]].copy() # finds the copy of the print head associated with this position
        position = translation(position,tool_path[-1],tool_path[ele[0]]) # translate the print head to the desired position
        
        p.add_mesh(tool_path, color='white') # displays the tool_path
        p.add_mesh(tool_path[ele[0]], color='red') # displays the desired point in red 
        p.add_mesh(position, show_edges=False, color='blue') # displays the print head 
        p.add_mesh(mesh_collision, color=True, show_edges=False, opacity=0.7) # displays the object that causes the collisions 
        
        img = p.screenshot(window_size=[800, 600])
        images.append(img)

    return images

""" creation of the video """
def create_video(images, output_file, fps=30):
    with imageio.get_writer(output_file, mode='I', fps=fps) as writer:
        for img in images:
            writer.append_data(img)

