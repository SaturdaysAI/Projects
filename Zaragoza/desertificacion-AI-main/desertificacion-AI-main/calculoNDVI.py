import os, rasterio
from rasterio import plot
import matplotlib.pyplot as plt
import glob
import numpy as np
from osgeo import gdal 

#Path de salida donde almacenaremos los ficheros generados
outfile = './out'
#Path de la imagen de Sentinel2 descargada 
imagePath = './Sentinel2/GRANULE/L2A_T30TXN_A022671_20210709T105443/IMG_DATA/R10m/'
#Bandas de imagenes
'''band2 = rasterio.open(imagePath+'T30TXN_20210709T104619_B02_10m.jp2', driver='JP2OpenJPEG') #blue
band3 = rasterio.open(imagePath+'T30TXN_20210709T104619_B03_10m.jp2', driver='JP2OpenJPEG') #green
band4 = rasterio.open(imagePath+'T30TXN_20210709T104619_B04_10m.jp2', driver='JP2OpenJPEG') #red
band8 = rasterio.open(imagePath+'T30TXN_20210709T104619_B08_10m.jp2', driver='JP2OpenJPEG') #nir

#https://desktop.arcgis.com/es/arcmap/10.3/manage-data/raster-and-images/raster-bands.htm
#Numero de bandas de raster
print(band4.count)
#Numero de columnas
print(band4.width)
#Numero de filas
print(band4.height)
#Visualizacion de la banda 4
plot.show(band4)

#Sobre la imagen de banda 4 varias caracteristicas de rasterio
#Tipo raster https://www.um.es/geograf/sigmur/sigpdf/temario_4.pdf 
#dtype: the data type of the dataset
print(band4.dtypes[0])
#crs: a coordinate reference system identifier or description
print(band4.crs)
#transform: an affine transformation matrix
print(band4.transform)
#The read() method returns a Numpy N-D array.
print(band4.read(1))'''

#Ventana plot de varias imagenes a la vez
'''fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(12, 4))
plot.show(band2, ax=ax1, cmap='Blues')
plot.show(band3, ax=ax2, cmap='Greens')
plot.show(band4, ax=ax3, cmap='Reds')
plot.show(band8, ax=ax4, cmap='Nir')
fig.tight_layout()'''

#Imagen color Verdadero
'''trueColor = rasterio.open('./out/SentinelTrueColor2.tiff','w',driver='Gtiff',
                         width=band4.width, height=band4.height,
                         count=3,
                         crs=band4.crs,
                         transform=band4.transform,
                         dtype=band4.dtypes[0]
                         )
trueColor.write(band2.read(1),3) #blue
trueColor.write(band3.read(1),2) #green
trueColor.write(band4.read(1),1) #red
trueColor.close()

src = rasterio.open(r"./out/SentinelTrueColor2.tiff", count=3)
plot.show(src)'''

#Imagen Falso color
'''falseColor = rasterio.open('./out/SentinelFalseColor.tiff', 'w', driver='Gtiff',
                          width=band2.width, height=band2.height,
                          count=3,
                          crs=band2.crs,
                          transform=band2.transform,
                          dtype='uint16'                   
                         )
falseColor.write(band3.read(1),3) #Blue
falseColor.write(band4.read(1),2) #Green
falseColor.write(band8.read(1),1) #Red
falseColor.close()

#Generacion de un histograma de la imagen de color verdadero
trueColor = rasterio.open('./out/SentinelTrueColor2.tiff')
#Visualizacion del histograma
plot.show_hist(trueColor, bins=50, lw=0.0, stacked=False, alpha=0.3, histtype='stepfilled', title="Histogram")
'''
#open the bands (I can't believe how easy is this with rasterio!)

#PRUEBA 1 de calculo de ndvi
'''RED = band4.read(1)
NIR = band8.read(1)
print(NIR.astype(float))
print(RED.astype(float))
ndvi = (NIR.astype(float) - RED.astype(float)) / (NIR+RED)'''


#Calculo de NDVI 
imagePath = './31TBG/20210316/GRANULE/20210316/IMG_DATA/'
imagePath = './31TBG/20210405/GRANULE/20210405/IMG_DATA/'
imagePath = './31TBG/20210505/GRANULE/20210505/IMG_DATA/'
imagePath = './31TBG/20210525/GRANULE/20210525/IMG_DATA/'
imagePath = './31TBG/20210614/GRANULE/20210614/IMG_DATA/'
imagePath = './31TBG/20210624/GRANULE/20210624/IMG_DATA/'
imagePath = './31TBG/20210714/GRANULE/20210714/IMG_DATA/'
imagePath = './31TBG/20210813/GRANULE/20210813/IMG_DATA/'
imagePath = './31TBG/20210823/GRANULE/20210823/IMG_DATA/'
imagePath = './31TBG/20210912/GRANULE/20210912/IMG_DATA/'
imagePath = './31TBG/20211027/GRANULE/20211027/IMG_DATA/'
imagePath = './31TBG/20211206/GRANULE/20211206/IMG_DATA/'
imagePath = './31TBG/20211116/GRANULE/20211116/IMG_DATA/'
imagePath = './31TBG/20210219/GRANULE/20210219/IMG_DATA/'
imagePath = './31TBG/20220120/GRANULE/20220120/IMG_DATA/'


