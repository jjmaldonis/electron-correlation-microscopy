import sys
import time
import numpy as np
from utilities import load_pixel_positions
from utilities import load_R_pixel_positions



def main():
    pixel_positions = load_pixel_positions()

    width = 1.0
    R = sys.argv[1]
    R = float(R)

    R_pixel_positions = load_R_pixel_positions(pixel_positions, R, width)


if __name__ == "__main__":
    main()
