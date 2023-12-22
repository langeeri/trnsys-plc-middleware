clear all
clc
%close all

%% Weather
Wdata=importfileWDat("Prague_Libus-min_skartveit.dat");
HDH=zeros(365,1);
CDH=zeros(365,1);
Solar=zeros(365,3);
Tdif_HDH=(21-Wdata.Ta);
Tdif_HDH(Tdif_HDH<0)=0;

Tdif_CDH=(Wdata.Ta-24);
Tdif_CDH(Tdif_CDH<0)=0;


 for d =1:365
  HDH(d)=sum(Tdif_HDH(Wdata.dy==d))*365/length(Tdif_HDH); %conversion to degreehours for sub hourly data;
  CDH(d)=sum(Tdif_CDH(Wdata.dy==d))*365/length(Tdif_CDH); 
  Solar(d,:)=[sum(Wdata.G_Gk(Wdata.dy==d)),sum(Wdata.G_Dk(Wdata.dy==d)),sum(Wdata.G_Bn(Wdata.dy==d))]*365*24/length(Wdata.dy)./1000;
 end
 
DDH=[HDH,CDH];

DaysWinSeas=unique(Wdata.dy(Wdata.m==1 | Wdata.m==2 | Wdata.m==3 | Wdata.m==12 | Wdata.m==4 | Wdata.m==11)); 
%DaysIntSeas=unique(Wdata.dy(Wdata.m==10 | Wdata.m==11 | Wdata.m==4 | Wdata.m==5));
DaysSumSeas=unique(Wdata.dy(Wdata.m==6 | Wdata.m==7 | Wdata.m==8 | Wdata.m==9));





% [day,pos]=max(HDH);
% TestingSeq=[array2table(ones(length(Wdata.dy)/365,1).*1) Wdata(Wdata.dy==pos,:)];

%extreme days
prc_LR=98;
prc_HR=100;

TypDay_LR=prctile(HDH(DaysWinSeas),prc_LR);
TypDay_HR=prctile(HDH(DaysWinSeas),prc_HR);

posT=find(HDH>TypDay_LR & HDH<TypDay_HR);


  

[dday,posS]=min(Solar(posT,1)-Solar(posT,2));

TestingSeq=[array2table(ones(length(Wdata.dy)/365,1).*1) Wdata(Wdata.dy==posT(posS),:)];
%TestingSeq =[TestingSeq;array2table(ones(length(Wdata.dy)/365,1).*2) Wdata(Wdata.dy==posT(posS),:)];


[dday,posS]=max(Solar(posT,1)-Solar(posT,2));


TestingSeq=[TestingSeq;array2table(ones(length(Wdata.dy)/365,1).*2) Wdata(Wdata.dy==posT(posS),:)];

 figure
   histogram(HDH(DaysWinSeas),16)
   hold on
   plot(TypDay_LR.*(ones(1,26)),0:25)
   plot(TypDay_HR.*(ones(1,26)),0:25)
%typical ddays
prc_LR=40;
prc_HR=60;

TypDay_LR=prctile(HDH(DaysWinSeas),prc_LR);
TypDay_HR=prctile(HDH(DaysWinSeas),prc_HR);

posT=find(HDH>TypDay_LR & HDH<TypDay_HR);


  

[dday,posS]=min(Solar(posT,1)-Solar(posT,2));

TestingSeq =[TestingSeq;array2table(ones(length(Wdata.dy)/365,1).*3) Wdata(Wdata.dy==posT(posS),:)];


[dday,posS]=max(Solar(posT,1)-Solar(posT,2));


TestingSeq=[TestingSeq;array2table(ones(length(Wdata.dy)/365,1).*4) Wdata(Wdata.dy==posT(posS),:)];


   plot(TypDay_LR.*(ones(1,26)),0:25)
   plot(TypDay_HR.*(ones(1,26)),0:25)

   
posT=find(CDH>0);
figure

hist3([CDH(posT,1),Solar(posT,1)],[5,5],'CdataMode','auto','FaceAlpha',0.2, 'EdgeColor', 'none' ) 
view(2)
hold on
scatter(CDH(posT,1),Solar(posT,1),'x','MarkerEdgeColor',[0 0 0])


prc_LR=40;
prc_HR=60;

