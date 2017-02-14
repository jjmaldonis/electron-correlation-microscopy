import os, sys
import numpy as np
import scipy.signal
from scipy.optimize import curve_fit
from PIL import Image

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
plt.ioff()

from dask import delayed


def main():
    #directory = "g4test"
    #lazy_dataframes = [delayed(np.loadtxt)(os.path.join(directory, filename)) for
    #    filename in os.listdir(directory) if '.txt' in filename]
    #mean = delayed(np.mean)(lazy_dataframes)
    #result = mean.compute()
    #print(result)
    #return
    mask = np.loadtxt("nanowire_background.txt", skiprows=1)
    pixel_positions = zip(*np.where(mask == 255))

    fns = ["g4results/C250_0.1s_{i}_{j}.g4data.txt".format(i=i, j=j) for i,j in pixel_positions]
    #pngs = [f for f in os.listdir("g4results") if ".png" in f]
    #fns = [f for f in fns if "{}.png".format(f[10:-4]) not in pngs]


    #fns = fns[35000:]
    #print(fns[0])
    #return
    #average = np.loadtxt("avg35000.txt")

    average = np.zeros((2900,499), dtype=np.float)
    for i, fn in enumerate(fns):
        average += np.loadtxt(fn)/37761.0
        print(fn)
        if i % 1000 == 0:
            np.savetxt("avg{i}.txt".format(i=i), average)
            print("Saved avg")
    np.savetxt("avg.txt", average)

    fig, ax = plt.subplots(figsize=(20, 10))
    img = ax.imshow(average.T)
    plt.savefig("avg.png")
    plt.close()


if __name__ == "__main__":
    main()

