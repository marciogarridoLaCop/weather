import numpy as np

def Components(CAD, ARM, PET, PCP, PETP, nrows):
    ALT = np.zeros(nrows)
    ETR = np.zeros(nrows)
    DEF = np.zeros(nrows)
    EXC = np.zeros(nrows)
    RET = np.zeros(nrows)
    REP = np.zeros(nrows)

    for i in range(1, nrows):
        ALT[i] = ARM[i] - ARM[i - 1]

        if PETP[i] >= 0:
            ETR[i] = PET[i]
        else:
            ETR[i] = PCP[i] - ALT[i]

        if ARM[i] < CAD:
            EXC[i] = 0
        else:
            EXC[i] = PETP[i] - ALT[i]

        DEF[i] = PET[i] - ETR[i]

        if PETP[i] < 0 and ALT[i] <= 0:
            RET[i] = round(ALT[i])
            REP[i] = 0
        else:
            if PETP[i] > 0 and ALT[i] > 0:
                REP[i] = round(ALT[i])
                RET[i] = 0
            else:
                REP[i] = 0
                RET[i] = 0

    return ALT, ETR, DEF, EXC, RET, REP
