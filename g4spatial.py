import sys
import os
import json
import numpy as np

from utilities import load_pixel_positions, load_mask


def g4(dt, dr, data):
    # TODO This assumes the background has been replaced with nans
    X, Y, Nt, Nr = data.shape
    Itr = data[:, :, 0:Nt-dt, 0]
    Idtr = data[:, :, dt:Nt, 0]
    Itdr = data[:, :, 0:Nt-dt, dr]
    Idtdr = data[:, :, dt:Nt, dr]
    return np.nanmean(Itr * Idtr * Itdr * Idtdr) / (
            np.nanmean(Itr) * np.nanmean(Idtr) * np.nanmean(Itdr) * np.nanmean(Idtdr)
           )


def g4_from_slices(dt, dr, data0, data_dr):
    assert data0.shape == data_dr.shape
    Nt = data0.shape[-1]
    Itr = data0[:, 0:Nt-dt]
    Idtr = data0[:, dt:Nt]
    Itdr = data_dr[:, 0:Nt-dt]
    Idtdr = data_dr[:, dt:Nt]
    return np.nanmean(Itr * Idtr * Itdr * Idtdr) / (
            np.nanmean(Itr) * np.nanmean(Idtr) * np.nanmean(Itdr) * np.nanmean(Idtdr)
           )



def main():
    paramfile = sys.argv[1]
    params = json.load(open(paramfile))

    dir = "results/{}".format(params["dataset_key"])
    if not os.path.exists(dir):
        os.makedirs(dir)
    dt_range = params["dT range"]
    dr_range = params["dR range"]
    tsize = dt_range[1] - dt_range[0]
    rsize = dr_range[1] - dr_range[0]

    mask = load_mask(dataset_key=params["dataset_key"], rotate_mask=params["rotate mask"])
    print("Loaded mask.")
    pixel_positions = load_pixel_positions(mask)
    print("Loaded masked positions.")

    if os.path.exists(os.path.join(dir, "dtdata.npy")):
        data0 = np.load(os.path.join(dir, "dtdata.npy"))
    elif os.path.exists("dtdata.npy"):
        data0 = np.load("dtdata.npy")
    else:
        raise RuntimeError("Couldn't find data")
    print("Loaded tif data.")

    zip2where = lambda t0: (np.array(next(t0)), np.array(next(t0)))

    result = np.zeros((rsize, tsize), dtype=np.float)

    # G4 can be parallelized at the (dr, dt) scale, but then the loading overhead is almost
    # as much as the calculation. In order to avoid that much unncessary calculation, we
    # should split those calculations up. However, running all drs means we need to pass in
    # all the data. On the other hand, the dt size is 100, which will take quite a bit of time,
    # and we'd only be submitting 10 jobs. Still, I'm thinking about going that route.
    for dr in range(*dr_range):
        data_dr = np.load(os.path.join(dir, "drdata_{}.npy".format(dr)))
        for dt in range(*dt_range):
            result[dr, dt] = g4_from_slices(dt, dr, data0[zip2where(zip(*pixel_positions))], data_dr[zip2where(zip(*pixel_positions))])
            print("dr", dr, "dt", dt, result[dr, dt])

    np.savetxt(os.path.join(dir, "G4.txt"), result)
    print("Saved G4 results to", os.path.join(dir, "G4.txt"))


if __name__ == "__main__":
    main()

