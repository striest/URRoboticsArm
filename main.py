from gpiozero import AngularServo
import inputs

servos = []

def setServos(servos, angles):
    '''
    Set the servos in teh servo array to corresponding angles
    '''
    
    for i in range(len(servos)):
        servos[i].angle = angles[i]
  
def main():
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
    

    while 1:
            events = inputs.get_gamepad()
            for event in events:
                    if event.ev_type == "Key" or event.ev_type == "Absolute":
                            if event.code == "BTN_THUMB2" and event.state == 1:
                                    print('S1UP')
                                    if servoangles[0] <= 175:
                                        servoangles[0] += 5
                            elif event.code == "BTN_THUMB" and event.state == 1:
                                    print('S1DOWN')
                                    if servoangles[0] >= 5:
                                        servoangles[0] -= 5
                            elif event.code == "BTN_TOP" and event.state == 1:
                                    print('S2UP')
                                    if servoangles[1] <= 175:
                                        servoangles[1] += 5
                            elif event.code == "BTN_TRIGGER" and event.state == 1:
                                    print('S2DOWN')
                                    if servoangles[1] >= 5:
                                        servoangles[1] -= 5
                            elif event.code == "BTN_TOP2" and event.state == 1:
                                    print('S3UP')
                                    if servoangles[2] <= 175:
                                        servoangles[2] += 5
                            elif event.code == "BTN_BASE" and event.state == 1:
                                    print('S3DOWN')
                                    if servoangles[2] >= 5:
                                        servoangles[2] -= 5
                            elif event.code == "BTN_PINKIE" and event.state == 1:
                                    print('S4UP')
                                    if servoangles[3] <= 175:
                                        servoangles[3] += 5
                            elif event.code == "BTN_BASE2" and event.state == 1:
                                    print('S4DOWN')
                                    if servoangles[3] >= 5:
                                        servoangles[3] -= 5
                            elif event.code == "ABS_HAT0Y" and event.state == -1:
                                    print('S5UP')
                                    if servoangles[4] <= 175:
                                        servoangles[4] += 5
                            elif event.code == "ABS_HAT0Y" and event.state == 1:
                                    print('S5DOWN')
                                    if servoangles[4] >= 5:
                                        servoangles[4] -= 5
                            elif event.code == "ABS_HAT0X" and event.state == 1:
                                    print('S6UP')
                                    if servoangles[5] <= 175:
                                        servoangles[5] += 5
                            elif event.code == "ABS_HAT0X" and event.state == -1:
                                    print('S6DOWN')
                                    if servoangles[5] >= 5:
                                        servoangles[5] -= 5
                    setServos(servos, servoangles)
                            

if __name__ == '__main__':
    main()