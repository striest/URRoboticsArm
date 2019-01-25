import inputs

for device in inputs.devices:
	print(device)

servoangles = [0] * 6

while 1:
	events = inputs.get_gamepad()
	for event in events:
		if event.ev_type == "Key" or event.ev_type == "Absolute":
			if event.code == "BTN_THUMB2" and event.state == 1:
				print('S1UP')
			elif event.code == "BTN_THUMB" and event.state == 1:
				print('S1DOWN')
			elif event.code == "BTN_TOP" and event.state == 1:
				print('S2UP')
			elif event.code == "BTN_TRIGGER" and event.state == 1:
				print('S2DOWN')
			elif event.code == "BTN_TOP2" and event.state == 1:
				print('S3UP')
			elif event.code == "BTN_BASE" and event.state == 1:
				print('S3DOWN')
			elif event.code == "BTN_PINKIE" and event.state == 1:
				print('S4UP')
			elif event.code == "BTN_BASE2" and event.state == 1:
				print('S4DOWN')
			elif event.code == "ABS_HAT0Y" and event.state == -1:
				print('S5UP')
			elif event.code == "ABS_HAT0Y" and event.state == 1:
				print('S5DOWN')
			elif event.code == "ABS_HAT0X" and event.state == 1:
				print('S6UP')
			elif event.code == "ABS_HAT0X" and event.state == -1:
				print('S6DOWN')
			