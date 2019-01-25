from gpiozero import AngularServo
import inputs
import numpy as np; np.set_printoptions(suppress=True, precision=2);
from numpy import cos as cos
from numpy import sin as sin

servos = []

def setServos(servos, angles):
    '''
    Set the servos in teh servo array to corresponding angles
    '''
    
    for i in range(len(servos)):
        servos[i].angle = angles[i]

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

def combineLinks(l1, l2):
  '''
  :param l1: h_matrix
  :param l2: h mtarix 2
  '''  
  return l1*l2


  
def main():
    pi = np.pi
    for device in inputs.devices:
            print(device)
            
    a = AngularServo(2,min_angle = 0,max_angle = 180,min_pulse_width = .0005,max_pulse_width = .0025)
    b = AngularServo(3,min_angle = 0,max_angle = 180,min_pulse_width = .0005,max_pulse_width = .0025)
    c = AngularServo(4,min_angle = 0,max_angle = 180,min_pulse_width = .0005,max_pulse_width = .0025)
    d = AngularServo(5,min_angle = 0,max_angle = 180,min_pulse_width = .0005,max_pulse_width = .0025)
    e = AngularServo(6,min_angle = 0,max_angle = 180,min_pulse_width = .0005,max_pulse_width = .0025)
    f = AngularServo(7,min_angle = 0,max_angle = 180,min_pulse_width = .0005,max_pulse_width = .0025)

    servos = [a, b, c, d, e, f]
    
    servoangles = [0] * 6


    m1 = createHTM(0, pi/2, 3.83, servoangles[0])
    m2 = createHTM(0, -pi/2, 0, servoangles[1])
    m3 = createHTM(0, pi/2, 2.92, 0)
    m4 = createHTM(0, -pi/2, 0, servoangles[2])
    m5 = createHTM(0, 0, 3.46, 0)

    

    t_matrices = [m1, m2, m3, m4, m5] ### [m1,m2,m3,m4,m5,m6,m7,m8]
    t_e = createHTM(0, 0, 0, 0)
    for m in t_matrices:
      t_e = np.matmul(t_e, m)

    print("m1-m5")
    print(t_e)

    while 1:
        print('Degrees:')
        print("t0={}; t1={}; t2={}".format(servoangles[0], servoangles[1], servoangles[2]))

        theta1 = servoangles[0]*pi/180
        theta2 = servoangles[1]*pi/180
        theta3 = servoangles[2]*pi/180

        print("Radians:")
        print("t0={}; t1={}; t2={}".format(theta1, theta2, theta3))


        m1 = createHTM(0, pi/2, 3.83, -theta1)
        m2 = createHTM(0, -pi/2, 0, theta2)
        #m3 = createHTM(0, pi/2, 2.92, 0)
        m4 = createHTM(0, -pi/2, 0, theta3)
        #m5 = createHTM(0, 0, 3.46, 0)

        

        t_matrices = [m1, m2, m3, m4, m5] ### [m1,m2,m3,m4,m5,m6,m7,m8]
        t_e = createHTM(0, 0, 0, 0)
        for m in t_matrices:
          t_e = np.matmul(t_e, m)

        print("m1-m5")
        print(t_e)

        events = inputs.get_gamepad()
        for event in events:
                if event.ev_type == "Key" or event.ev_type == "Absolute":
                        if event.code == "BTN_THUMB2" and event.state == 1:
                                #print('S1UP')
                                if servoangles[0] <= 175:
                                    servoangles[0] += 5
                        elif event.code == "BTN_THUMB" and event.state == 1:
                                #print('S1DOWN')
                                if servoangles[0] >= 5:
                                    servoangles[0] -= 5
                        elif event.code == "BTN_TOP" and event.state == 1:
                                #print('S2UP')
                                if servoangles[1] <= 175:
                                    servoangles[1] += 5
                        elif event.code == "BTN_TRIGGER" and event.state == 1:
                                #print('S2DOWN')
                                if servoangles[1] >= 5:
                                    servoangles[1] -= 5
                        elif event.code == "BTN_TOP2" and event.state == 1:
                                #print('S3UP')
                                if servoangles[2] <= 175:
                                    servoangles[2] += 5
                        elif event.code == "BTN_BASE" and event.state == 1:
                                #print('S3DOWN')
                                if servoangles[2] >= 5:
                                    servoangles[2] -= 5
                        elif event.code == "BTN_PINKIE" and event.state == 1:
                                #print('S4UP')
                                if servoangles[3] <= 175:
                                    servoangles[3] += 5
                        elif event.code == "BTN_BASE2" and event.state == 1:
                                #print('S4DOWN')
                                if servoangles[3] >= 5:
                                    servoangles[3] -= 5
                        elif event.code == "ABS_HAT0Y" and event.state == -1:
                                #print('S5UP')
                                if servoangles[4] <= 175:
                                    servoangles[4] += 5
                        elif event.code == "ABS_HAT0Y" and event.state == 1:
                                #print('S5DOWN')
                                if servoangles[4] >= 5:
                                    servoangles[4] -= 5
                        elif event.code == "ABS_HAT0X" and event.state == 1:
                                #print('S6UP')
                                if servoangles[5] <= 175:
                                    servoangles[5] += 5
                        elif event.code == "ABS_HAT0X" and event.state == -1:
                                #print('S6DOWN')
                                if servoangles[5] >= 5:
                                    servoangles[5] -= 5
                setServos(servos, servoangles)
        print("_"*50)
                     


if __name__ == '__main__':
    main()