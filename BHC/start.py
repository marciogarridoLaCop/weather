def start(dados, nrows):
    PCP = np.zeros(nrows)
    PET = np.zeros(nrows)
    PETP = np.zeros(nrows)
    PETPM = np.zeros(nrows)
    PETPN = np.zeros(nrows)

    for i in range(nrows):
        PCP[i] = round(dados[i, 0])  # Precipitação mensal - P [mm]
        PET[i] = round(dados[i, 1])  # Evapotranspiração potencial - ETP
        PETP[i] = PCP[i] - PET[i]  # P - ETP mensal [mm]

        if PETP[i] > 0:
            PETPM[i] = PETP[i]
            PETPN[i] = 0
        else:
            PETPM[i] = 0
            PETPN[i] = PETP[i]

    # Balanço anual Precipitação e evapotranspiração potencial
    PCPTotal = np.sum(PCP)
    PETotal = np.sum(PET)
    PETPTotal = np.sum(PETP)
    PETPMTotal = np.sum(np.abs(PETPM))
    PETPNTotal = np.sum(np.abs(PETPN))

    if PETPMTotal == 0:
        PETPMTotal = 0.001

    return PCP, PET, PETP, PETPM, PETPN, PCPTotal, PETotal, PETPTotal, PETPMTotal, PETPNTotal
