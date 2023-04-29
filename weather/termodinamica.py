import math

def Termodinamica(Tx,Tn,URx,URn,Z): # Temperatura

    Patm = 101.3*((293-0.0065*Z)/293) ** 5.26 # Pressão atmosférica [kPa]

    Tm = float(str((Tx+Tn)/2)[1:-1])                          # Temperatura do ar média [oC]

    URm = float(str((URx+URn)/2)[1:-1])                      # Umidade do ar média [%]

    es = float(str(((0.6108*math.exp(17.27*Tn/(237.3+Tn)))+(0.6108*math.exp(17.27*Tx/(237.3+Tx))))/2)[1:-1])  # Pressão de saturação do vapor d'água do ar [kPa]

    ea = float(str((0.6108*math.exp(17.27*Tn/(237.3+Tn))*URx+0.6108*math.exp(17.27*Tx/(237.3+Tx))*URn)/200)[1:-1])      # Pressão de real do vapor d'água do ar [kPa]

    DPV = (es -ea)                         # Déficit de pressão de saturação [kPa]

    Ses = 4098*(0.6108*math.exp(17.27*Tm/(Tm+237.3)))/(Tm+237.3) ** 2           # Derivada da curvas de pressão de saturação [kPa]

    UA = 2168*(ea/(Tm+273.15))             # Umidade absoluta [g/m³]

    US = 2168*(es/(Tm+273.15))             # Umidade Absoluta de saturação [g/m³]

    Qesp = 0.622*ea/(Patm-0.378*ea)        # Umidade específica [g/g]

    Rmix = 0.622*ea/(Patm-ea)              # Razão de mistura [g/g]

    Tpo = (237.3*math.log10(ea/0.6108))/(7.5-math.log10(ea/0.6108))  # Temperatura do ponto de orvalho [oC]

    Lamb = 2.501-(0.002361)*Tm                             # Calor latente de evaporação [MJ/kg]

    Gama = (1.013E-3*Patm)/(0.622*Lamb)   # Coeficiente pscrométrico [oC/MJ]

    Dens = 3.484*(Patm/Tm)                # Densidade do ar [g/m³]

    return [Patm,Tm,URm,es,ea,DPV,UA,US,Qesp,Rmix,Tpo,Dens,Lamb,Gama,Ses]
            