import sys
import os
import json
import time
import numpy as np

from utilities import load_pixel_positions, load_mask, load_tif_data, load_R_pixel_positions


def create_tif_box(params, dir):
    print("Creating TIF box...")
    nframes = len(os.listdir("tif/"))
    data = load_tif_data(nframes, filename_base=params["tif_filename_base"])
    np.save(os.path.join(dir, "dtdata.npy"), data)
    return data


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
    rscale = params["Rscale"]
    tscale = params["Tscale"]

    mask = load_mask(dataset_key=params["dataset_key"], rotate_mask=params["rotate mask"])
    print("Loaded mask.")
    pixel_positions = load_pixel_positions(mask)
    print("Loaded masked positions.")


    if os.path.exists(os.path.join(dir, "dtdata.npy")):
        data = np.load(os.path.join(dir, "dtdata.npy"))
    elif os.path.exists("dtdata.npy"):
        data = np.load("dtdata.npy")
    else:
        data = create_tif_box(params, dir)
    print("Loaded tif data.")
    print("Shape:", data.shape)
    print("Min intensity of tifs:", np.nanmin(data))
    print("Max intensity of tifs:", np.nanmax(data))

    # The data format is:
    # data[x, y, t] (i.e. the frame # is the last index)

    drdata = data.copy()
    width = 1.0

    zip2where = lambda t: (np.array(next(t)), np.array(next(t)))

    for R in range(*dr_range):
        R = float(R)
        print("dR: {}".format(R))
        R_pixel_positions = load_R_pixel_positions(params["dataset_key"], pixel_positions, R, width)
        print("Finished loading R_pixel_positions")

        for (R,x,y), positions in R_pixel_positions.items():
            R_pixel_positions[(R,x,y)] = zip2where(zip(*positions))
        print("Re-rendered R_pixel_positions into np.where format")
        rsize = len(R_pixel_positions)

        for i, ((R,x,y), positions) in enumerate(R_pixel_positions.items()):
            #if i % 100 == 0 and i > 0:
            #    print(i, rsize, end=" ", flush=True)
            drdata[x, y, :] = np.mean(data[positions], axis=0)

        np.save(os.path.join(dir, "drdata_{R}.npy".format(R=int(R))), drdata)


if __name__ == "__main__":
    main()

