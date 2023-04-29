/*
  Balanço de Hídrico Climático - BHC 
  Thornthwaite and Mather 1955
  Autor : Gusatvo Lyra
  Versão : V 0.1
  21/06/2022
*/

clear;
clc;

caminho =('C:\Users\UFRRJ_1\Dropbox\CropModels\Climate\');  //  Pasta com script BHC_ThM.sce
Dados = fscanfMat(caminho+'Data\BHClimateP7.txt');          // Carregar dados climáticos da subpasta Data
nrows = size (Dados,"r");    
CAD = 100       // Capacidade de água disponível - CAD [mm]

// Inicialização
    exec(caminho+'BHC\Start.sci');
    [PCP, PET, PETP,PETPM,PETPN,PCPTotal,PETotal,PETPTotal,PETPMTotal,PETPNTotal] = Start(Dados, nrows);
        
// Determinação do Armazenamento - ARM [mm] e do Negativo Acumulado - NegAcu [mm]
if PETPTotal >= 0 | (PETPTotal < 0 & PETPMTotal >= CAD) // Caso 1 e Caso 2.1
    exec(caminho+'BHC\Case1.sci');
    [ARM,NegAcu] = ARM_Case1(PETP);
   else                                                    // Caso 2.2
    exec(caminho+'BHC\Case2.sci');
    [ARM, NegAcu] = ARM_Case2(PETP, PETPMTotal, PETPNTotal);
end

// Determinação dos componentes Alteração - ALT, Evapotranspiração Real - ETR, Excedente - EXC e Deficiência Hídrica - DEF [mm]
   exec(caminho+'BHC\Components.sci');
   [ALT,ETR,DEF,EXC,RET,REP] = Components(CAD,ARM,PET,PCP,PETP);

// Aferiação do BHC 
   exec(caminho+'BHC\Closure.sci');
   [Lag] = Closure(PETotal,PETPTotal,PCPTotal,ETR,EXC,DEF);

// Tabela Resumo BHC
BHC(:,1)=PCP;
BHC(:,2)=PET;
BHC(:,3)=PETP;
BHC(:,4)=ARM;
BHC(:,5)=ALT;
BHC(:,6)=ETR;
BHC(:,7)=DEF;
BHC(:,8)=EXC;

// Exportar BHC *.csv
csvWrite(BHC, caminho+'Data\BHC_output.csv')

// Gráficos
clf()

scf(0);
subplot(2,2,1)
bar(-DEF,1,'red')
bar(EXC,1,'blue')

xtitle("","Mês","EXC ou DEF (mm)")
legend(['DEF';'EXC'])

subplot(2,2,2)
bar(PCP,'blue1');
plot(PET,'cyan');
plot(ETR,'red');

xtitle("","Mês","Chuva, ETP ou ETR(mm)")
legend(['Chuva';'ETP';'ETR'])

subplot(2,2,3)
bar(1:12,[EXC,RET,-DEF,REP],'stacked')
xtitle("","Mês","DEF, EXC, REP ou RET(mm)")
legend(['EXC';'RET';'DEF';'REP'])
