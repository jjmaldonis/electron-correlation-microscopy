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

def g4_spatial(data, pixel_positions, dt, R, width, nprocs=4):
    R_pixel_positions = load_R_pixel_positions(pixel_positions, R, width)

    t_size = data.shape[2] - dt
    len_pixel_positions = len(pixel_positions)

    totals = {}

    start = time.time()
    if nprocs == 1:
        for i, (x,y) in enumerate(pixel_positions):
            totals[(x,y)] = _calculate([data, R_pixel_positions, dt, R, x, y, t_size, len_pixel_positions])
            if i % 1000 == 0 and i > 0:
                print("({},{}): {} took {}".format(x,y,totals[(x,y)], (time.time()-start)/1000))
                start = time.time()
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


def run_one(dt, R, width, pixel_positions=None, data=None):
    if pixel_positions is None:
        pixel_positions = load_pixel_positions()
    if data is None:
        data = load_tif_data(nprocs=1)

    g4 = g4_spatial(data, pixel_positions, dt=dt, R=R, width=width, nprocs=1)
    print(dt, R, g4)

    with open("spatial_results/dt={dt}.R={R}.data".format(dt=dt, R=R), "w") as f:
        f.write(str(g4))

    return g4


def run_all():
    pixel_positions = load_pixel_positions()
    data = load_tif_data(nprocs=1)

    dts = list(range(1, 500))
    width = 1.0
    Rs = np.arange(1., 100., width)

    for dt in dts:
        for R in Rs:
            g4 = g4_spatial(data, pixel_positions, dt=dt, R=R, width=width, nprocs=1)
            print(dt, R, g4)

            with open("spatial_results/dt={dt}.R={R}.data".format(dt=dt, R=R), "w") as f:
                f.write(str(g4))


if __name__ == "__main__":
    pixel_positions = load_pixel_positions()
    data = load_tif_data(nprocs=1)

    dt, R, width = sys.argv[1:]
    dt = int(dt)
    R = float(R)
    width = float(width)
    g4 = run_one(dt, R, width, pixel_positions, data)

