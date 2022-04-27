# ---------------------------------------------- IMPORTS ------------------------------------------------------------------------------------------------------
import bpy, os, bmesh, math, mathutils
import numpy as np
from bpy import context
# --------------------------------------CLASS TRANSFORMATIONS--------------------------------------------------------------------------------------------------
class Transformations:

	# Method: "set_rotation(bone, rotation_angle, rotation_axis)"
	# Description: Alter the rotation of bone over one axis.
	# Parameters:
	#    bone_name: The bone to rotate
	#    rotation_angle: The rotation angle
	#    rotation_axis: The roation axis
	# Returns: The matrix inserted into the bone
	def set_rotation(bone_name, rotation_angle, rotation_axis):
		ob = bpy.data.objects['Armature']
		bpy.context.view_layer.objects.active=ob
		bpy.ops.object.mode_set(mode='POSE')
		bone = ob.pose.bones[bone_name]
		bone.rotation_mode = 'AXIS_ANGLE'
		bone.rotation_axis_angle = [math.radians(rotation_angle), 1, 0, 0]
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
		rotation = bone.matrix_basis.to_quaternion()
		return rotation

	# Method: "get_vertices_mesh(object_name)"
	# Description: Get the mesh vertices and return its coordinates in tuple form, later can be accessed by index of vertex
	# Parameter:
	#   object_name: the name in string format
	# Returns: The rotation quaternion that the bone currently has
	def get_vertices_mesh(object_name):
		bpy.context.view_layer.objects.active = bpy.data.objects[object_name] 
		obj = bpy.context.active_object
		depsgraph = bpy.context.evaluated_depsgraph_get()
		depsgraph.update()
		object_eval = obj.evaluated_get(depsgraph)
		mesh_from_eval = bpy.data.meshes.new_from_object(object_eval)
		vertices = mesh_from_eval.vertices
		vert_array = np.array([])
		for vert in vertices:
			vert_array = np.append(vert_array, np.array(vert.co))
        
		bpy.data.meshes.remove(mesh_from_eval)
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
		Transformations.set_bones(mesh_name, bones_array, angles_array)
		mesh_vertices = Transformations.get_vertices_mesh(mesh_name)
		return mesh_vertices

	# Method: "set_bones(mesh_name, bones_array, angles_array)"
	# Description: Traverses through the bone array to set the rotations (transform) for each bone
	# Parameters:
	#    mesh_name: The mesh to access
	#    bones_array: Array that contains the bone names to be changed 
	#    angles_array: Array that contains the new angles for the bones
	# Returns: None
	def set_bones(mesh_name, bones_array, angles_array):
		ob = bpy.data.objects['Armature']
		bpy.context.view_layer.objects.active=ob
		bpy.ops.object.mode_set(mode='POSE')
		angle_index=0
		for bone_name in bones_array:
			Transformations.set_rotation(bone_name, angles_array[angle_index], 'X')
			angle_index=angle_index+1
		return