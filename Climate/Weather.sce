// Gustavo Bastos Lyra 
// V0.1 16/01/2021

clear;
clc;
caminho =('C:\Users\UFRRJ_1\Dropbox\CropModels\Climate\');
Dados = fscanfMat(caminho+'Data\DadosEvapo.txt');
nrows = size (Dados,"r");    
Z = 54;    // Altitude (m)
fi = -22.45;   // Latitude (decimos de graus)

for i = 1:nrows;
    Data(i) = Dados (i,1);      // Data em valor numérico
    Doy(i)  = Dados (i,2);      // Dia de ordem do ano/dia Juliano 
    Tx(i)  = Dados (i,3);       // Temperatura do ar máxima absoluta [oC]
    Tn(i)  = Dados (i,4);       // Temperatura do ar mínima absoluta [oC]
    Rs(i)  = Dados (i,5);       // Radiação solar global [MJ / m² d]
    U2(i)  = Dados (i,6);       // Velocidade do vento - 2m [m/s]
    URx(i)  = Dados (i,7);      // Umidade relativa do ar máxima absoluta [%]
    URn(i)  = Dados (i,8);      // Umidade relativa do ar mínima absoluta [%]
    PCP(i)  = Dados (i,9);      // Precipitação total [mm]

// Função termodinâmica do ar
exec(caminho+'Weather\Termodinamica.sci');
[Patm(i),Tm(i),URm(i),es(i),ea(i),DPV(i),UA(i),US(i),Qesp(i),Rmix(i),Tpo(i),Dens(i),Lamb(i),Gama(i),Ses(i)] = Termodinamica(Tx(i),Tn(i),URx(i),URn(i),Z);

// Função radiação solar e terrestre
exec(caminho+'Weather\Radiacao.sci');
[Rn(i),Rns(i),Rnl(i),Ra(i)] = SaldoRadiacao(Doy(i),fi,Z,Rs(i),Tx(i),Tn(i),ea(i));

// Função evapotranspiração de referência (ETo)
exec(caminho+'Evapo\Evapo.sci');
[ETo_HS(i), ETo_PM(i)] = Evapo(Ra(i),Rn(i),Tm(i),Tx(i),Tn(i),es(i),ea(i),Lamb(i),Gama(i),Ses(i),U2(i))

end

// Tabela Radiação e ETo
Radiation(:,1)=Ra;
Radiation(:,2)=Rs;
Radiation(:,3)=Rns;
Radiation(:,4)=Rnl;
Radiation(:,5)=Rn;
Radiation(:,6)=ETo_HS;
Radiation(:,7)=ETo_PM;

// Tabela Termodinâmico 
Termodynamic(:,1)=Tm;
Termodynamic(:,2)=URm;
Termodynamic(:,3)=es;
Termodynamic(:,4)=ea;
Termodynamic(:,5)=DPV;
Termodynamic(:,6)=UA;
Termodynamic(:,7)=US;
Termodynamic(:,8)=Qesp;
Termodynamic(:,9)=Rmix;
Termodynamic(:,10)=Tpo;
Termodynamic(:,11)=Dens;
Termodynamic(:,12)=Lamb;
Termodynamic(:,13)=Gama;
Termodynamic(:,14)=Ses;

// Exportar arquivo radiação e temodinâmico *.csv
csvWrite(Radiation, caminho+'Data\Radiation_output.csv')
csvWrite(Termodynamic, caminho+'Data\Termodynamic_output.csv')

// Gráficos
clf()

scf(0);

subplot(5,1,1)
plot(Doy,Tn,'cyan');
plot(Doy,Tm,'blue'); 
plot(Doy,Tx,'red');

lines(0)
a=get("current_axes")
a.data_bounds=[min(Doy),0.9*min(Tn);max(Doy),1.1*max(Tx)]
a.sub_tics=[4,5]
a.auto_ticks

xtitle("","DOY","Tar (oC)")
legend(['Tn';'Tm';'Tx'])

subplot(5,1,2)
bar(Doy, PCP,'blue1');
plot(Doy, ETo_HS,'green');
plot(Doy, ETo_PM,'red');

lines(0)
a=get("current_axes")
a.data_bounds=[min(Doy),0;max(Doy),1.1*max(PCP)]
 
xtitle("","DOY","ETo e Chuva (mm)")
legend(['Chuva';'PM';'HS'])

subplot(5,1,3)
plot(Doy,URn,'cyan');
plot(Doy,URm,'blue'); 
plot(Doy,URx,'red');

lines(0)
a=get("current_axes")
a.data_bounds=[min(Doy),0.9*min(URn);max(Doy),1.1*max(URx)]
a.sub_tics=[4,5]
a.auto_ticks

xtitle("","DOY","UR (%)")
legend(['URn';'URm';'URx'])

subplot(5,1,4)
plot(Doy,U2,'blue');

lines(0)
a=get("current_axes")
a.data_bounds=[min(Doy),0.9*min(U2);max(Doy),1.1*max(U2)]
a.sub_tics=[4,5]
a.auto_ticks

xtitle("","DOY","U2 (m/s)")
legend(['U2'])

subplot(5,1,5)
plot(Doy,Ra,'red');
plot(Doy,Rs,'blue');
plot(Doy,Rn,'cyan');

lines(0)
a=get("current_axes")
a.data_bounds=[min(Doy),0.9*min(Rn);max(Doy),1.1*max(Ra)]
a.sub_tics=[4,5]
a.auto_ticks

xtitle("","DOY","Radiação (M/m² d)")
legend(['Ra';'Rs';'Rn'])
