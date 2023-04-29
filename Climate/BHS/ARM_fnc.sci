// Armazenamento e Negtaivo Acumulado
// Balanço hídrico climatológico Thornthwaite e Mather (1955)
// Caso 1 - P - ETP anual > 0 e Caso 2.1 - P - ETP anual < 0, mas P-ETP no período chuvo > CAD
// Autor : Gusatvo Lyra
//  Versão : V 0.1
//  10/01/2022

funcprot(0);

function [ARM,NegAcu] = ARM_fnc(PETP,CAD);

// NegAcu e ARM inicial
ARM(1) = 100
NegAcu(1) = 0

// NegAcu e ARM para os demais mese

for i = 2:nrows
    if PETP(i) < 0                            // Mês seco
        NegAcu(i) = NegAcu(i-1)+ PETP(i);     // Negativo acumulado - NegAcum [mm]
        ARM(i) = CAD*exp(NegAcu(i)/CAD);      // Armaenmaneto - ARM [mm]
            if ARM(i) > CAD 
               ARM(i) = CAD
               NegAcu(i) = 0
            end                    
    else        
        if PETP(i) >= 0;                       // Mês chuvoso
           ARM(i) = ARM(i-1)+PETP(i);          // ARM [mm]
           NegAcu(i) = CAD*log(ARM(i)/CAD);    // NegAcum [mm]
           if ARM(i) > CAD 
               ARM(i) = CAD
               NegAcu(i) = 0
           end                    
        end
    end
end 

endfunction
