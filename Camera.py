# ---------------------------------------------- IMPORTS ------------------------------------------------------------------------------------------------------
import bpy, os, bmesh, math, mathutils
import numpy as np
from bpy import context
from mathutils import Matrix
from mathutils import Vector
# --------------------------------------CLASS TRANSFORMATIONS--------------------------------------------------------------------------------------------------
class Camera:
# Method: "set_camera_position(new_x, new_y, new_z)"
# Description: Changes camera position with respect to the position (0,0,0)
# Parameters:
#    new_x: The new x coordinate
#    new_y: The new y coordinate 
#    new_z: The new z coordinate
# Returns: None
    def set_camera_position(new_x, new_y, new_z, x_orient, y_orient, z_orient):
        bpy.ops.object.mode_set(mode='POSE')
        bpy.data.objects['Camera'].location = Vector((new_x, new_y, new_z))
        bpy.data.objects['Camera'].rotation_euler = Vector((x_orient, y_orient, z_orient))
        return

    def get_camera_angles():
        euler = bpy.data.objects['Camera'].rotation_euler
        print("Euler before: ", euler)
        #pi = math.pi
        # roll = (euler[0] / (2 * pi) ) * 360
        # pitch = (euler[1] / (2 * pi) ) * 360
        # yaw = (euler[2] / (2 * pi) ) * 360
        return euler#Vector((roll, pitch,yaw))

    def get_camera_loc():
        location = bpy.data.objects['Camera'].location
        return location   

    def get_calibration_matrix(camera):
        # Source: https://blender.stackexchange.com/questions/38009/3x4-camera-matrix-from-blender-camera
        # camera.lens = 677.1037
        # focus = camera.lens
        focus=39
        scene = bpy.context.scene
        res_x = scene.render.resolution_x # pixels
        res_y = scene.render.resolution_y # pixels
    
        # print("Res x: ", scene.render.resolution_x)
        # print("Res y : ", scene.render.resolution_y)
        scale = scene.render.resolution_percentage/100
    
        sensor_w = camera.sensor_width
        sensor_h = camera.sensor_height

        # print("Focus: ", bpy.data.cameras['Camera'].lens)
        # print("Sensor w: ", sensor_w)
        # print("Sensor h: ", sensor_h)
        
        # print("Scale: ", scale)
    
        aspect_ratio = scene.render.pixel_aspect_x/scene.render.pixel_aspect_y
        # print("aspect_ratio: ", aspect_ratio)
        if (camera.sensor_fit == 'VERTICAL'):
            # the sensor height is fixed (sensor fit is horizontal), 
            # the sensor width is effectively changed with the pixel aspect ratio
            s_u = res_x * scale / sensor_w / aspect_ratio 
            
            s_v = res_y * scale / sensor_h
            
        else: # 'HORIZONTAL' and 'AUTO'
            # the sensor width is fixed (sensor fit is horizontal), 
            # the sensor height is effectively changed with the pixel aspect ratio
            aspect_ratio = scene.render.pixel_aspect_x / scene.render.pixel_aspect_y
            # s_u = res_x * scale / sensor_w
            # s_v = res_y * scale * aspect_ratio / sensor_h
            #print(s_u)
            # print(s_v)

        # Parameters of intrinsic calibration matrix K
        # alpha_u = focus * s_u
        # alpha_v = focus * s_v
      
        alpha_u = (res_y/2)/(math.tan((focus/2)*(math.pi/180)) ) 
        alpha_v = (res_y/2)/(math.tan((focus/2)*(math.pi/180)) )  
        u_0 = res_x*scale / 2
        v_0 = res_y*scale / 2
        skew = 0 # only use rectangular pixels

        K = Matrix(
            ((alpha_u, skew,    u_0),
            (    0  ,  alpha_v, v_0),
            (    0  ,    0,      1 )))
        
        return K

    def get_extrinsic_matrix(camera):
        # bcam stands for blender camera
        R_bcam2cv = Matrix(
            ((1, 0,  0),
            (0, -1, 0),
            (0, 0, -1)))

        # Transpose since the rotation is object rotation, 
        # and we want coordinate rotation
        # R_world2bcam = cam.rotation_euler.to_matrix().transposed()
        # T_world2bcam = -1*R_world2bcam * location
        #
        # Use matrix_world instead to account for all constraints
        location, rotation = camera.matrix_world.decompose()[0:2]
        R_world2bcam = rotation.to_matrix().transposed()

        # Convert camera location to translation vector used in coordinate changes
        # T_world2bcam = -1*R_world2bcam*cam.location
        # Use location from matrix_world to account for constraints:     
        T_world2bcam = -1*R_world2bcam @ location

        # Build the coordinate transform matrix from world to computer vision camera
        # NOTE: Use * instead of @ here for older versions of Blender
        # TODO: detect Blender version
        R_world2cv = R_bcam2cv@R_world2bcam
        T_world2cv = R_bcam2cv@T_world2bcam

        # put into 3x4 matrix
        RT = Matrix((
            R_world2cv[0][:] + (T_world2cv[0],),
            R_world2cv[1][:] + (T_world2cv[1],),
            R_world2cv[2][:] + (T_world2cv[2],)
            ))
        return RT
    