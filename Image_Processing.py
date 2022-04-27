import numpy as np
import sys
sys.path.insert(0, '/Users/liannesanchez/opt/miniconda3/lib/python3.7/site-packages/cv2')
import cv2

class Image_Processing(object):

  def __init__(self, image_name):
    print(image_name)
    self.image = cv2.imread(image_name)
    # self.img_copy = self.image.copy()

  def mask_image(self):
    hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
    lower_range = np.array([110,50,50])
    upper_range = np.array([130,255,255])
    self.mask = cv2.inRange(hsv, lower_range, upper_range)

  def find_circles_coor(self):
    contours, hierarchy = cv2.findContours(self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    self.detected_circles = []
    for i, c in enumerate(contours):

      # Approximate the contour to a circle:
      (x, y), radius = cv2.minEnclosingCircle(c)

      # Compute the center and radius:
      center_coor = (int(x), int(y))
      radius = int(radius)

      # Draw the circles:
      # cv2.circle(img_copy, center, radius, (0, 255, 0), 2)

      # Store the center and radius:
      self.detected_circles.append([center_coor, radius])
    return self.detected_circles

  def undistort_image(coordinates):
    image_dim_x = 640
    image_dim_y = 480 
    focal_length_x = 677.1037
    focal_length_y = 677.1037
    center_x = 310.3956
    center_y = 230.3598

    Rd = np.array([-0.09728, 0.07831, 0.00069, 0.00060, -0.04527])
    K = np.array(   [[focal_length_x,         0      , center_x],
        [    0          ,  focal_length_y, center_y],
        [    0          ,         0      ,      1 ]])

    undistorted_points = cv2.undistortPoints(coordinates, K, Rd, P=K)
  
    return undistorted_points