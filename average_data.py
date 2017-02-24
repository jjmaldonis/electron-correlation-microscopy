import os, sys
import numpy as np
from utilities import load_pixel_positions
from utilities import load_tif_data

def main():
    pixel_positions = load_pixel_positions()

    fns = ["individual_spatial_data/({},{}).data".format(i,j) for i,j in pixel_positions]

    #average = np.zeros((2900,499), dtype=np.float)
    average = np.zeros((10,100), dtype=np.float)
    for i, fn in enumerate(fns):
        average += np.loadtxt(fn)/37761.0
        if i % 1000 == 0:
            np.savetxt("avg_spatial_{i}.txt".format(i=i), average)
            print("Saved avg_spatial_{i}.txt".format(i=i))
    np.savetxt("avg_spatial_final.txt", average)


if __name__ == "__main__":
    main()

