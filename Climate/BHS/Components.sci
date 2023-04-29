// Componentes do balanço hídrico climatológico Thornthwaite e Mather (1955)
// Autor : Gusatvo Lyra
//  Versão : V 0.1
//  10/01/2022

funcprot(0);

function [ALT,ETR,DEF,EXC,RET,REP] = Components(CAD,ARM,PET,PCP,PETP);
for i = 2:nrows;
    ALT(i) = ARM(i)-ARM(i-1);                // Alteração do ARM - ALT [mm]
    
    
    if PETP(i) >=0                          // Mês chuvoso
       ETR(i) = PET(i);                     // Evapotranspiração real [mm]
    else
                                            // Mês seco
       ETR(i)= PCP(i)-ALT(i);    
       
    end
    
    if ARM(i) < CAD;
       EXC(i) = 0;    
    else
       EXC(i) = PETP(i)-ALT(i);             // Excedente hidríco - EXC [mm]   
    end
    
    DEF(i) = PET(i)-ETR(i);                  // Deficiência hídrica - DEF [mm]
    
    if PETP(i)< 0 & ALT(i) <= 0
       RET(i)= round(ALT(i));               // Reposição [mm] p/ gráfico
       REP(i) = 0;
    else 
        if PETP(i)> 0 & ALT(i) > 0 // Retirada [mm] p/gráfico
           REP(i) = round(ALT(i));
           RET(i) = 0;
        else
            REP(i) = 0;        
            RET(i) = 0;
        end
    end    
end

endfunction
