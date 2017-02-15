import os
import numpy as np
import scipy.spatial.distance
from PIL import Image


def load_matplotlib():
    #%matplotlib inline
    import matplotlib
    import matplotlib.pyplot as plt
    import matplotlib.pylab as pylab
    import matplotlib.mlab as mlab
    import matplotlib.image as mpimg


def load_pixel_positions(filename=None):
    if filename is None:
        head, tail = os.path.split(__file__)
        filename = os.path.join(head, "nanowire_background.txt")
    mask = np.loadtxt(filename, skiprows=1)
    mask = np.rot90(np.fliplr(mask))
    pixel_positions = list(zip(*np.where(mask == 255)))
    return pixel_positions


def load(fn):
    return np.array(Image.open(fn))


def load_tif_data(nprocs=4):
    fns = ["tif/C250_0.1s_{i}.tif".format(i=str(i).zfill(4)) for i in range(4000)]

    data = np.zeros((247, 250, 4000), dtype=np.float)

    if nprocs == 1:
        for i, fn in enumerate(fns):
            data[:,:,i] = load(fn)
            #if i % 100 == 0:
            #    print("Loaded {}%".format(round(100.*i/4000)))
    else:
        from multiprocessing import Pool
        pool = Pool(processes=nprocs)
        for i, temp in enumerate(pool.map(load, fns)):
            #if i % 100 == 0:
            #    print("Loaded {}%".format(round(100.*i/4000)))
            data[:,:,i] = temp
        pool.close()
        pool.join()
    print("Finished loading data!")
    return data


def load_R_pixel_positions(pixel_positions, R, width):
    R2_start = R*R
    R2_end = (R+width)*(R+width)

    R_pixel_positions = {}
    for k, (x,y) in enumerate(pixel_positions):
        #fn = "R2xy_data/R={r}.({x},{y}).npy".format(r=R, x=x, y=y)
        fn = "R2xy_data/R={r}/R={r}.({x},{y}).npy".format(r=R, x=x, y=y)
        try:
            #try:
            r_away = np.load(fn)
            #if k % 1000 == 0:
            #    print("Loaded precomputed R pixel position data:", R, k, len(pixel_positions))
            #except IOError:
            #    fn = "R2xy_data/R={r}/R={r}.({x},{y}).npy".format(r=R, x=x, y=y)
            #    r_away = np.load(fn)
        except IOError:
            #fn = "R2xy_data/R={r}.({x},{y}).npy".format(r=R, x=x, y=y)
            #print("WARNING! Could not find {}".format(fn))
            dists2 = scipy.spatial.distance.cdist([[x,y]], pixel_positions, metric="sqeuclidean").flatten() ###
            r_away = np.where( (R2_start <= dists2) & (dists2 < R2_end) )[0]
            r_away = [pixel_positions[i] for i in r_away]
            r_away = np.array(r_away, dtype=np.int32)
            np.save(file=fn, arr=r_away)
            #if k % 100 == 0:
            #    print("Precomputed R pixel position data:", R, k, len(pixel_positions))

        R_pixel_positions[(R,x,y)] = r_away

    for k, v in R_pixel_positions.items():
        if v.ndim != 2:
            R_pixel_positions[k] = v.reshape((1,2))

    print("Successfully loaded R={}".format(R))
    return R_pixel_positions


