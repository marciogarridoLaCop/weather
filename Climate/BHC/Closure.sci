// Aferição do balanço hídrico climatológico Thornthwaite e Mather (1955)
// Autor : Gusatvo Lyra
//  Versão : V 0.1
//  10/01/2022

funcprot(0);

function [Lag] = Closure(PETotal,PETPTotal,PCPTotal,ETR,EXC,DEF);

if  round(PCPTotal) == round(PETotal + PETPTotal)
    Lag(1,1) = 1  
else
    Lag(1,1) = 0
end

if  round(PCPTotal) == round(sum(ETR(:)) + sum(EXC(:)))
    Lag(2,1) = 1  
else
    Lag(2,1) = 0
end

if  round(PETotal) == round(sum(ETR(:)) + sum(DEF(:)))
    Lag(3,1) = 1  
else
    Lag(3,1) = 0
end

if  sum(ALT(:)) == 0
    Lag(4,1) = 1  
else
    Lag(4,1) = 0
end

endfunction
