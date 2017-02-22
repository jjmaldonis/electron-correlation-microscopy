import sys
import time
import numpy as np
from utilities import load_pixel_positions
from utilities import load_R_pixel_positions
from utilities import load_tif_data




def _calculate(args):
    data, R_pixel_positions, dt, R, x, y, t_size, len_pixel_positions = args
    r_away = R_pixel_positions[(R,x,y)]
    r_size = len(r_away)
    denom = 1. / (t_size*r_size*len_pixel_positions)
    return sum(data[x,y,t] * data[dx,dy,t] * data[x,y,t+dt] * data[dx,dy,t+dt] * denom
               for dx, dy in r_away
               for t in range(t_size)
              )

def g4_spatial(data, pixel_positions, x, y, dt, R, width, R_pixel_positions=None, nprocs=4):
    if R_pixel_positions is None:
        R_pixel_positions = load_R_pixel_positions(pixel_positions, R, width)

    t_size = data.shape[2] - dt
    len_pixel_positions = len(pixel_positions)

    totals = {}

    start = time.time()
    if nprocs == 1:
        total = _calculate([data, R_pixel_positions, dt, R, x, y, t_size, len_pixel_positions])
        return total
    else:
        from multiprocessing import Pool
        pool = Pool(processes=nprocs)
        args = ([data, R_pixel_positions, dt, R, x, y, t_size, len_pixel_positions] for i, (x,y) in enumerate(pixel_positions))
        for i, temp in enumerate(pool.map(_calculate, args)):
            x, y = pixel_positions[i]
            totals[(x,y)] = temp
            #print("{}, {}: ({},{}): {}".format(i, len_pixel_positions, x, y, totals[(x,y)]))
        pool.close()
        pool.join()

    return sum(totals.values())


def run_one(x, y, dt, R, width, pixel_positions=None, data=None, R_pixel_positions=None):
    if pixel_positions is None:
        pixel_positions = load_pixel_positions()
    if data is None:
        data = load_tif_data(nframes=4071, nprocs=1)
    if R_pixel_positions is None:
        R_pixel_positions = load_R_pixel_positions(pixel_positions, R, width)

    g4 = g4_spatial(data, pixel_positions, x=x, y=y, dt=dt, R=R, width=width, R_pixel_positions=R_pixel_positions, nprocs=1)

    return g4


def run_many(dts, Rs):
    pixel_positions = load_pixel_positions()
    data = load_tif_data(nframes=4071, nprocs=1)

    width = 1.0

    import time
    for R in Rs:
        for dt in dts:
            start = time.time()
            g4 = g4_spatial(data, pixel_positions, dt=dt, R=R, width=width, nprocs=1)
            print(dt, R, g4, time.time()-start)

            #with open("spatial_results/dt={dt}.R={R}.data".format(dt=dt, R=R), "w") as f:
            #    f.write(str(g4))


if __name__ == "__main__":
    pixel_positions = load_pixel_positions()
    data = load_tif_data(nframes=4071, nprocs=1)

    width = 1.0
    x, y = sys.argv[1:]
    x = int(x)
    y = int(y)
    image = np.zeros((10,100))
    image.fill(np.nan)
    for R in range(1,11):
        R = float(R)
        start = time.time()
        R_pixel_positions = load_R_pixel_positions(pixel_positions, R, width)
        for dt in range(1,101):
            g4 = run_one(x, y, dt, R, width, pixel_positions=pixel_positions, data=data, R_pixel_positions=R_pixel_positions)
            image[int(R)-1,dt-1] = g4
    np.savetxt("({x},{y}).data".format(x=x, y=y), image)


    # Make matplotlib image
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    _image = image[:,:100]
    dtl_range = (1,100)
    dts_range = (1,10)
    fig, ax = plt.subplots(figsize=(32,8))
    img = ax.imshow(_image)
    ax.set_title("G4 spatial - for pixel ({}, {})".format(x,y))
    ax.set_ylabel("dR")
    ax.set_xlabel("dT")
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    DT = 0.25
    DX = 0.3293
    plt.xticks(np.arange(0, _image.shape[1], 2), DT*np.array(np.arange(dtl_range[0], dtl_range[1], 2, dtype=float), dtype=int))
    plt.yticks(np.arange(0, _image.shape[0], 1), DX*np.arange(dts_range[0], dts_range[1], 1, dtype=float))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="2%", pad=0.05)
    plt.colorbar(img, cax=cax)
    plt.savefig("({x},{y}).png".format(x=x, y=y))
    plt.close()



    #dt, R, width = sys.argv[1:]
    #dt = int(dt)
    #R = float(R)
    #width = float(width)
    #g4 = run_one(130, 130, dt, R, width, pixel_positions, data)

