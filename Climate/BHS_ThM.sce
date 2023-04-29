/*
  Balanço de Hídrico Climático - BHC 
  Thornthwaite and Mather 1955
  Autor : Gusatvo Lyra
  Versão : V 0.1
  11/10/2022
*/

clear;
clc;

caminho =('C:\Users\UFRRJ_1\Dropbox\CropModels\Climate\');  //  Pasta com script BHS_ThM.sce
Planilha = readxls(caminho+'Data\ClimaUSC.xls')             // Carregar séries climáticas da subpasta Data

typeof(Planilha)

Aba = Planilha(1)

Dados = Aba.value

nrows = size (Dados,"r")

CAD = 100       // Capacidade de água disponível - CAD [mm]


// Inicialização
    exec(caminho+'BHS\Start.sci');
    [PCP, PET, PETP] = Start(Dados, nrows);
        
// Determinação do Armazenamento - ARM [mm] e do Negativo Acumulado - NegAcu [mm]
   exec(caminho+'BHS\ARM_fnc.sci');
    [ARM,NegAcu] = ARM_fnc(PETP,CAD);

// Determinação dos componentes Alteração - ALT, Evapotranspiração Real - ETR, Excedente - EXC e Deficiência Hídrica - DEF [mm]
   exec(caminho+'BHS\Components.sci');
   [ALT,ETR,DEF,EXC,RET,REP] = Components(CAD,ARM,PET,PCP,PETP);

// Auxiliar gráfico

k = 1
j = 1
for i = 1:nrows-1
    if j < 12
        m(k,j) = ARM(i);
        if  EXC(i) > 0 then
            n(k,j) = EXC(i)
        else     
            if DEF(i) > 0 
                n(k,j)= -DEF(i)
            else
                n(k,j)= 0
            end
        end
        j = j +1
    else
        if j == 12 
            m(k,j) = ARM(i);
            if  EXC(i) > 0 then
                n(k,j) = EXC(i)
                else     
                    if DEF(i) > 0 
                        n(k,j)= -DEF(i)
                    else
                        n(k,j)= 0
                    end
            k = k + 1
            j = 1
            end
     end
    end
end

// Gráficos
clf()

scf(0);
subplot(4,1,1)
bar(PCP(2:121),'blue1');
plot(PET(2:121),'cyan');
plot(ETR(2:121),'red');
legend(['Chuva';'ETP';'ETR'])
a=get("current_axes")
a.data_bounds=[1,0;120,1.1*max(PCP)]

subplot(4,1,2)
bar(PCP(122:241),'blue1');
plot(PET(122:241),'cyan');
plot(ETR(122:241),'red');
a=get("current_axes")
a.data_bounds=[1,0;120,1.1*max(PCP)]

subplot(4,1,3)
bar(PCP(242:361),'blue1');
plot(PET(242:361),'cyan');
plot(ETR(242:361),'red');

a=get("current_axes")
a.data_bounds=[1,0;120,1.1*max(PCP)]

xtitle("","","Chuva, ETP ou ETR(mm)")

subplot(4,1,4)
bar(PCP(362:nrows),'blue1');
plot(PET(362:nrows),'cyan');
plot(ETR(362:nrows),'red');

a=get("current_axes")
a.data_bounds=[1,0;120,1.1*max(PCP)]
xtitle("","Mês","")

scf(1);
subplot(4,1,1);
bar(-DEF(2:121),'red');
bar(EXC(2:121),'blue');
legend(['DEF';'EXC']);
a=get("current_axes");
a.data_bounds=[1,-1.1*max(DEF);120,1.1*max(EXC)];

subplot(4,1,2);
bar(-DEF(122:241),'red');
bar(EXC(122:241),'blue');
a=get("current_axes");
a.data_bounds=[1,-1.1*max(DEF);120,1.1*max(EXC)];

subplot(4,1,3);
bar(-DEF(242:361),'red');
bar(EXC(242:361),'blue');

a=get("current_axes");
a.data_bounds=[1,-1.1*max(DEF);120,1.1*max(EXC)];

xtitle("","","DEF ou EXC(mm)");

subplot(4,1,4);
bar(-DEF(362:nrows),'red');
bar(EXC(362:nrows),'blue');

a=get("current_axes");
a=get("current_axes");
a.data_bounds=[1,-1.1*max(DEF);120,1.1*max(EXC)];

xtitle("","Mês","");

scf(2);
subplot(2,1,1)
gcf().color_map =  hotcolormap(64);
colorbar(0,100)
title("ARM [mm]")
grayplot([1987:2021],[1:12],m, strf="011",rect=[1987,1,2021,12])
xtitle("","Ano","Mês")

subplot(2,1,2)
gcf().color_map =  hotcolormap(64);
colorbar(min(n),max(n))
title("DEF e EXC [mm]")
grayplot([1987:2021],[1:12],n, strf="011",rect=[1987,1,2021,12])
xtitle("","Ano","Mês")

