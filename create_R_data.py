import sys
import os
import json
import time
import numpy as np
from utilities import load_pixel_positions, load_mask, load_tif_data, load_R_pixel_positions



def main():
    paramfile = sys.argv[1]
    params = json.load(open(paramfile))

    dir = "results/{}".format(params["dataset_key"])
    if not os.path.exists(dir):
        os.makedirs(dir)
    nframes = params["nframes"]
    dt_range = params["dT range"]
    dr_range = params["dR range"]
    tsize = dt_range[1] - dt_range[0]
    rsize = dr_range[1] - dr_range[0]
    rscale = params["Rscale"]
    tscale = params["Tscale"]

    mask = load_mask(dataset_key=params["dataset_key"], rotate_mask=params["rotate mask"],
                     xstart=50, xend=100, ystart=50, yend=100  # TODO DELETE
                    )
    print("Loaded mask.")
    pixel_positions = load_pixel_positions(mask)
    print("Loaded masked positions.")

    data = load_tif_data(nframes,
                         filename_base=params["tif_filename_base"],
                         xstart=50, xend=100, ystart=50, yend=100  # TODO DELETE
                        )
    data = data[:, :, :100]  # TODO DELETE
    np.save(os.path.join(dir, "dtdata.npy"), data)
    print(data.shape)
    print("Loaded tif data.")
    print("Min intensity of tifs:", np.nanmin(data))
    print("Max intensity of tifs:", np.nanmax(data))

    # The data format is:
    # data[x, y, t] (i.e. the frame # is the last index)

    #drshape = tuple(list(data.shape) + [dr_range[1]-dr_range[0]])
    drshape = data.shape
    print(drshape)
    drdata = np.zeros(drshape, dtype=np.float64)
    print("Created empty data.")
    drdata.fill(np.nan)
    print("Filled with nans.")
    #drdata[:, :, :, 0] = data
    drdata = data.copy()
    print("Set initial data.")
    #assert (drdata[:, :, :, 0] == data).all()
    #assert len(np.where(~np.isnan(drdata[:, :, :, 1:]))[0]) == 0
    #print("Ran checks on initial data.")
    #np.save(os.path.join(dir, "initialized_drdata.npy"), drdata)
    #print("Saved initial data.")

    width = 1.0
    #R = sys.argv[1]
    #R = float(R)

    zip2where = lambda t: (np.array(next(t)), np.array(next(t)))

    for R in range(*dr_range):
        R = float(R)
        print("dR: {}".format(R))
        R_pixel_positions = load_R_pixel_positions(pixel_positions, R, width)
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

    #np.save(os.path.join(dir, "drdata.npy"), drdata)

if __name__ == "__main__":
    main()

