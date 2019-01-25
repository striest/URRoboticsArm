import inputs

"""
Returns an x,y,z vector from the current controller inputs.
"""

def getXYZ():
    events = inputs.get_gamepad()
    for event in events:
        print(event.ev_type, event.code, event.state)

def main():
    while 1:
        getXYZ()

if __name__ == '__main__':
    main()
