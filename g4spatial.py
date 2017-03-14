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


def main():
    data = np.load("drdata.npy")
    result = np.zeros((20, 10), dtype=np.float)
    for dt in range(20):
        print(dt)
        for dr in range(10):
            result[dt, dr] = g4(dt, dr, data)
    #result = g4(5, 2, data)
    print(result)
    np.savetxt("temp_result.txt", result)

if __name__ == "__main__":
    main()

