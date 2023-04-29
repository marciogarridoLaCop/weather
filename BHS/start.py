import numpy as np

def Start(Dados, nrows):
    PCP = np.zeros(nrows)
    PET = np.zeros(nrows)
    PETP = np.zeros(nrows)

    for i in range(1, nrows):
        PCP[i] = round(Dados[i, 2])
        PET[i] = round(Dados[i, 3])
        PETP[i] = PCP[i] - PET[i]

    return PCP, PET, PETP
