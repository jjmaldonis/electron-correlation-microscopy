import sys
import os
import json
import numpy as np


def g2(dr, data):
    X, Y, Nt, Nr = data.shape
    Itr = data[:, :, :, 0]
    Itdr = data[:, :, :, dr]
    return np.nanmean(Itr * Itdr, axis=(0,1)) / (
            np.nanmean(Itr, axis=(0,1)) * np.nanmean(Itdr, axis=(0,1))
           )


#def g2_from_slices(data0, data_dr):
#    assert data0.shape == data_dr.shape
#    Itr = data0
#    Itdr = data_dr
#    return np.nanmean(Itr * Itdr, axis=(0,1)) / (
#            np.nanmean(Itr, axis=(0,1)) * np.nanmean(Itdr, axis=(0,1))
#           )



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
    nframes = 3967

    if os.path.exists(os.path.join(dir, "drdtdata.npy")):
        data = np.load(os.path.join(dir, "drdtdata.npy"))
    elif os.path.exists("drdtdata.npy"):
        data = np.load("drdtdata.npy")
    else:
        raise RuntimeError("Couldn't find data")

    result = np.zeros((rsize, nframes), dtype=np.float)

    for dr in range(*dr_range):
        result[dr] = g2(dr, data)
        print("dr", dr, result[dr])

    np.savetxt(os.path.join(dir, "G2_spatial.txt"), result)
    print("Saved G2 results to", os.path.join(dir, "G2_spatial.txt"))


if __name__ == "__main__":
    main()

