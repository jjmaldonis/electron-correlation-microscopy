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

from mpl_toolkits.axes_grid1 import make_axes_locatable


def save_png(fn):
    try:
        data = np.loadtxt(fn)
    except:
        print("{}.png FAILED".format(fn[:-4]))
        return "{}.png FAILED".format(fn[:-4])
    dts_range = (1, 500)
    dtl_range = (100, 3000)

    fig, ax = plt.subplots(figsize=(20, 10))

    img = ax.imshow(data.T)
    ax.set_ylabel("delta-T short (s)")
    ax.set_xlabel("delta-T long (s)")
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    plt.xticks(np.arange(0, data.T.shape[1], 50),
               np.array(0.1*np.arange(dtl_range[0], dtl_range[1], 50, dtype=float), dtype=int))
    plt.yticks(np.arange(0, data.T.shape[0], 20),
              0.1*np.arange(dts_range[0], dts_range[1], 20, dtype=float))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="2%", pad=0.05)
    plt.colorbar(img, cax=cax)

    plt.savefig("{}.png".format(fn[:-4]))
    plt.close()
    print("Saved {}.png".format(fn[:-4]))
    return "{}.png".format(fn[:-4])

def main():
    save_png(sys.argv[1])
    #mask = np.loadtxt("nanowire_background.txt", skiprows=1)
    #pixel_positions = zip(*np.where(mask == 255))

    #fns = ["g4results/C250_0.1s_{i}_{j}.g4data.txt".format(i=i, j=j) for i,j in pixel_positions]
    #pngs = [f for f in os.listdir("g4results") if ".png" in f]
    #fns = [f for f in fns if "{}.png".format(f[10:-4]) not in pngs]
    fns = ["avg0.txt", "avg1000.txt", "avg2000.txt", "avg3000.txt", "avg4000.txt", "avg5000.txt", "avg6000.txt", "avg7000.txt", "avg8000.txt", "avg9000.txt", "avg10000.txt", "avg11000.txt", "avg12000.txt", "avg13000.txt", "avg14000.txt", "avg15000.txt", "avg16000.txt", "avg17000.txt", "avg18000.txt", "avg19000.txt", "avg20000.txt", "avg21000.txt", "avg22000.txt", "avg23000.txt", "avg24000.txt", "avg25000.txt", "avg26000.txt", "avg27000.txt", "avg28000.txt", "avg29000.txt", "avg30000.txt", "avg31000.txt", "avg32000.txt", "avg33000.txt", "avg34000.txt", "avg35000.txt", "average_data.py", "avg36000.txt", "avg37000.txt"]


    #for i, fn in enumerate(map(save_png, fns)):
    #    pass

    #from multiprocessing import Pool
    #pool = Pool(processes=20)
    #for i, fn in enumerate(pool.map(save_png, fns)):
    #    #print("Saved {}".format(fn))
    #    pass
    #pool.close()
    #pool.join()


if __name__ == "__main__":
    main()

