import sys
import os
import json
import numpy as np


def g4(dt, dr, data):
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
    X, Y, Nt = data0.shape
    Itr = data0[:, :, 0:Nt-dt]
    Idtr = data0[:, :, dt:Nt]
    Itdr = data_dr[:, :, 0:Nt-dt]
    Idtdr = data_dr[:, :, dt:Nt]
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

    data0 = np.load(os.path.join(dir, "dtdata.npy"))

    result = np.zeros((rsize, tsize), dtype=np.float)

    for dr in range(*dr_range):
        data_dr = np.load(os.path.join(dir, "drdata_{}.npy".format(dr)))
        for dt in range(*dt_range):
            result[dr, dt] = g4_from_slices(dt, dr, data0, data_dr)
            print("dr", dr, "dt", dt, result[dt, dr])

    np.savetxt(os.path.join(dir, "G4.txt"), result)
    print("Saved G4 results to", os.path.join(dir, "G4.txt"))


if __name__ == "__main__":
    main()

