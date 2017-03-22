import sys
import os
import json
import numpy as np


def g4(x, y, dts, dtl, data):
    X, Y, Nt = data.shape
    It = data[:, :, 0:Nt-dts-dtl]
    Its = data[:, :, dts:Nt-dtl]
    Itl = data[:, :, dtl:Nt-dts]
    Itstl = data[:, :, dts+dtl:Nt]
    return np.nanmean(It * Its * Itl * Itstl) / (
            np.nanmean(It) * np.nanmean(Its) * np.nanmean(Itl) * np.nanmean(Itstl)
           )


def main():
    paramfile = sys.argv[1]
    params = json.load(open(paramfile))

    dir = "results/{}".format(params["dataset_key"])
    if not os.path.exists(dir):
        os.makedirs(dir)
    dts_range = params["dTs range"]
    dtl_range = params["dTl range"]
    dtssize = dts_range[1] - dts_range[0]
    dtlsize = dtl_range[1] - dtl_range[0]

    mask = load_mask(dataset_key=params["dataset_key"], rotate_mask=params["rotate mask"])
    print("Loaded mask.")
    pixel_positions = load_pixel_positions(mask)
    print("Loaded masked positions.")

    if os.path.exists(os.path.join(dir, "dtdata.npy")):
        data = np.load(os.path.join(dir, "dtdata.npy"))
    elif os.path.exists("dtdata.npy"):
        data = np.load("dtdata.npy")
    else:
        raise RuntimeError("Couldn't find data")
    print("Loaded data.")

    result = np.zeros((dtssize, dtlsize), dtype=np.float)

    for x,y in pixel_positions:
        for dts in range(*dts_range):
            for dtl in range(*dtl_range):
                if dtl < dts: continue
                result[dts, dtl] = g4(x, y, dts, dtl, data)
                print("dts", dts, "dtl", dtl, result[dts, dtl])

        np.savetxt(os.path.join(dir, "G4_time_{}_{}.txt".format(x,y)), result)
        print("Saved G4 results to", os.path.join(dir, "G4_time_{}_{}.txt".format(x,y)))


if __name__ == "__main__":
    main()

