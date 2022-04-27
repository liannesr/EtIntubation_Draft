# ---------------------------------------------- IMPORTS ------------------------------------------------------------------------------------------------------
import bpy, os, bmesh, math, mathutils
import numpy as np
from bpy import context
import sys
from mathutils import Matrix
import csv
from scipy.optimize import least_squares
from scipy.spatial.transform import Rotation as R
from Camera import Camera 
# import matplotlib as plt
# sys.path.insert(0, '/Users/liannesanchez/opt/miniconda3/lib/python3.7/site-packages')
# import cv2
# import matplotlib 
# import matplotlib.pyplot as plt
# %matplotlib inline
# from matplotlib import pyplot as plt
sys.path.insert(0, '/Users/liannesanchez/Desktop/')
from Transformations import Transformations
from Camera import Camera 
from Image_Processing import Image_Processing
# ---------------------------------------------- SOLVER -------------------------------------------------------------------------------------------------------
# features_blender = [253891,245757,258346,273943,261732,420159,419736,418791,417540,419226,478392,436828,434417,480580,451334,448279]
features_blender = [253880,241846,258350,277330,270851,419722,419740,418371,418298,417561,478415,478148,434421,478831,451321,447810]
coordinates = []
fields = []
rows = []
with open('CollectedData_Sanjeev.csv', 'r') as csvfile:
	csvreader = csv.reader(csvfile)
     
   	# extracting field names through first row
	fields = next(csvreader)
 
# extracting each data row one by one
	for row in csvreader:
		rows.append(row)

# coordinates = []
for column in rows[6][3::]:
	coordinates.append(float(column))

coordinates_vector= np.reshape(coordinates, (16, 2))
undistorted = Image_Processing.undistort_image(coordinates_vector)
# print(np.array(undistorted[0][0][1]))
coordinates_vector = undistorted
# print(coordinates_vector)
# input("Press Enter to continue...")

def euclidean_distance(point1, point2):
	# print(point1)
	# print(point2[0])
	# print(point2[1])
	# input("Press Enter to continue...")
	sum_1 = point1[0][0]-point2[0]
	sum_2 = point1[0][1]-point2[1]
	additions = (sum_1**2) + (sum_2**2)
	# print(additions)
	distance = math.sqrt(additions)
	# input("Press Enter to continue...")
	# print(distance)
	# input("Press Enter to continue...")
	# distance = np.sqrt(np.sum(np.square(point1-point2)))
	return distance

def optimize(parameters): #x
	# Subtract PI from z 
	# With 6 parameters calculate (tx, ty, tz, rx, ry, rz)
	location = [parameters[0], parameters[1], parameters[2]]#Camera.get_camera_loc()
	rotation = [((parameters[3])/(2 * math.pi)) * 360,((parameters[4])/(2 * math.pi)) * 360, ((parameters[5])/(2 * math.pi)) * 360]#Camera.get_camera_angles()



	# NOT YET: Deform mesh



	# Extract from mesh the vertices that correspond to indices 
		# use config file index numbers or source code with index defined by Sanjeev.csv
		# get 3d position for each vertex 
	bpy.context.view_layer.objects.active = bpy.data.objects['Airway project model.001'] 
	obj = context.active_object
	global_coor = np.empty((4,len(features_blender)))
	counter = 0
	for verts_index in features_blender:
		local_co = obj.data.vertices[verts_index].co
		# global_coor.append(np.array(obj.matrix_world @ local_co))
		# print(obj.matrix_world @ local_co)
		# np.append(global_coor,np.matrix(np.array(obj.matrix_world @ local_co)).T,1)
		global_coor[ :, counter] = np.append(np.array(obj.matrix_world @ local_co), 1)
		counter=counter+1
	# print("Coordinate: ", np.array(global_coor))
	# print(global_coor)

	K = np.matrix([[677.10347, 0,     310.3956],
				  [0,       677.1037, 230.3598],
		 		  [0,       0,        1]])
		 				
	# Calculate rotation matrix (3x3) from euler angles (rx, ry, rz - pi)
	rotation[2]=rotation[2]-math.pi # Added cause it was negative.... Would that be ok?
	
	r = R.from_euler('xyz', [rotation[0], rotation[1], rotation[2]], degrees=False).as_matrix()
	# print(r)
	# initial_parameters = [location[0], location[1], location[2], rotation[0], rotation[1], rotation[2]]

	# Assemble camera extrinsics matrix (pose, 3x4) from rotation and translation (tx, ty, yz)
	# extrinsics = Matrix(
