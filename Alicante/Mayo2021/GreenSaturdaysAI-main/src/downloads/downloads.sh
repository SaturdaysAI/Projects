#!/usr/bin/env bash

#TODO:
# [ ] set -P to wget to download stuff to temp/, change relevant stuff

# Mapas immisión
wget -i urls/urls_maps.txt
 
mkdir ../datasets/maps/2019
mkdir ../datasets/maps/2018
cp 2019* ../datasets/maps/2019/
cp 2018* ../datasets/maps/2018/
rm 2019* 2018*

# estaciones
wget -i urls/urls_estaciones.txt
mkdir ../datasets/estaciones/2021
mkdir ../datasets/estaciones/2020
mkdir ../datasets/estaciones/2019
mkdir ../datasets/estaciones/2018
cp 2021* ../datasets/estaciones/2021/
cp 2020* ../datasets/estaciones/2020/
cp 2019* ../datasets/estaciones/2019/
cp qualitat* ../datasets/estaciones/2018/

rm 2019* 2018* 2020* 2021*

# medidas
./medidas_download.sh
# Demasiado largo: puesto en su propio script

mkdir ../datasets/medidas/2021
mkdir ../datasets/medidas/2020
mkdir ../datasets/medidas/2019
mkdir ../datasets/medidas/2018
cp 2021* ../datasets/medidas/2021/
cp 2020* ../datasets/medidas/2020/
cp 2019* ../datasets/medidas/2019/
cp 2018* ../datasets/medidas/2018/

# meta
wget https://opendata-ajuntament.barcelona.cat/data/dataset/6960936a-95ed-4cc4-a6ec-e089197ccd8b/resource/c122329d-d26d-469e-bf9e-8efa10e4c127/download/qualitat_aire_contaminants.csv 
mv qualitat_aire_contaminants.csv ../datasets/meta/

wget https://opendata-ajuntament.barcelona.cat/data/dataset/0582a266-ea06-4cc5-a219-913b22484e40/resource/c2032e7c-10ee-4c69-84d3-9e8caf9ca97a/download
mv download* ../datasets/meta/qualitat.csv
