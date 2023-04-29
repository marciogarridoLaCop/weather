// Inicialização do BHC
// Carregar dados de Evapotranspiração e Precipitação e balanço P - ETP (mensal, anual e estação seca - N e Chuvosa - M)
// Autor : Gusatvo Lyra
//  Versão : V 0.1
//  10/01/2022

funcprot(0);

function [PCP, PET, PETP] = Start(Dados, nrows);

for i = 2:nrows;                
    PCP(i) = round(Dados(i,3));        // Precipitação mensal - P [mm]
    PET(i) = round(Dados(i,4));        // Evapotranspiração potencial - ETP 
    PETP(i) = PCP(i)-PET(i);           // P - ETP mensal [mm]
end

endfunction
