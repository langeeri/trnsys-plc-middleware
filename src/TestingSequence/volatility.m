
function [vol_A,kvalita_dat,peak_data] = volatility(data,filtrPos,filtrNeg)
%function [vol_A,kvalita_dat,peak_data] = volatility(data,filtrH, filteL)
%VSTUPY
%   data mus� b�t ve form�tu (X,1), kde X jsou ro�n� ceny v
%   libovoln�m rozli�en�, tedy nap�. pro hodinov� data budou data ve form�tu
%   (8760,1)
%   druh�m vstupem fce je filtr = absolutn� hodnota, kter� p�edstavuje max
%   a min cenu kter� se bude v datasetu uva�ovat, ostatn� hodnoty budou
%   odfiltrov�ny
%V�STUPY
%   v�sledkem funkce (vol_A) je ro�n� index volatility
%   druh� v�stup funkce (kvalita_dat) d�v� informaci o kvalit� datasetu v %
%   (100% = dataset bez chyb, 0% pouze chybn� data). Za chybu je
%   pova�ov�n NaN a inf
%   v�stup peak_data d�v� info o relativn�m mno�stv� extr�mn�ch hodnot,
%   kter� byly odfiltrov�ny z datasetu

%p��prava datasetu k v�po�tu - posun dat v��i sob� o 1 pozici
GridPrice = data(1:(end-1),:);
GridPrice_posun = data(2:end,:);
%v�po�et odchylek Xi-(Xi-1)
ri = GridPrice_posun-GridPrice;

%v�po�et kvality dat
chybna_data = length(ri(isnan(ri))) + length(ri(isinf(ri)));
kvalita_dat = 100-(chybna_data/(length(GridPrice)))*100;

%�i�t�n� dat
ri = ri(not(isnan(ri)) & not(isinf(ri)));

%filtrace extr�mn�ch hodnot odchylek ri
ri_filtr = ri(ri <= filtrPos & ri >= filtrNeg);
ri_peak_low = ri(ri < filtrNeg);
ri_peak_high = ri(ri > filtrPos);
peak_data = ((length(ri_peak_low)+length(ri_peak_high))/length(ri))*100;
%v�po�et volatility
ri_av = mean(ri_filtr);
r_dev = (ri_filtr-ri_av).^2;
dev = (mean(r_dev)).^0.5;
vol_A = dev;
end




