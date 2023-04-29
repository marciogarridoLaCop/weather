// Relações psicrométricas e termodinâmicas
// Gusatvo Lyra 01162021

funcprot(0);

function [Patm,Tm,URm,es,ea,DPV,UA,US,Qesp,Rmix,Tpo,Dens,Lamb,Gama,Ses] = Termodinamica(Tx,Tn,URx,URn,Z)
    Patm = 101.3*((293-0.0065*Z)/293)^5.26; // Pressão atmosférica [kPa]
    
    Tm = (Tx+Tn)/2;                         // Temperatura do ar média [oC]
    
    URm = (URx+URn)/2;                      // Umidade do ar média [%]
    
    es = ((0.6108*exp(17.27*Tn/(237.3+Tn)))+(0.6108*exp(17.27*Tx/(237.3+Tx))))/2;          // Pressão de saturação do vapor d'água do ar [kPa]
    
    ea = (0.6108*exp(17.27*Tn/(237.3+Tn))*URx+0.6108*exp(17.27*Tx/(237.3+Tx))*URn)/200;  // Pressão de real do vapor d'água do ar [kPa]
    
    DPV = (es -ea);                         // Déficit de pressão de saturação [kPa]
    
    Ses = 4098*(0.6108*exp(17.27*Tm/(Tm+237.3)))/(Tm+237.3)^2;           // Derivada da curvas de pressão de saturação [kPa]
    
    UA = 2168*(ea/(Tm+273.15));             // Umidade absoluta [g/m³]
    
    US = 2168*(es/(Tm+273.15));             // Umidade Absoluta de saturação [g/m³]
    
    Qesp = 0.622*ea/(Patm-0.378*ea);        // Umidade específica [g/g]
    
    Rmix = 0.622*ea/(Patm-ea);              // Razão de mistura [g/g]
    
    Tpo = (237.3*log10(ea/0.6108))/(7.5-log10(ea/0.6108));  // Temperatura do ponto de orvalho [oC]
    
    Lamb = 2.501-(0.002361)*Tm                             // Calor latente de evaporação [MJ/kg]
    
    Gama = (1.013E-3*Patm)/(0.622*Lamb);   // Coeficiente pscrométrico [oC/MJ]
    
    Dens = 3.484*(Patm/Tm);                // Densidade do ar [g/m³]
endfunction
