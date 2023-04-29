import numpy as np

def ARM_fnc(PETP, CAD, nrows):
    ARM = np.zeros(nrows)
    NegAcu = np.zeros(nrows)

    # NegAcu e ARM inicial
    ARM[0] = 100
    NegAcu[0] = 0

    # NegAcu e ARM para os demais meses
    for i in range(1, nrows):
        if PETP[i] < 0:
            NegAcu[i] = NegAcu[i - 1] + PETP[i]
            ARM[i] = CAD * np.exp(NegAcu[i] / CAD)
            if ARM[i] > CAD:
                ARM[i] = CAD
                NegAcu[i] = 0
        else:
            if PETP[i] >= 0:
                ARM[i] = ARM[i - 1] + PETP[i]
                NegAcu[i] = CAD * np.log(ARM[i] / CAD)
                if ARM[i] > CAD:
                    ARM[i] = CAD
                    NegAcu[i] = 0

    return ARM, NegAcu
