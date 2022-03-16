import bpy, os, bmesh, math, mathutils
from bpy import context

# Method: set_rotation(bone, rotation_angle, rotation_axis)"
# Description: Alter the rotation of bone over one axis.
# Parameters:
#    bone: The bone to rotate
#    rotation_angle: The rotation angle
#    rotation_axis: The roation axis
# Returns: The matrix inserted into the bone
def set_rotation(bone_name, rotation_angle, rotation_axis):
    mat_rot = mathutils.Matrix.Rotation(math.radians(rotation_angle), 4, rotation_axis)
    bone = bpy.context.active_object.pose.bones[bone_name]
    bone.matrix = mat_rot
    return bone.matrix

# Method: get_matrix_bone(bone)"
# Description: Get the matrix of properties including bone location, scale and rotation
# Parameter:
#    bone: The bone to search 
# Returns: The rotation quaternion that the bone currently has
def get_matrix_bone(bone_name):
    bpy.ops.object.mode_set(mode='POSE')
    bone = bpy.context.active_object.pose.bones[bone_name]
    bone_location, bone_rotation, bone_scale = bone.matrix_basis.decompose()
    rotation = bone.matrix_basis.to_quaternion()
    return rotation

# Method: "get_vertices_mesh()"
# Description: Get the mesh vertices and return its coordinates in tuple form, later can be accessed by index of vertex
# Parameter: None
# Returns: The rotation quaternion that the bone currently has
def get_vertices_mesh(object_name):
    bpy.context.view_layer.objects.active = bpy.data.objects[object_name]
    bpy.ops.object.mode_set(mode='EDIT')
    obj = bpy.context.active_object
    bm = bmesh.from_edit_mesh(obj.data)
    vertices = bm.verts
    vert_list = []
    for vert in vertices:
        vert_list.insert(vert.index, vert.co.to_tuple())
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = bpy.data.objects['Armature']
    return vert_list


# ---------------------------------------------------------------------------------------------------------------------------
#Testing how to access MESH vertices
print(get_vertices_mesh('Cylinder'))

# Testing how to access Armature matrices
print(get_matrix_bone('Bone.001'))
print(get_matrix_bone('Bone'))
print(get_matrix_bone('Bone.002'))

# Testing rotation of bone
set_rotation('Bone', 100,'X')

# ---------------------------------------------------------------------------------------------------------------------------
# INSTRUCTIONS
# Lianne to create Python function, which: 
# Inputs: 

    # Joint positions (for each bone) 
    # Deformed mesh (3D coordinates of vertices) 

# Outputs (option B): 
    # Deformed feature points (3D coordinates of corresponding vertices) 
# Description: 
    # The function calculates the mesh of the deformed model based on the joint parameters. It will be used in the optimization loop. 

