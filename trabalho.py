import sys
import os


if __name__ == "__main__":

    args = sys.argv[1]

    if(args == "--r1"):
        exec(open("./intrinsicsCalibration.py").read())
    elif(args == "--r2"):
        exec(open("./extractFrames.py").read())
        exec(open("./extrinsicsCalibration.py").read())

    elif(args == "--r3"):
        exec(open("./disparityMap.py").read())

    elif(args == "--r4"):
        exec(open("./worldCoordinates.py").read())