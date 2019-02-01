#Writing some code just to start with the math
import numpy as np;
from numpy import cos as cos
from numpy import sin as sin

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

def get_positions(servoangles):
    pi = np.pi

    m1 = createHTM(0, pi/2, 3.83, servoangles[0])
    m2 = createHTM(0, -pi/2, 0, servoangles[1])
    m3 = createHTM(0, pi/2, 2.92, 0)
    m4 = createHTM(0, -pi/2, 0, servoangles[2])
    m5 = createHTM(0, 0, 3.46, 0)


    t_matrices = [m1, m2, m3, m4, m5]
    t_e = createHTM(0, 0, 0, 0)
    for m in t_matrices:
        t_e = np.matmul(t_e, m)

        #print(t_e)
    print("m1-m5")
    #print(t_e)
    print("x: " + str(t_e[0][3]) +  ", y: " + str(t_e[1][3]) + ", z: " + str(t_e[2][3]))

pi = np.pi

for i in range(0, 180):
    for j in range(0, 180):
        for k in range(0, 180):
            print("-"*15)
            deg_servoangles = [i, j, k]
            print(deg_servoangles)

            rad_i = i * pi/180
            rad_j = j * pi/180
            rad_k = k * pi/180

            servoangles = [rad_i, rad_j, rad_k]
            #print(servoangles)
            get_positions(servoangles)
