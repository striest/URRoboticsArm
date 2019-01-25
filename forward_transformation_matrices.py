# -*- coding: utf-8 -*-
"""Forward Transformation Matrices

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IZMuI6o4AH_wQ3aBjhNAOwobHR8eoG_m
"""
'''
servo n: n+1 for n=1 to 6
'''
import numpy as np; np.set_printoptions(suppress=True, precision=2);

from numpy import cos as cos
from numpy import sin as sin
pi = np.pi

def createHTM(a, alpha, d, theta):
  """
  a : link length
    Distance along rotated x axis.
  alpha : link twist  
    Determined by frame setup, rotation around new x to make zs match.
  d : link offset
    Distance along the original z between the two links.
  theta : joint angle
    Rotation around original z.
  Applied as: Rotate theta arounnd z0, translate along z, translate along x, rotate alpha around new x
  """
  t_matrix = np.zeros((4, 4))
  
  t_matrix[0][0] = cos(theta)
  t_matrix[0][1] = -sin(theta)*cos(alpha)
  t_matrix[0][2] = sin(theta)*sin(alpha)
  t_matrix[0][3] = a*cos(theta)
  t_matrix[1][0] = sin(theta)
  t_matrix[1][1] = cos(theta)*cos(alpha)
  t_matrix[1][2] = -cos(theta)*sin(alpha)
  t_matrix[1][3] = a*sin(theta)
  t_matrix[2][0] = 0
  t_matrix[2][1] = sin(alpha)
  t_matrix[2][2] = cos(alpha)
  t_matrix[2][3] = d
  t_matrix[3][0] = 0
  t_matrix[3][1] = 0
  t_matrix[3][2] = 0
  t_matrix[3][3] = 1
  
  return t_matrix

theta1 = 0
theta2 = pi/2
theta3 = 0
theta4 = 0
theta5 = 0
theta6 = 0

m1 = createHTM(0, pi/2, 3.83, theta1)
print("m1")
print(m1)
m2 = createHTM(0, -pi/2, 0, theta2)
print("m2")
print(m2)
m3 = createHTM(0, pi/2, 2.92, 0)
print("m3")
print(m3)
m4 = createHTM(0, -pi/2, 0, theta3)
print("m4")
print(m4)
m5 = createHTM(0, 0, 3.46, 0)
print("m5")
print(m5)

###These are wrist joints

m6 = createHTM(0,pi/2,0,theta4)
print("m6")
print(m6)
m7 = createHTM(0, -pi/2,0,theta5)
print("m7")
print(m7)
m8 = createHTM(0,0,0,theta6)
print("m8")
print(m8)

def combineLinks(l1, l2):
  '''
  :param l1: h_matrix
  :param l2: h mtarix 2
  '''
  return l1*l2

t_matrices = [m1, m2, m3, m4, m5] ### [m1,m2,m3,m4,m5,m6,m7,m8]
t_e = createHTM(0, 0, 0, 0)
for m in t_matrices:
  t_e = np.matmul(t_e, m)

print("m1-m5")
print(t_e)

t_matrices_wrist = [m6, m7, m8] ### [m1,m2,m3,m4,m5,m6,m7,m8]
t_e_wrist = createHTM(0, 0, 0, 0)
for m in t_matrices_wrist:
  t_e_wrist = np.matmul(t_e_wrist, m)
  
print("m6-m8")
print(t_e_wrist)