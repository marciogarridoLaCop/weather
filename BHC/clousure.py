def closure(PETotal, PETPTotal, PCPTotal, ETR, EXC, DEF):
    Lag = np.zeros((4, 1))

    if round(PCPTotal) == round(PETotal + PETPTotal):
        Lag[0, 0] = 1
    else:
        Lag[0, 0] = 0

    if round(PCPTotal) == round(np.sum(ETR) + np.sum(EXC)):
        Lag[1, 0] = 1
    else:
        Lag[1, 0] = 0

    if round(PETotal) == round(np.sum(ETR) + np.sum(DEF)):
        Lag[2, 0] = 1
    else:
        Lag[2, 0] = 0

    # Substitua ALT pela variável correta no Python, se necessário
    # ALT não foi definido na função original em Scilab
    if np.sum(ALT) == 0:
        Lag[3, 0] = 1
    else:
        Lag[3, 0] = 0

    return Lag
