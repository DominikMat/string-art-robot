# String Art Robot

A machine to draw string art designes on a circular ring of nails automatiacally,

# sequence visualizer
The sequence visuallizer is written in python and uses the turtle library, 
it can display various different nails sequences, after which they 
can be copied to the robot.

# robot
A servo and stepper motor controlled by a raspberry pi pico (the stepper also uses a 
ULM2003 chip for control). The microcontroller reads the sequence and controls the 
components to draw the design on the ring.

# gearing 
the stepper motor and the nail ring are geared with a 4 to 1 reduction
(4 stepper revolution = 1 ring revolution)

# presentation
This robot has been created for the Intro to Robotics course at the University of the Aegean in Greece,
the main components and functions are showns in the accompanying presentation:
https://docs.google.com/presentation/d/1VIfVSTO9Wcaq9Rl0Zi-_Bw-y_5G3Nwj30t2qu21ZTrM/edit?usp=sharing
