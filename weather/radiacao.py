import math

def SaldoRadiacao(Doy,fi,Z,Rs,Tx,Tn,ea): 

    # Correção distância relativa Terra-Sol
    dr = 1 + 0.033 * math.cos(2*math.pi*Doy/365)         
    
    # Declinação solar
               
    decl = 0.409 * math.sin((2*math.pi*Doy/365)-1.39)

    # Ângulo horário entre o nasceer-pôr do Sol
    
    ws = math.acos(-math.tan(fi*math.pi/180)*math.tan(decl)) # Ângulo horário entre o nasceer-pôr do Sol
 
    Np = (24/math.pi)*ws
    
    Hn = 12 - Np/2     # Hora do Nascer do Sol
    Hp = 12 + Np/2     # Hora do Nascer do Pôr
    
   
    Ra = 37.568*dr*((ws*math.sin(fi*math.pi/180)*math.sin(decl))+(math.cos(fi*math.pi/180)*math.cos(decl)*math.sin(ws)))
    # Balanço de radiação
  
    Rso = (0.75 +2E-5*Z)*Ra        
   
    Rns =float(str(0.77 * Rs)[1:-1])   

    # Ondas longas
    Rnl =float(str(4.903E-9*((((Tx + 273.16)**4)+((Tn + 273.16)**4))/2)*(0.34-0.14*ea**0.5)*(1.35*(Rs/Rso)-0.35))[1:-1])   
  
    Rn = Rns - Rnl

    return [Rn,Rns,Rnl,Ra]
            