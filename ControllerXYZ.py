import inputs
from decimal import Decimal

"""
Returns an x,y,z vector from the current controller inputs.
"""

def getXYZ(prev_coord, prev_gradient):
    speed = 0.1
    null_zone = 0

    events = inputs.get_gamepad()
    gradient = prev_gradient

    for event in events:
        # print(event.ev_type, event.code, event.state)
        type = str(event.ev_type)
        code = str(event.code)
        state = int(event.state)

        if (type == "Absolute"):
            state = (state - 127.5) / 127.5 * speed

            if (abs(state) < null_zone):
                state = 0

            if (code == "ABS_X"):
                gradient[0] = state
            elif (code == "ABS_Y"):
                gradient[1] = -state
            elif (code == "ABS_RZ"):
                gradient[2] = -state

    new_coord = [0,0,0]
    for i in range(3):
        new_coord[i] = prev_coord[i] + gradient[i]

    return new_coord, gradient

def main():
    coord = [0,0,0]
    gradient = [0,0,0]
    while 1:
        getXYZ()

if __name__ == '__main__':
	main()
