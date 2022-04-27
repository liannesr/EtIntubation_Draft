import bpy, bmesh
import os, math, mathutils
import numpy as np
from bpy import context
# import open3d
from mathutils import Matrix
from mathutils import Vector
import statistics
import csv
import sys
sys.path.insert(0, '/Users/liannesanchez/opt/miniconda3/lib/python3.7/site-packages/cv2')
import cv2
# sys.path.insert(0, '/opt/homebrew/lib/python3.9/site-packages/open3d')
import open3d
sys.path.insert(0, '/Users/liannesanchez/Desktop/')
from Transformations import Transformations
from Camera import Camera 
from Image_Processing import Image_Processing
from Solver import *
import csv

from scipy.optimize import least_squares
# ------------------------------- TESTING TRANSFORMATION CLASS --------------------------------------------------------------
# array_of_bone = ['Bone', 'Bone.001','Bone.002' ,'Bone.003', 'Bone.004']
# array_of_angles = [0, 0, 45, 0, 0]
# Transformations.transform_mesh('Cylinder', array_of_bone, array_of_angles)
# ---------------------------------------------------------------------------------------------------------------------------
#Vector((7.358891487121582, -6.925790786743164, 4.958309173583984))
#Euler((0.0, -0.0, 0.0), 'XYZ')
# ----------------------------------- TESTING CAMERA CLASS ------------------------------------------------------------------
# print(bpy.data.objects['Camera'].location)
# # print(bpy.data.objects['Camera'].rotation_euler)
# set_camera_position(3.0,-3.0, 3.0, 0.0, 0.0, 0.0)
# print(bpy.data.objects['Camera'].location)
# print(bpy.data.objects['Camera'].rotation_euler)

# area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
# area.spaces[0].region_3d.view_perspective = 'PERSP'
# ---------------------------------------------------------------------------------------------------------------------------

# ----------------------------------- TESTING COMPUTER VISION CLASS ---------------------------------------------------------
# cam = bpy.data.objects['Camera'].data
# print(Camera.get_calibration_matrix(cam))
# print(Camera.get_extrinsic_matrix(bpy.data.objects['Camera']))
# ---------------------------------------------------------------------------------------------------------------------------

# ----------------------------------- TESTING IMAGE PROCESSING CLASS ---------------------------------------------------------
# image = Image_Processing('trim_test.png')
# Image_Processing.mask_image(image)
# print(Image_Processing.find_circles_coor(image))
# ---------------------------------------------------------------------------------------------------------------------------


# TESTING FOR OPEN 3D
# sys.path.insert(0, '/Users/liannesanchez/opt/miniconda3/lib/python3.7/site-packages/open3d/')

# mesh = bpy.data.objects['Airway project model.001'].data
# mesh.calc_loop_triangles()
# triangles = mesh.loop_triangles
# vertices = mesh.vertices

# print("Computing normal and rendering it.")
# mesh.compute_vertex_normals()
# print(np.asarray(mesh.triangle_normals))
# draw_geometries([mesh])

# bpy.ops.render.opengl()
# bpy.ops.render.opengl('INVOKE_DEFAULT')
# bpy.ops.render.render(animation=False, write_still=False, use_viewport=False, layer='', scene='')
# bpy.ops.render.view_show('INVOKE_DEFAULT')



# fields = []
# rows = []
# with open('CollectedData_Sanjeev.csv', 'r') as csvfile:
#     csvreader = csv.reader(csvfile)
     
#     # extracting field names through first row
#     fields = next(csvreader)
 
#     # extracting each data row one by one
#     for row in csvreader:
#         rows.append(row)

 
# coordinates = []
# for column in rows[5][3::]:
#     coordinates.append(float(column))

# coordinates_vector= np. reshape(coordinates, (16, 2))
# # print(coordinates_vector)
# undistorted = Image_Processing.undistort_image(coordinates_vector)

initial_parameters = [ 0.34419, -1.5999, 14.04, 5.52, - 1.16 ,-180+180]
#residuals = Solver.optimize( [ 0.40419, -1.6299, 14.51, 5.52, - 0.959 ,-180])
res_1 = least_squares(optimize, initial_parameters)
print("Resulting optimized parameters: ", res_1.x)
print("Cost: ", res_1.cost)
print("Optimality: ", res_1.optimality)
# print("Sum of residuals: ", np.sum(res_1.x))
# print("Average of residuals: ", np.average(res_1.x))
# Solver.caller_fun(coordinates_vector)
# Camera.get_camera_angles()
# Camera.get_camera_loc()

