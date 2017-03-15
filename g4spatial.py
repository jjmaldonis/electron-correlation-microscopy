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
    data0 = np.load("results/C234/dtdata.npy")
    result = np.zeros((20, 10), dtype=np.float)
    for dr in range(10):
        data_dr = np.load("results/C234/drdata_{}.npy".format(dr))
        for dt in range(20):
            result[dt, dr] = g4_from_slices(dt, dr, data0, data_dr)
            print(dr, dt, result[dt, dr])
    print(result)
    np.savetxt("temp_result.txt", result)

    """
    data = np.load("drdata.npy")
    result = np.zeros((20, 10), dtype=np.float)
    for dt in range(20):
        print(dt)
        for dr in range(10):
            result[dt, dr] = g4(dt, dr, data)
    #result = g4(5, 2, data)
    print(result)
    np.savetxt("temp_result.txt", result)
    """

if __name__ == "__main__":
    main()

