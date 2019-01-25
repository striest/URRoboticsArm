from gpiozero import AngularServo

a = AngularServo(2,min_angle = 0,max_angle = 180,min_pulse_width = .0005,max_pulse_width = .0025)
b = AngularServo(3,min_angle = 0,max_angle = 180,min_pulse_width = .0005,max_pulse_width = .0025)
c = AngularServo(4,min_angle = 0,max_angle = 180,min_pulse_width = .0005,max_pulse_width = .0025)
d = AngularServo(5,min_angle = 0,max_angle = 180,min_pulse_width = .0005,max_pulse_width = .0025)
e = AngularServo(6,min_angle = 0,max_angle = 180,min_pulse_width = .0005,max_pulse_width = .0025)
f = AngularServo(7,min_angle = 0,max_angle = 180,min_pulse_width = .0005,max_pulse_width = .0025)

def get_servos(self):
    servos = [a, b, c, d, e,f]
    return servos
