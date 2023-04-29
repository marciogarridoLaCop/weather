import numpy as np

def arm_case2(PETP, nrows, PETPMTotal, PETPNTotal, CAD=100):
    NegAcua = np.zeros(nrows)
    ARMa = np.zeros(nrows)
    j = None

    for i in range(nrows):
        if i == 0 and PETP[i] < 0 and PETP[11] > 0:
            NegAcua[0] = CAD * np.log((PETPMTotal / CAD) / (1 - np.exp(-PETPNTotal / CAD)))
            ARMa[0] = CAD * np.exp(NegAcua[0] / CAD)
            j = 11
        else:
            if i > 0 and PETP[i] < 0 and PETP[i - 1] > 0:
                NegAcua[0] = CAD * np.log((PETPMTotal / CAD) / (1 - np.exp(-PETPNTotal / CAD)))
                ARMa[0] = CAD * np.exp(NegAcua[0] / CAD)
                j = i - 1
            else:
                if PETP[i] == max(PETP):
                    NegAcua[0] = CAD * np.log((PETPMTotal / CAD) / (1 - np.exp(-PETPNTotal / CAD)))
                    ARMa[0] = CAD * np.exp(NegAcua[0] / CAD)
                    j = i

    PETPa = np.zeros(nrows)
    for i in range(nrows):
        if i < j:
            PETPa[11 - j + i + 1] = PETP[i]
        else:
            PETPa[i - j + 1] = PETP[i]

    for i in range(1, nrows):
        if PETPa[i] < 0:
            NegAcua[i] = NegAcua[i - 1] + PETPa[i]
            ARMa[i] = CAD * np.exp(NegAcua[i] / CAD)
        else:
            if PETPa[i] > 0:
                ARMa[i] = ARMa[i - 1] + PETPa[i]
                NegAcua[i] = CAD * np.log(ARMa[i] / CAD)

    ARM = np.zeros(nrows)
    NegAcu = np.zeros(nrows)
    for i in range(nrows):
        if i <= (12 - j):
            ARM[j + i - 1] = round(ARMa[i])
            NegAcu[j + i - 1] = round(NegAcua[i])
        else:
            ARM[i + j - 12] = round(ARMa[i])
            NegAcu[i + j - 12] = round(NegAcua[i])

    return ARM, NegAcu
