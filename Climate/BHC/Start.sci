// Inicialização do BHC
// Carregar dados de Evapotranspiração e Precipitação e balanço P - ETP (mensal, anual e estação seca - N e Chuvosa - M)
// Autor : Gusatvo Lyra
//  Versão : V 0.1
//  10/01/2022

funcprot(0);

function [PCP, PET, PETP,PETPM,PETPN,PCPTotal,PETotal,PETPTotal,PETPMTotal,PETPNTotal] = Start(Dados, nrows);

for i = 1:nrows;                // i = 1 - janeiro -> 12 - dezembro
    PCP(i) = round(Dados(i,1));        // Precipitação mensal - P [mm]N
    PET(i) = round(Dados(i,2));        // Evapotranspiração potencial - ETP 
    PETP(i) = PCP(i)-PET(i);    // P - ETP mensal [mm]
    if PETP(i) > 0
        PETPM(i) = PETP(i);
        PETPN(i) = 0;
    else
        PETPM(i) = 0;
        PETPN(i) = PETP(i);
    end
end

// Balanço anual Precipitação e evapotranspiração potencial
PCPTotal = sum (PCP(:));            // Precipitação total anual - P [mm]
PETotal = sum (PET(:));             // Evapotranspiração total anual - ETP [mm]
PETPTotal = sum (PETP(:));          // P - ETP anual [mm]
PETPMTotal = sum(abs(PETPM(:)));    // P - ETP período chuvoso [mm]
PETPNTotal = sum(abs(PETPN(:)));    // P - ETP período seco [mm]

if PETPMTotal == 0 then
    PETPMTotal = 0.001
end

endfunction
