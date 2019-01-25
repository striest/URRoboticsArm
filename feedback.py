from gpiozero import Servo
from gpiozero import GPIODevice
from time import sleep

s = Servo(2)
p = GPIODevice(3)


while True:
	s.mid()
	print(p.value)
	sleep(3)
	s.max()
	print(p.value)
	sleep(3)
	s.mid()
	print(p.value)
	sleep(3)
	s.min()
	print(p.value)
	sleep(3)