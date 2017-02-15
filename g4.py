import os, sys
import numpy as np
from utilities import load_pixel_positions
from utilities import load_tif_data


def g2(data, dt):
    top = []
    bottom1 = []
    bottom2 = []
    for i in range(len(data)-dt):
        top.append(data[i]*data[i+dt])
        bottom1.append(data[i])
        bottom2.append(data[i+dt])
    top = (len(data) - dt) * np.sum(top)
    bottom = np.sum(bottom1) * np.sum(bottom2)
    return top/bottom


@np.vectorize
def fit_g2(t, A, tau, beta):
    return 1.0 + A * np.exp(-2*(t/tau)**beta)


def fast_g4(data, dts_range, dtl_range):
    #assert dts_range[1] <= dtl_range[0]
    #size = len(data) - dtl #max(dts, dtl)  # With the assert statement at the top of this func, we can set the size just from dtl
    results_g4 = np.zeros((dtl_range[1]-dtl_range[0], dts_range[1]-dts_range[0]), dtype=np.float)
    for dtl in range(*dtl_range):
        for dts in range(*dts_range):
            size = len(data) - (dts+dtl)
            bottom1 = np.sum(data[:size])
            bottom2 = np.sum(data[dtl:dtl+size])
            bottom3 = np.sum(data[dts:dts+size])
            bottom4 = np.sum(data[dts+dtl:dts+dtl+size])
            bottom = bottom1 * bottom2 * bottom3 * bottom4
            top = size**3*np.sum(
                    np.multiply(
                    np.multiply(
                    np.multiply(
                        data[:size],
                        data[dts:dts+size]),
                        data[dtl:dtl+size]),
                        data[dts+dtl:dts+dtl+size])
                  )
            results_g4[dtl-dtl_range[0], dts-dts_range[0]] = top/bottom
    return results_g4


#def calculate(arg):
def calculate(strip, i, j):
    #strip, i, j = arg
    dts_range = (1, 500)
    dtl_range = (100, 3000)
    results = fast_g4(strip, dts_range, dtl_range)
    fn = "C250_0.1s_{i}_{j}.g4time.txt".format(i=i, j=j)
    np.savetxt(fn, results)
    print(fn)
    return None


def main():
    NPROCS = 1
    data = load_tif_data(nprocs=NPROCS)

    i, j = sys.argv[1], sys.argv[2]
    i = int(i)
    j = int(j)
    calculate(data[i,j,:], i, j)

    #gen = ( (data[i,j,:], i, j) for i,j in pixel_positions )
    #pool = Pool(processes=NPROCS)
    #pool.map(calculate, gen)
    #pool.close()
    #pool.join()
    #print("Finished!")


if __name__ == "__main__":
    main()

