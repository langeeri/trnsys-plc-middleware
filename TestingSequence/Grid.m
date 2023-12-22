 clear all
 clc
 close all
Gdata=load('CZE_2015_2021.mat');
GdataPrice=Gdata.data.CZ.DAhPrice.DAhPrice;
GdataPrice=unique(GdataPrice);
GdataCO2=Gdata.data.CZ.AggregatedGeneration.AggregatedGeneration;
%% GRID
TimeStamp=GdataPrice.timeMat;
normPrice=zeros(length(GdataPrice.Price),1);
normHDO=zeros(length(GdataPrice.Price),1);
c=0;
for y=2015:2021    
    xd=length(TimeStamp(hour(TimeStamp)==12 & year(TimeStamp)==y));
for d=1:xd
 c=c+1;  
normPriced=(GdataPrice.Price(year(TimeStamp)==y & day(TimeStamp,'dayofyear')==d)-mean(GdataPrice.Price(year(TimeStamp)==y & day(TimeStamp, 'dayofyear')==d))) ...
     ./(max(GdataPrice.Price(year(TimeStamp)==y & day(TimeStamp, 'dayofyear')==d))-min(GdataPrice.Price(year(TimeStamp)==y & day(TimeStamp, 'dayofyear')==d)));
 
normPrice(year(TimeStamp)==y & day(TimeStamp,'dayofyear')==d)= normPriced;
Vol_rel(c,1)= volatility(normPriced,10,-10);%(max(normPrice(year(TimeStamp)==y & day(TimeStamp, 'dayofyear')==d))-min(normPrice(year(TimeStamp)==y & day(TimeStamp, 'dayofyear')==d))); 
Vol_abs(c,1)= volatility(GdataPrice.Price(year(TimeStamp)==y & day(TimeStamp, 'dayofyear')==d),1000,-200); %(max(GdataPrice.Price(year(TimeStamp)==y & day(TimeStamp, 'dayofyear')==d))-min(GdataPrice.Price(year(TimeStamp)==y & day(TimeStamp, 'dayofyear')==d))); 

% normHDOd=double(GdataPrice.Price((year(TimeStamp)==y & day(TimeStamp,'dayofyear')==d)) ...
%        <= prctile(GdataPrice.Price(year(TimeStamp)==y & day(TimeStamp,'dayofyear')==d),33.333333)).*-1;
% normHDO(year(TimeStamp)==y & day(TimeStamp,'dayofyear')==d)=normHDOd;

end
end
TimeStamp2=TimeStamp(hour(TimeStamp)==12);
TS_winter=TimeStamp2(month(TimeStamp2)== 1 | month(TimeStamp2)== 2 | month(TimeStamp2)== 12 | month(TimeStamp2)== 3);
TS_summer=TimeStamp2(month(TimeStamp2)== 6 | month(TimeStamp2)== 7 | month(TimeStamp2)== 8 | month(TimeStamp2)== 9);

Vol_winter=Vol_abs(month(TimeStamp2)== 1 | month(TimeStamp2)== 2 | month(TimeStamp2)== 12 | month(TimeStamp2)== 3);
Vol_summer=Vol_abs(month(TimeStamp2)== 6 | month(TimeStamp2)== 7 | month(TimeStamp2)== 8 | month(TimeStamp2)== 9);

Vol_winter_diff=abs(Vol_winter-prctile(Vol_winter,50));
Vol_summer_diff=abs(Vol_summer-prctile(Vol_winter,50));


% Typical_day_winter=TS_winter(Vol_winter_diff==min(Vol_winter_diff));
% Typical_day_summer=TS_summer(Vol_summer_diff==min(Vol_summer_diff));
% 
% normPriceTD_winter=normPrice(TimeStamp>=Typical_day_winter-hours(12) & TimeStamp<Typical_day_winter+hours(12));
% normPriceTD_summer=normPrice(TimeStamp>=Typical_day_summer-hours(12) & TimeStamp<Typical_day_summer+hours(12));
% 
% Vol_winter_diff=abs(Vol_winter-prctile(Vol_winter,2));
% Vol_summer_diff=abs(Vol_summer-prctile(Vol_winter,2));
% 
% Extreme_day_winter=TS_winter(Vol_winter_diff==min(Vol_winter_diff));
% Extreme_day_summer=TS_summer(Vol_summer_diff==min(Vol_summer_diff));
% 
% normPriceED_winter=normPrice(TimeStamp>=Extreme_day_winter-hours(12) & TimeStamp<Extreme_day_winter+hours(12));
% normPriceED_summer=normPrice(TimeStamp>=Extreme_day_summer-hours(12) & TimeStamp<Extreme_day_summer+hours(12));
normProfiles=[normPriceTD_winter normPriceTD_summer];
normProfiles=normProfiles-mean(normProfiles,1);


HDOProfiles=double(normProfiles<= prctile(normProfiles,33.33333,1))*-1;
HDOProfiles=HDOProfiles-mean(HDOProfiles,1);

