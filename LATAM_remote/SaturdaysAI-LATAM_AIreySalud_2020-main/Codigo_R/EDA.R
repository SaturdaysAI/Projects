#https://diegokoz.github.io/Curso_R_EPH_clases/
#https://www.youtube.com/watch?v=l3nIKwZSRSc #Openair
#https://www.youtube.com/watch?v=AzLMCjOC_mk #promedios
#https://www.ncei.noaa.gov/access/search/data-search/global-hourly #NOAA #National Centers for Environmental Information
#https://github.com/davidcarslaw/worldmet


#Citation
#Carslaw, D. C. and K. Ropkins, (2012) openair --- an R package for air quality data analysis. Environmental Modelling & Software. Volume 27-28, 52-61.

#Instala wordlmet desde Github3
#require(devtools)
#install_github('davidcarslaw/worldmet')

#Paquetes ====
library(here)
library(tidyverse)
library(openair)
library(lubridate)
library(leaflet) #maps
library(worldmet)
library(softImpute)
#library(carData)
#library(car) #recode()
#library(compare) #compara renglones de dos df
#library(sqldf) #compara filas de dos df

#Funciones ====
'%nin%' <- Negate('%in%')

#Datos ====
loc <- read.csv(here("CA","BD","cat_estacion.csv"))

df<- read.csv(here("CA","base_analisis_ancho_2015_2020.csv"))
names(df) <- tolower(names(df))
names(df)[names(df)%in%c("no","pa","pba","pmco","wdr","wsp")] <- c("NO","PA","PBa","PMCo","wd","ws")

#respalda.rds
saveRDS(df,here("CA","BD","rds","df.rds"))
saveRDS(loc,here("CA","BD","rds","loc.rds"))
saveRDS(meteoNOAA,here("CA","BD","rds","meteoNOAA.rds"))
saveRDS(tray,here("CA","BD","rds","tray.rds"))
saveRDS(info,here("CA","BD","rds","info.rds"))

#carga datos rds ====
df <- readRDS(here("CA","BD","rds","df.rds"))
loc <- readRDS(here("CA","BD","rds","loc.rds"))
meteoNOAA <- readRDS(here("CA","BD","rds","meteoNOAA.rds"))
tray <- readRDS(here("CA","BD","rds","tray.rds"))
info <- readRDS(here("CA","BD","rds","info.rds"))

df <- as.data.frame(df)
df[,3] <- dmy(df[,3]) 
df$Date <- make_datetime(year(df[,3]),month(df[,3]),day(df[,3]),df$Hour)
df$year <- year(df[,3])
df$month <- month(df[,3])

names(df)[c(3:5,22,6:21)]
df <- df[,c(3:5,22,6:21)]
names(df)[1] <- 'date'
#date2 <- ymd_hms(df$date,tz="America/Mexico_City") #cambiar el formato de fecha a  Sys.timezone(location=TRUE) America/Mexico_City
param <- names(df)[-c(1:5)]
str(df)


#Mapa ====
names(loc)
loc2 <- loc[loc$cve_estac%in%unique(df$id_station),]
content <- paste(
    paste(
        loc2$cve_estac,
        paste("Altitud:", loc2$alt),
        sep = "<br/>"
    )
)

# paste("Start:", loc$start_date),
# paste("End:", loc$end_date),
# paste("Site Type:", loc$site_type),

#visualizar las 11 estaciones

leaflet(loc2) %>%
    addTiles() %>%
    addMarkers(~ longitud, ~ latitud, popup = content,
               clusterOptions = markerClusterOptions())

#Sitios de la NOAA ====

getMeta(site = "mexico") #Code: 766800-99999 766793-99999 766810-99999
info <- getMeta(lat = 19.4, lon = -99.2)
info <- info[info$code%in%c("766800-99999","766793-99999","766810-99999"),]

meteoNOAA <- importNOAA(code = info$code, year = c(2015:2020))
names(meteoNOAA)
unique(meteoNOAA$code)
windRose(meteoNOAA,type="code",main="NOAA")


#Uso de openair ====
openair::

p1="pm2.5"

#dispersion
for(e in unique(df[,"id_station"])){
    pdf(here("CA","graficos",paste0(e,".pdf")))    
        datos <- df[df["id_station"]==e,-c(2:5,20)] #date y parametros
        summaryPlot(datos,clip=FALSE,percentil=0.95,type="density",main=e) #,avg.time="12 hour",period="months"
        timeVariation(datos,pollutant=p1,main=e)
        trendLevel(datos,pollutant=p1,border="BLACK",main=e)
        smoothTrend(datos,pollutant=p1,main=e)
        for(y in unique(year(datos$date))){calendarPlot(datos,pollutant=p1,year=y,main=e)} #annotate="wsp",
        for(p2 in param[param%nin%p1]){
            #scatterPlot(datos,x=p1,y=p2,z="wdr",type=c("year","season")) #,type="season""
            #scatterPlot(datos,x=p1,y=p2,z="wd",type=c("seasonyear")) #,type="season""
            scatterPlot(datos,x=p1,y=p2,type=c("seasonyear"),main=e) #,type="season""
        } #for p2
    dev.off()
} #for e

#rosas de viento y contaminantes
e <- unique(df[!is.na(df[,"wd"]),"id_station"])[1]

for(e in unique(df[!is.na(df[,"wd"]),"id_station"])){
    pdf(here("CA","graficos",paste0(e,"_WR.pdf")))    
        datos <- df[df["id_station"]==e,-c(2,18)]
        windRose(datos,ws="ws",wd="wd",paddle=FALSE,type="year",main=e)
        windRose(datos,ws="ws",wd="wd",paddle=FALSE,type=c("year","season"),main=e)
        windRose(datos,ws="ws",wd="wd",paddle=FALSE,type=c("seasonyear"),main=e)
        pollutionRose(datos,pollutant=p1,main=e)
        polarPlot(datos,pollutant=p1,main=e,remove.calm=TRUE)
        polarAnnulus(datos,pollutant=p1,remove.calm=TRUE,type=c("year","season"),main=e)
        polarAnnulus(datos,pollutant=p1,remove.calm=TRUE,type=c("seasonyear"),main=e)
        polarAnnulus(datos,pollutant=p1,remove.calm=TRUE,period="season",main=e)
        polarAnnulus(datos,pollutant=p1,remove.calm=TRUE,period="trend",main=e)
    dev.off()
} #for e

tray <- importTraj(site="ny-alesund",year=c(2013),local=NA)
trajPlot(tray,type="season")

#PM2.5 movil24h ====
for(e in unique(df[,"id_station"])){
    datos <- df[df[,"id_station"]==e,c("date","pm2.5")]
    datos <- rollingMean(datos, pollutant = "pm2.5", hours = 24, new.name = "mov24h", data.thresh = 75)
    #timeAverage(datos,av.time="24 hour",data.thresh = 75) promedio de 24h
}
mydata <- rollingMean(mydata, pollutant = "o3", hours = 8,
                      new.name = "rollingo3", data.thresh = 75)
tail(mydata)

#aqStats()
#splitByDate()


#EDA ====
pdf(here("CA","graficos","BxP_P.pdf"))
    for(v in param){
        boxplot(df[,v]~df[,"id_station"],xlab="station",ylab=v,las=2)
    }
dev.off()



#Intervalos CA ====

df$pm2.5_int <- cut(df$pm2.5, 
                        breaks = c(0, 50, 100, 150, 1000), 
                        labels = c("Very low", "Low", "High",
                                   "Very High"), 
                        include.lowest = TRUE)



#Relleno de faltantes ====
