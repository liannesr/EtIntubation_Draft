import bpy, os, bmesh, math, mathutils
from bpy import context
import numpy as np


# Method: "set_rotation(bone, rotation_angle, rotation_axis)"
# Description: Alter the rotation of bone over one axis.
# Parameters:
#    bone_name: The bone to rotate
#    rotation_angle: The rotation angle
#    rotation_axis: The roation axis
# Returns: The matrix inserted into the bone
def set_rotation(bone_name, rotation_angle, rotation_axis):
    #bone = bpy.context.active_object.pose.bones[bone_name]
    bpy.data.objects["Armature"].data.bones[bone_name].select = True
    bpy.ops.transform.rotate(value=math.radians(rotation_angle), orient_axis=rotation_axis, orient_type='VIEW')
    bpy.data.objects["Armature"].data.bones[bone_name].select = False
    #bone.rotation_euler.rotate_axis(rotation_axis, math.radians(rotation_angle))
    return

# Method: "get_matrix_bone(bone)"
# Description: Get the matrix of properties including bone location, scale and rotation
# Parameter:
#    bone: The bone to search 
# Returns: The rotation quaternion that the bone currently has
def get_matrix_bone(bone_name):
    bpy.ops.object.mode_set(mode='POSE')
    bone = bpy.context.active_object.pose.bones[bone_name]
    bone_location, bone_rotation, bone_scale = bone.matrix_basis.decompose()
    print(bone_rotation)
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
    vert_array = np.array([])
    for vert in vertices:
        vert_array = np.append(vert_array, np.array(vert.co))
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = bpy.data.objects['Armature']
    return vert_array


# Method: "transform_mesh(mesh_name, bones_array, angles_array)"
# Description: Merge the needed steps into one routine
# Parameters:
#    mesh_name: The mesh to access
#    bones_array: Array that contains the bone names to be changed 
#    angles_array: Array that contains the new angles for the bones
# Returns: Mesh 3D vertices and its coordinates
def transform_mesh(mesh_name, bones_array, angles_array): # THINK IN FUTURE ABOUT LENGTH OR SCALING!
    set_bones(mesh_name, bones_array, angles_array)
    mesh_vertices = get_vertices_mesh(mesh_name)
    return mesh_vertices

# Method: "set_bones(mesh_name, bones_array, angles_array)"
# Description: Traverses through the bone array to set the rotations (transform) for each bone
# Parameters:
#    mesh_name: The mesh to access
#    bones_array: Array that contains the bone names to be changed 
#    angles_array: Array that contains the new angles for the bones
# Returns: None
def set_bones(mesh_name, bones_array, angles_array):
    bpy.ops.object.mode_set(mode='POSE')
    angle_index=0
    for bone_name in bones_array:
        set_rotation(bone_name, angles_array[angle_index], 'X')
        angle_index=angle_index+1
    ret
        
# Method: "set_camera_position(new_x, new_y, new_z)"
# Description: Changes camera position with respect to the position (0,0,0)
# Parameters:
#    new_x: The new x coordinate
#    new_y: The new y coordinate 
#    new_z: The new z coordinate
# Returns: None
def set_camera_position(new_x, new_y, new_z):
    camera_location = bpy.data.objects['Camera'].location
    camera_location.x = new_x
    camera_location.y = new_y
    camera_location.z = new_z
    return
    
# ---------------------------------------------------------------------------------------------------------------------------
#array_of_bone = ['Bone', 'Bone.001','Bone.002' ,'Bone.003', 'Bone.004']
#array_of_angles = [10, 45, 10, 10, 10]
#transform_mesh('Cylinder', array_of_bone, array_of_angles)
# ---------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------
#print(bpy.data.objects['Camera'].location)
#set_camera_position(7.0,-6.0, 5.0)
#print(bpy.data.objects['Camera'].location)
# ---------------------------------------------------------------------------------------------------------------------------

# Method: set_head_tail_postition(bone_name, head_position, tail_position)" ====================== NOT NEEDED FOR APPLICATION ======================
# Description: Alter the head and tail positions of a bone
# Parameters:
#    bone_name: The bone to rotate
#    head_position: Array that contains 3D coordinates of head
#    tail_position: Array that contains 3D coordinates of tail
# Returns: Nothing
def set_head_tail_postition(bone_name, head_position, tail_position):
    bpy.context.view_layer.objects.active = bpy.data.objects['Armature']
    bpy.ops.object.mode_set(mode='EDIT')
    obj = bpy.context.edit_object
    bones = obj.data.edit_bones
    bones[bone_name].head = (head_position[0], head_position [1], head_position[2])
    bones[bone_name].tail = (tail_position[0], tail_position [1], tail_position[2])
    return 