red_file = glob.glob(imagePath+'T31TBG_20210405T105021_B04.jp2') # red band
nir_file = glob.glob(imagePath+'T31TBG_20210405T105021_B08.jp2') # nir band
red_file = glob.glob(imagePath+'T31TBG_20210505T105031_B04.jp2') # red band
nir_file = glob.glob(imagePath+'T31TBG_20210505T105031_B08.jp2') # nir band
red_file = glob.glob(imagePath+'T31TBG_20210525T105031_B04.jp2') # red band
nir_file = glob.glob(imagePath+'T31TBG_20210525T105031_B08.jp2') # nir band
red_file = glob.glob(imagePath+'T31TBG_20210614T105031_B04.jp2') # red band
nir_file = glob.glob(imagePath+'T31TBG_20210614T105031_B08.jp2') # nir band
red_file = glob.glob(imagePath+'T31TBG_20210624T105031_B04.jp2') # red band
nir_file = glob.glob(imagePath+'T31TBG_20210624T105031_B08.jp2') # nir band
red_file = glob.glob(imagePath+'T31TBG_20210714T105031_B04.jp2') # red band
nir_file = glob.glob(imagePath+'T31TBG_20210714T105031_B08.jp2') # nir band
red_file = glob.glob(imagePath+'T31TBG_20210813T105031_B04.jp2') # red band
nir_file = glob.glob(imagePath+'T31TBG_20210813T105031_B08.jp2') # nir band
red_file = glob.glob(imagePath+'T31TBG_20210823T105031_B04.jp2') # red band
nir_file = glob.glob(imagePath+'T31TBG_20210823T105031_B08.jp2') # nir band
red_file = glob.glob(imagePath+'T31TBG_20210912T105031_B04.jp2') # red band
nir_file = glob.glob(imagePath+'T31TBG_20210912T105031_B08.jp2') # nir band
red_file = glob.glob(imagePath+'T31TBG_20211027T105049_B04.jp2') # red band
nir_file = glob.glob(imagePath+'T31TBG_20211027T105049_B08.jp2') # nir band
red_file = glob.glob(imagePath+'T31TBG_20211206T105329_B04.jp2') # red band
nir_file = glob.glob(imagePath+'T31TBG_20211206T105329_B08.jp2') # nir band
red_file = glob.glob(imagePath+'T31TBG_20211116T105229_B04.jp2') # red band
nir_file = glob.glob(imagePath+'T31TBG_20211116T105229_B08.jp2') # nir band
red_file = glob.glob(imagePath+'T31TBG_20210219T104959_B04.jp2') # red band
nir_file = glob.glob(imagePath+'T31TBG_20210219T104959_B08.jp2') # nir band
red_file = glob.glob(imagePath+'T31TBG_20220120T105351_B04.jp2') # red band
nir_file = glob.glob(imagePath+'T31TBG_20220120T105351_B08.jp2') # nir band


# Abrimos las bandas con gdal
red_link = gdal.Open(red_file[0])
nir_link = gdal.Open(nir_file[0])
 
# Lee cada banda como array y pasamos a float para el calculo
red = red_link.ReadAsArray().astype(np.float64)
nir = nir_link.ReadAsArray().astype(np.float64)

# Funcion de calculo de NDVI
def ndvi(red, nir):
 return ((nir - red)/(nir + red))

# Calculamos el indice
ndvi2 = ndvi(red, nir)
 
# Se crea un fichero de salida en pase al fichero de banda 4
#outfile_name = red_file[0].split('_B')[0] + '_NDVI.tif'
outfile_name='./out/T31TBG_20210316T105031_B_NDVI.tif' 
outfile_name='./out/T31TBG_20210405T105021_B_NDVI.tif' 
outfile_name='./out/T31TBG_20210505T105031_B_NDVI.tif' 
outfile_name='./out/T31TBG_20210525T105031_B_NDVI.tif' 
outfile_name='./out/T31TBG_20210614T105031_B_NDVI.tif' 
outfile_name='./out/T31TBG_20210624T105031_B_NDVI.tif' 
outfile_name='./out/T31TBG_20210714T105031_B_NDVI.tif'
outfile_name='./out/T31TBG_20210813T105031_B_NDVI.tif'
outfile_name='./out/T31TBG_20210823T105031_B_NDVI.tif'
outfile_name='./out/T31TBG_20210912T105031_B_NDVI.tif'
outfile_name='./out/T31TBG_20211027T105049_B_NDVI.tif'
outfile_name='./out/T31TBG_20211206T105329_B_NDVI.tif'
outfile_name='./out/T31TBG_20211116T105229_B_NDVI.tif'
outfile_name='./out/T31TBG_20210219T104959_B_NDVI.tif'
outfile_name='./out/T31TBG_20220120T105351_B_NDVI.tif'

x_pixels = ndvi2.shape[0] # pixels en eje x
y_pixels = ndvi2.shape[1] # pixels en eje y
 
# GeoTIFF de salida
driver = gdal.GetDriverByName('GTiff') 

ndvi_data = driver.Create(outfile_name,x_pixels, y_pixels, 1,gdal.GDT_Float32)
 
# Incluye el array ndvi como banda 1 raster
ndvi_data.GetRasterBand(1).WriteArray(ndvi2)
 
# Incluye el sistema de referencia de coordenadas geotiff
geotrans=red_link.GetGeoTransform() # entrada informacion GeoTransform 
proj=red_link.GetProjection() # Graba informacion GeoTransform del fichero de entrada

ndvi_data.SetGeoTransform(geotrans) 
ndvi_data.SetProjection(proj)
ndvi_data.FlushCache()
ndvi_data=None
###############################################################################

plot.show(rasterio.open(outfile_name))

