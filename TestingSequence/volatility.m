
function [vol_A,kvalita_dat,peak_data] = volatility(data,filtrPos,filtrNeg)
%function [vol_A,kvalita_dat,peak_data] = volatility(data,filtrH, filteL)
%VSTUPY
%   data musí být ve formátu (X,1), kde X jsou roèní ceny v
%   libovolném rozlišení, tedy napø. pro hodinová data budou data ve formátu
%   (8760,1)
%   druhým vstupem fce je filtr = absolutní hodnota, která pøedstavuje max
%   a min cenu která se bude v datasetu uvažovat, ostatní hodnoty budou
%   odfiltrovány
%VÝSTUPY
%   výsledkem funkce (vol_A) je roèní index volatility
%   druhý výstup funkce (kvalita_dat) dává informaci o kvalitì datasetu v %
%   (100% = dataset bez chyb, 0% pouze chybná data). Za chybu je
%   považován NaN a inf
%   výstup peak_data dává info o relativním množství extrémních hodnot,
%   které byly odfiltrovány z datasetu

%pøíprava datasetu k výpoètu - posun dat vùèi sobì o 1 pozici
GridPrice = data(1:(end-1),:);
GridPrice_posun = data(2:end,:);
%výpoèet odchylek Xi-(Xi-1)
ri = GridPrice_posun-GridPrice;

%výpoèet kvality dat
chybna_data = length(ri(isnan(ri))) + length(ri(isinf(ri)));
kvalita_dat = 100-(chybna_data/(length(GridPrice)))*100;

%èištìní dat
ri = ri(not(isnan(ri)) & not(isinf(ri)));

%filtrace extrémních hodnot odchylek ri
ri_filtr = ri(ri <= filtrPos & ri >= filtrNeg);
ri_peak_low = ri(ri < filtrNeg);
ri_peak_high = ri(ri > filtrPos);
peak_data = ((length(ri_peak_low)+length(ri_peak_high))/length(ri))*100;
%výpoèet volatility
ri_av = mean(ri_filtr);
r_dev = (ri_filtr-ri_av).^2;
dev = (mean(r_dev)).^0.5;
vol_A = dev;
end




