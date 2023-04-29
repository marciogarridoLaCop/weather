// Armazenamento e Negtaivo Acumulado
// Balanço hídrico climatológico Thornthwaite e Mather (1955)
// Caso 1 - P - ETP anual > 0 e Caso 2.1 - P - ETP anual < 0, mas P-ETP no período chuvo > CAD
// Autor : Gusatvo Lyra
//  Versão : V 0.1
//  10/01/2022

funcprot(0);

function [ARM,NegAcu] = ARM_Case1(PETP);

for i = 1:nrows;
    if i == 1 & PETP(i) < 0 & PETP(12) > 0           // Janeiro mês de início do Período seco
        NegAcua(1) = PETP(i);                        // Negativo Acumulado - NegAcu[mm]  mês de início
        ARMa(1) = CAD*exp(NegAcua(1)/CAD);           // Armazenamento de água no solo - ARM [mm]
        j = 1;
    else
        if i > 1 & PETP(i) < 0 & PETP(i-1) > 0       // Mês início do período seco <> janeiro
           NegAcua(1) = PETP(i); 
           ARMa(1) = CAD*exp(NegAcua(1)/CAD);
           j = i;
       else
           if PETP(i) == max(PETP)
           NegAcua(1) = 0
           ARMa(1) = 100
           j = i
           end
       end
    end
end

//Ordenar vetor P-EPT i = 1 mês de início (auxililar)
for i = 1:nrows
    if i < j
        PETPa(12-j+i+1) = PETP(i)
    else
       if i >= j then
        PETPa(i-j+1)= PETP(i)
        end
    end
end

// NegAcu e ARM para os demais meses
for i = 2:nrows
    if PETPa(i) < 0                                             // Mês seco <> mês de início e de janeiro
          NegAcua(i) = NegAcua(i-1)+ PETPa(i);   
          ARMa(i) = CAD*exp(NegAcua(i)/CAD);   
    else
        if PETPa(i) > 0 & PETPa(i-1) < 0 ;          // Mês chuvoso
           if PETPa(i) + NegAcua(i-1)< CAD          // ARM < CAD
              ARMa(i) = ARMa(i-1)+PETPa(i);         // ARM [mm]
              NegAcua(i) = CAD*log(ARMa(i)/CAD);    // NegAcum [mm]
           else  // ARM = CAD
              NegAcua(i) = 0; 
              ARMa(i) = 100;                      
            end
         else
            NegAcua(i) = 0; 
            ARMa(i) = 100;                      
        end
    end 
end

//Ordenar cronologicamente o vetor ARM e NegAcu
for i = 1:nrows
    if i <= (13-j)
            ARM(j+i-1) = round(ARMa(i));
            NegAcu(j+1-1) = round(NegAcua(i));
    else
        if i > (13-j)
        ARM(i+j-13) = round(ARMa(i));
        NegAcu(i+j-13) = round(NegAcua(i)); 
        end
    end
end

endfunction
