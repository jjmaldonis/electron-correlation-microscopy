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


def load_mask(filename=None, dataset_key=None, rotate_mask=True, xstart=0, xend=None, ystart=0, yend=None):
    if filename is None:
        head, tail = os.path.split(__file__)
        filename = os.path.join(head, "masks/mask_{key}.txt".format(key=dataset_key))
    mask = np.loadtxt(filename)
    mask = np.rot90(np.fliplr(mask))
    if xend is None:
        xend = mask.shape[0]
    if yend is None:
        yend = mask.shape[1]
    mask = mask[xstart:xend, ystart:yend]
    return mask


def load_pixel_positions(mask):
    pixel_positions = list(zip(*np.where(mask == 0)))
    return pixel_positions


def load(fn):
    return np.array(Image.open(fn))


def load_tif_data(nframes, filename_base, xstart=0, xend=None, ystart=0, yend=None):
    fns = ["tif/{base}_{i}.tif".format(i=str(i).zfill(4), base=filename_base) \
           for i in range(nframes)]

    # Load one tif to get the size
    tif = load(fns[0])
    xsize, ysize = tif.shape

    if xend is None:
        xend = xsize
    if yend is None:
        yend = ysize

    xsize = xend - xstart
    ysize = yend - ystart

    data = np.zeros((xsize, ysize, nframes), dtype=np.float)

    for i, fn in enumerate(fns):
        data[:,:,i] = load(fn)[xstart:xend, ystart:yend]
    print("Finished loading data!")

    return data


def load_R_pixel_positions(dataset_key, pixel_positions, R, width):
    R2_start = R*R
    R2_end = (R+width)*(R+width)

    R_pixel_positions = {}
    for k, (x,y) in enumerate(pixel_positions):
        fn = "results/{key}/R2xy_data/R={r}/R={r}.({x},{y}).npy".format(key=dataset_key, r=R, x=x, y=y)
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

