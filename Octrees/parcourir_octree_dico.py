import open3d as o3d
import numpy as np

def parcourir_octree_dico(node, node_info, dictionnaire):
    node_id = (node_info.depth, tuple(node_info.origin))
    if node_id not in dictionnaire:
        dictionnaire[node_id] = {'infos': (node_info.depth, node_info.origin, node_info.size), 'enfants': []}
    
    if isinstance(node, o3d.geometry.OctreeInternalNode):
        for i in range(8):
            child = node.children[i]
            if child:
                child_depth = node_info.depth + 1
                child_size = node_info.size / 2
                child_origin_offset = np.array([1 * (i % 2 == 1)  ,
                                                1* (i in [2,3,6,7]) ,
                                                1* (i > 3) ])  *   child_size

                child_origin = node_info.origin + child_origin_offset
                child_id = (child_depth, tuple(child_origin))
                dictionnaire[node_id]['enfants'].append(child_id)
                dictionnaire[child_id] = {'infos': (child_depth, child_origin , child_size), 'enfants': []} 



def dic(octree,dictionnaire):
    function_octree = lambda node, node_info: parcourir_octree_dico(node, node_info, dictionnaire)
    octree.traverse(function_octree)