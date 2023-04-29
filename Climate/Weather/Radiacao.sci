// Radiação solar e terrestre e relações astronômicas Terra-Sol
// Gustavo Lyra 01192021

funcprot(0);

    
function [Rn,Rns,Rnl,Ra] = SaldoRadiacao(Doy,fi,Z,Rs,Tx,Tn,ea);
    dr = 1 + 0.033 * cos(2*%pi*Doy/365); // Correção distância relativa Terra-Sol

    decl = 0.409 * sin((2*%pi*Doy/365)-1.39); // Declinação solar
 
    ws = acos(-tan(fi*%pi/180)*tan(decl)); // Ângulo horário entre o nasceer-pôr do Sol
    
    Np = (24/%pi)*ws;
    
    Hn = 12 - Np/2; // Hora do Nascer do Sol
    Hp = 12 + Np/2; // Hora do Nascer do Pôr
    
    Ra = 37.568*dr*((ws*sin(fi*%pi/180)*sin(decl))+(cos(fi*%pi/180)*cos(decl)*sin(ws)));
 
    // Balanço de radiação
    // Ondas curtas
    Rso = (0.75 + 2E-5*Z)*Ra;
    Rns = 0.77 * Rs;

    // Ondas longas
    Rnl = 4.903E-9*((((Tx + 273.16)^4)+((Tn + 273.16)^4))/2)*(0.34-0.14*ea^0.5)*(1.35*(Rs/Rso)-0.35);
    Rn = Rns - Rnl;
    
endfunction
