import math

def Evapo(Ra,Rn,Tm,Tx,Tn,es,ea,Lamb,Gama,Ses,U2): 

    #Método de Hargreaves-Samani
    ETo_HS = float(str(0.0023*(1/Lamb)*Ra*(Tm+17.8)*(Tx - Tn)**0.5)[1:-1])      

    # Método de Penman-Monteith
    G = 0
    ETo_PM = float(str(((1/Lamb)*Ses*(Rn-G)+(Gama*900*U2*(es-ea)/(Tm + 273)))/(Ses+Gama*(1+0.34*U2)))[1:-1])      

    return [ETo_HS, ETo_PM]