%TypDay_LR=prctile(Solar(posT,1)-Solar(posT,2),prc_LR);
%TypDay_HR=prctile(Solar(posT,1)-Solar(posT,2),prc_HR);
posS=find(Solar(posT,1)>= prctile(Solar(posT,1),prc_LR) & Solar(posT,1)<= prctile(Solar(posT,1),prc_HR));% & CDH(posT)>=prctile(CDH(posT),prc_LR) & CDH(posT)<=prctile(CDH(posT),prc_HR)); 
posS=posS(abs(CDH(posT(posS))- mean(CDH(posT(posS))))==min(abs(CDH(posT(posS))- mean(CDH(posT(posS))))));
%posS=find(Solar(posT)==max(Solar(posT(posS))));%[dday,posS]=max(Solar(posT(posS),1))%posS=find(CDH(posT)>=prctile(CDH(posT),prc_LR) & CDH(posT)<=prctile(CDH(posT),prc_HR))

    hold on
    scatter(CDH(posT(posS),1),Solar(posT(posS),1))

TestingSeq=[TestingSeq;array2table(ones(length(Wdata.dy)/365,1).*5) Wdata(Wdata.dy==posT(posS),:)];

posS=find(CDH(posT)==prctile(CDH(posT),100));
    hold on
    scatter(CDH(posT(posS),1),Solar(posT(posS),1))

TestingSeq=[TestingSeq;array2table(ones(length(Wdata.dy)/365,1).*6) Wdata(Wdata.dy==posT(posS),:)];


posS=find(Solar(posT,1)==prctile(Solar(posT,1),100));
    hold on
    scatter(CDH(posT(posS),1),Solar(posT(posS),1))

TestingSeq=[TestingSeq;array2table(ones(length(Wdata.dy)/365,1).*7) Wdata(Wdata.dy==posT(posS),:)];

%summer ddays


% %intermseason
% TypDay_LR=prctile(HDH(DaysIntSeas),prc_LR);
% TypDay_HR=prctile(HDH(DaysIntSeas),prc_HR);
% 
% posT=find(HDH(DaysIntSeas)>TypDay_LR & HDH(DaysIntSeas)<TypDay_HR);
% length(posT)
% 
% [dday,posS]=min(Solar(posT,1)-Solar(posT,2));
% 
% TestingSeq =[TestingSeq;array2table(ones(length(Wdata.dy)/365,1).*4) Wdata(Wdata.dy==posT(posS),:)];
% 
% [dday,posS]=max(Solar(posT,1)-Solar(posT,2));
% 
% TestingSeq=[TestingSeq;array2table(ones(length(Wdata.dy)/365,1).*5) Wdata(Wdata.dy==posT(posS),:)];
% 
% 
%    figure
%    histogram(HDH(DaysIntSeas),16)
%    hold on
%    plot(TypDay_LR.*(ones(1,26)),0:25)
%    plot(TypDay_HR.*(ones(1,26)),0:25)


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


Typical_day_winter=TS_winter(Vol_winter_diff==min(Vol_winter_diff));
Typical_day_summer=TS_summer(Vol_summer_diff==min(Vol_summer_diff));

normPriceTD_winter=normPrice(TimeStamp>=Typical_day_winter-hours(12) & TimeStamp<Typical_day_winter+hours(12));
normPriceTD_summer=normPrice(TimeStamp>=Typical_day_summer-hours(12) & TimeStamp<Typical_day_summer+hours(12));

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
 %% reporting
 TestingSeq.price=zeros(length(TestingSeq.Var1),1);
 
 baseprice=5;
 vol=[0 2 2 4];
 lable={'fixPrice','HDO','varPrice_L','varPrice_H'};
 figure
 for c=1:4
   switch c
       case 1
       priceprofile=baseprice.*ones(24,2);   
       case 2
       priceprofile=HDOProfiles.*vol(c)+baseprice;
       case 3
       priceprofile=normProfiles.*vol(c)+baseprice;
       case 4
       priceprofile=normProfiles.*vol(c)+baseprice;
  end
   plot(priceprofile)
   hold on
     
 for d=1:7
      if d<=4 
         s=1;                 
      else      
         s=2;
      end
      
      for h=1:24
        
                      
            TestingSeq.price(TestingSeq.h==(h-1) & TestingSeq.Var1==d)=ones(length(TestingSeq.price(TestingSeq.h==(h-1) & TestingSeq.Var1==d)),1).*priceprofile(h,s);     
            
        
      end
 fileName=['case_' lable{c} 'day_' num2str(d) '.csv'];       
 writetable(TestingSeq(TestingSeq.Var1==d,:),fileName)

 end
  %figure
 %plot(TestingSeq.price)
 end

plotyy([1:length(TestingSeq.G_Gk)]'./60./24,table2array(TestingSeq(:,12:15)),[1:length(TestingSeq.G_Gk)]'./60./24,table2array(TestingSeq(:,15)))