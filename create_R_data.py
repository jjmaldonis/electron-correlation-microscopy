from __future__ import print_function
import sys
import json
import time
import numpy as np
from utilities import load_pixel_positions, load_mask, load_tif_data, load_R_pixel_positions



def main():
    paramfile = sys.argv[1]
    params = json.load(open(paramfile))

    nframes = params["nframes"]
    dt_range = params["dT range"]
    dr_range = params["dR range"]
    tsize = dt_range[1] - dt_range[0]
    rsize = dr_range[1] - dr_range[0]
    rscale = params["Rscale"]
    tscale = params["Tscale"]

    mask = load_mask(dataset_key=params["dataset_key"], rotate_mask=params["rotate mask"],
                    )
    print("Loaded mask.")
    pixel_positions = load_pixel_positions(mask)
    print("Loaded masked positions.")

    data = load_tif_data(nframes,
                         filename_base=params["tif_filename_base"],
                        )
    np.save("dtdata.npy", data)
    print(data.shape)
    print("Loaded tif data.")
    print("Min intensity of tifs:", np.nanmin(data))
    print("Max intensity of tifs:", np.nanmax(data))

    drshape = tuple(list(data.shape) + [dr_range[1]-dr_range[0]])
    print(drshape)
    drdata = np.zeros(drshape, dtype=np.float64)
    print("Created empty data.")
    drdata.fill(np.nan)
    print("Filled with nans.")
    drdata[:, :, :, 0] = data
    print("Set initial data.")
    assert (drdata[:, :, :, 0] == data).all()
    assert len(np.where(~np.isnan(drdata[:, :, :, 1:]))[0]) == 0
    print("Ran checks on initial data.")
    np.save("initialized_drdata.npy", drdata)
    print("Saved initial data.")


    width = 1.0
    #R = sys.argv[1]
    #R = float(R)

    for R in range(*dr_range):
        R = float(R)
        print("dR: {}".format(R))
        R_pixel_positions = load_R_pixel_positions(pixel_positions, R, width)
        print("Finished loading R_pixel_positions")
        for t in range(drdata.shape[0]):
            print("t: {}".format(t), end="; ")
            for (R,x,y), positions in R_pixel_positions.items():
                drdata[t, x, y, int(R)] = np.mean([data[t, x, y] for x,y in positions])
            print(t, x, y, int(R), drdata[t, x, y, int(R)])

    np.save("drdata.npy", drdata)

if __name__ == "__main__":
    main()

