import pyvista as pv
import numpy as np
from gcodeparser import GcodeParser


class Create_Path():
    
    def __init__(self,path):
        
        
        with open(path, 'r') as f:
            gcode = f.read()
        self.file = GcodeParser(gcode).lines

    def see(self,end,start=0):
        return self.file[start:end+1]
        

    def read_gcode(self, start):
    
        tabl= self.file[start:]
        relevant_lines=[[tabl[0].params['X'],tabl[0].params['Y'],tabl[0].params['Z']]]
        for ele in tabl[1:]:
            if ele.command[0] in ['G']:
                i=0
                for ind, coord in enumerate(['X','Y','Z']):
                    if coord not in ele.params : 
                        ele.params[coord]=relevant_lines[-1][ind]
                        i+=1
                if i!=3:
                    relevant_lines.append([ele.params['X'],ele.params['Y'],ele.params['Z']])
        
        relevant_lines=np.array(relevant_lines)
        self.tool_path = relevant_lines[:-2]
    
    def centrer(self, object):
        min_x=object[:,0].min()
        min_y=object[:,1].min()

        self.tool_path[:,1]-=min_y
        self.tool_path[:,0]-=min_x

    def translat(self, position_ini : np.array, position_fin : np.array):

        self.tool_path += (position_fin - position_ini)
    
    def figure(self,mesh, show_edges = False):
        p = pv.Plotter()
        p.add_mesh(mesh, color=True, show_edges=show_edges, opacity=0.6)
        p.add_mesh(self.tool_path, color=True)
        p.show_grid()
        p.add_axes_at_origin()
        p.show()

    def correction(self, scale_voxel):   
        
        self.tool_path = np.floor(np.divide(self.tool_path, scale_voxel)).astype(int)

    


    

