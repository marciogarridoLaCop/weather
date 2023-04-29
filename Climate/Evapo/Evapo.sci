// Evapotranpiração de referência
// Gustavo Lyra 08102022

funcprot(0);
    
function [ETo_HS, ETo_PM] = Evapo(Ra,Rn,Tm,Tx,Tn,es,ea,Lamb,Gama,Ses,U2);

// Método de Hargreaves-Samani

ETo_HS = 0.0023*(1/Lamb)*Ra*(Tm+17.8)*(Tx - Tn)^0.5

// Método de Penman-Monteith
G = 0
ETo_PM = ((1/Lamb)*Ses*(Rn-G)+(Gama*900*U2*(es-ea)/(Tm + 273)))/(Ses+Gama*(1+0.34*U2));

endfunction