#           ((	 r[0][0], 	r[0][1], r[0][2], location[0]),
#           (    r[1][0], 	r[1][1], r[1][2], location[1]),
#           (    r[2][0],   r[2][1], r[2][2], location[2]),
#           (	 0  ,	 0, 	 0,			1      )))

	extrinsics = np.matrix([[r[0][0], r[0][1], r[0][2], location[0]],
						   [r[1][0], r[1][1], r[1][2], location[1]],
		 				   [r[2][0], r[2][1], r[2][2], location[2]],
		 				   [ 0,	        0,      0,	        1]])
	# print(extrinsics)
	# extrinsics.invert()
	# Invert camera extrinsics (you might have to make it into a 4x4 matrix temporarily)
	inverted_extrinsics = np.linalg.inv(extrinsics)
	pose = extrinsics[0::][0:3]
	# print(simple.shape)

	# Multiply calibration matrix with inverted camera extrinsics matrix (3x4) => projection matrix
	projection_matrix = K * pose#np.dot(K, pose)
	# print("projection_matrix: ", projection_matrix)

	image_coor = []
	# temp_arr = np.zeros(3,global_coor.shape[1])
	# Find the positions in image 
	  # For each vertex: multiply projection matrix with vertex
	  # Normalize homogenious vector results (divide vector by the 3rd element) >> (xi, yi) image coordinates
	#for world_coor in global_coor:
		#print(np.append(np.array(world_coor), 1))
	#	temp_arr
	#	temp_arr = np.append(np.array(world_coor), 1)
	#	vector_result = projection_matrix*temp_arr#np.dot(projection_matrix, temp_arr)
		#image_coor.append([vector_result[0]/vector_result[2], vector_result[1]/vector_result[2]])

	matrix_result = projection_matrix*global_coor #np.dot(projection_matrix, temp_arr)
	# print(matrix_result[0][:])

	matrix_result[0] = np.divide(matrix_result[0], matrix_result[2])
	matrix_result[1] = np.divide(matrix_result[1], matrix_result[2])
	matrix_result=matrix_result[0:2]
	# print("Divide First Row: ", matrix_result[0])
	# print("Divide Second Row: ", matrix_result[1])

	# print("Matrix results: " , matrix_result)
	# print(image_coor)
	# Calculate the distance between each simulated image coordinate and the one provided by Sanjeev (2D Euclidian distance)
	# Results: vector of distances (N=number of features)

	distances = []
	# index=0

	# for column in image_coor:
	# 	distances.append(Solver.euclidean_distance(coordinates_vector[index], image_point))
	# 	index = index+1
	print(matrix_result)
	x = matrix_result[0]
	y = matrix_result[1]

	# plt.scatter(x, y, c='r', marker='o', label='Optimizer Points')
	# plt.legend(loc='upper left')
	# plt.show()
	# input("Press Enter to continue...")

	for index in range(matrix_result.shape[1]-1):
		# print("Coordinates: ", coordinates_vector[index])
		# print("Matrix item: ", matrix_result[:,index].reshape(1,2))
		# print("MATRIX GOING IN: ", matrix_result[:,index])
		distances.append(euclidean_distance(coordinates_vector[index], matrix_result[:,index]))
		# input("Press Enter to continue...")

	print(euclidean_distance(coordinates_vector[index], matrix_result[:,index]))
	print("Distances: ", distances)

	return np.array(distances)

