import sys
import os
import json
import numpy as np


def g2(dt, data):
    X, Y, Nt = data.shape
    Itr = data[:, :, 0:Nt-dt]  # dr = 0
    Idtr = data[:, :, dt:Nt]  # dr = 0
    return np.nanmean(Itr * Idtr, axis=2) / (
            np.nanmean(Itr, axis=2) * np.nanmean(Idtr, axis=2)
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

    if os.path.exists(os.path.join(dir, "dtdata.npy")):
        data = np.load(os.path.join(dir, "dtdata.npy"))
    elif os.path.exists("dtdata.npy"):
        data = np.load("dtdata.npy")
    else:
        raise RuntimeError("Couldn't find data")
    X, Y, nframes = data.shape

    result = np.zeros((tsize, X, Y))

    for dt in range(*dt_range):
        result[dt, :, :] = g2(dt, data)
        print(dt, end=" ", flush=True)
    print()

    np.save(os.path.join(dir, "G2_time.npy"), result)
    np.savetxt(os.path.join(dir, "G2_time.txt"), result)
    print("Saved G2 results to", os.path.join(dir, "G2_time.txt"))


if __name__ == "__main__":
    main()

