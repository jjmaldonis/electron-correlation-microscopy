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
        filename = os.path.join(head, "nanowire_background_C242.txt")
    mask = np.loadtxt(filename, skiprows=1)
    #mask = np.rot90(np.fliplr(mask))  # This mask isn't rotated with respect to the tifs
    mask = mask[:, :195]  # Correct for the mask slightly, see notebook title "Aligning the Mask with the Tifs"
    pixel_positions = list(zip(*np.where(mask == 255)))
    return pixel_positions


def load(fn):
    return np.array(Image.open(fn))


def load_tif_data(nframes, nprocs=4):
    fns = ["tif/C246_{i}.tif".format(i=str(i).zfill(4)) for i in range(nframes)]  # the tif filesnames are C246, but they should be C242. they were just named incorrectly

    data = np.zeros((151,195, nframes), dtype=np.float)

    for i, fn in enumerate(fns):
        data[:,:,i] = load(fn)
    print("Finished loading data!")

    return data


def load_R_pixel_positions(pixel_positions, R, width):
    R2_start = R*R
    R2_end = (R+width)*(R+width)

    R_pixel_positions = {}
    for k, (x,y) in enumerate(pixel_positions):
        fn = "R2xy_data/R={r}/R={r}.({x},{y}).npy".format(r=R, x=x, y=y)
        try:
            r_away = np.load(fn)
        except IOError:
            dists2 = scipy.spatial.distance.cdist([[x,y]], pixel_positions, metric="sqeuclidean").flatten() ###
            r_away = np.where( (R2_start <= dists2) & (dists2 < R2_end) )[0]
            r_away = [pixel_positions[i] for i in r_away]
            r_away = np.array(r_away, dtype=np.int32)
            np.save(file=fn, arr=r_away)

        R_pixel_positions[(R,x,y)] = r_away

    for k, v in R_pixel_positions.items():
        if v.size > 0 and v.ndim != 2:
            R_pixel_positions[k] = v.reshape((1,2))

    print("Successfully loaded R={}".format(R))
    return R_pixel_positions


