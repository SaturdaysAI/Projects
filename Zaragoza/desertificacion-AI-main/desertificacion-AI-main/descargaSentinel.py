from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import geopandas

#Conexion a sentinel a https://scihub.copernicus.eu/dhus/#/home
api = SentinelAPI('desertificacion', 'SaturdayAI')

#PRUEBA 1 
#Definicion del area que queremos descargar
#area 1
#my_geojson = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-0.98052978515625,42.44372793752476],[-0.76080322265625,42.44372793752476],[-0.76080322265625,42.581399679665054],[-0.98052978515625,42.581399679665054],[-0.98052978515625,42.44372793752476]]]}}]}
#area 2
'''
my_geojson = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              -0.7305908203125,
              42.93229601903058
            ],
            [
              -0.9558105468749999,
              42.73087427928485
            ],
            [
              -1.285400390625,
              42.53689200787315
            ],
            [
              -1.40625,
              42.261049162113856
            ],
            [
              -1.29638671875,
              42.08191667830631
            ],
            [
              -1.40625,
              41.934976500546604
            ],
            [
              -1.86767578125,
              42.02481360781777
            ],
            [
              -1.77978515625,
              41.73033005046653
            ],
            [
              -1.988525390625,
              41.599013054830216
            ],
            [
              -1.9775390625,
              41.409775832009565
            ],
            [
              -2.120361328125,
              41.43449030894922
            ],
            [
              -2.120361328125,
              41.20345619205131
            ],
            [
              -1.9445800781249998,
              41.18692242290296
            ],
            [
              -1.6149902343749998,
              40.93841495689795
            ],
            [
              -1.5600585937499998,
              40.622291783092706
            ],
            [
              -1.8017578124999998,
              40.43858586704331
            ],
            [
              -1.483154296875,
              40.204050425113294
            ],
            [
              -1.2084960937499998,
              40.136890695345905
            ],
            [
              -1.131591796875,
              39.977120098439634
            ],
            [
              -0.8349609375,
              39.977120098439634
            ],
            [
              -0.758056640625,
              40.0360265298117
            ],
            [
              -0.63720703125,
              40.10328591293439
            ],
            [
              -0.54931640625,
              40.26276066437183
            ],
            [
              -0.494384765625,
              40.204050425113294
            ],
            [
              -0.263671875,
              40.38002840251183
            ],
            [
              -0.3515625,
              40.6306300839918
            ],
            [
              -0.10986328125,
              40.78054143186033
            ],
            [
              0.087890625,
              40.74725696280421
            ],
            [
              0.263671875,
              40.84706035607122
            ],
            [
              0.2911376953125,
              41.372686481864655
            ],
            [
              0.439453125,
              41.549700145132725
            ],
            [
              0.32958984375,
              41.6770148220322
            ],
            [
              0.4669189453125,
              41.775408403663285
            ],
            [
              0.7086181640625,
              42.10637370579324
            ],
            [
              0.68115234375,
              42.69858589169842
            ],
            [
              0.3350830078125,
              42.68243539838623
            ],
            [
              -0.0494384765625,
              42.67839711889055
            ],
            [
              -0.2801513671875,
              42.83972354764084
            ],
            [
              -0.5657958984375,
              42.79540065303723
            ],
            [
              -0.7305908203125,
              42.93229601903058
            ]
          ]
        ]
      }
    }
  ]
}'''
#Definicion de geojson para incluir en la query
#footprint = geojson_to_wkt(my_geojson)
##PRUEBA 2 
#footprint='GEOMETRYCOLLECTION(POLYGON((-1.2820340260311094 41.645019425778656,0.05651694830080148 41.645019425778656,0.05651694830080148 42.6375123889417,-1.2820340260311094 42.6375123889417,-1.2820340260311094 41.645019425778656)))'
#query de busqueda en sentinelsat del area indicada (footprint), fecha inicio=20210701, fecha fin=20210710
#del satelite Sentinel-2, y un % de nubes de 0 a 10
'''products = api.query(
		footprint,
    platformname = 'Sentinel-2',
    date = ('20210701', '20210710'),
    cloudcoverpercentage = (0,10),
    limit=1
)'''
#PRUEBA 3
#Fichero geojson con la definicion de las comunidades autonomas
fp = './comunidades-autonomas-espanolas-saturdays.geojson'
#Lectura del fichero
map_df = geopandas.read_file(fp)
#del fichero seleccionamos aragon
aragon=map_df[map_df['codigo']=='02']
aragon_simple=aragon['geometry'].iloc[0].convex_hull

#query de busqueda en sentinelsat del area indicada, fecha inicio=20160101, fecha fin=20200101
#del satelite Sentinel-2, y un % de nubes de 0 a 10
tile = '31TBG'

query_kwargs = {
        'platformname': 'Sentinel-2',
        'date': ('20210101', '20220201'),
        'relativeorbitnumber':'51'}
kw = query_kwargs.copy()
kw['tileid'] = tile
products = api.query(aragon_simple, cloudcoverpercentage = (0,10),**kw)
'''products = api.query(aragon_simple,                      
                      date = ('20210101', '20220201'),
                      platformname = 'Sentinel-2',
                      cloudcoverpercentage = (0,10)
                    )'''

#longitud
print(len(products))
#Para cada imagen seleccionada pinta el uuid y nos indica si esta online
for i in products:
    product = products[i]
    filename = product['title']
    print(filename)    
    #api.is_online(filename)
#api.to_geojson(products)


#De los datos seleccionados en la query se descargan todos
#api.download_all(products)

#Otras formas de descarga
#Todos los productos en el path indicado
#api.download_all(products, directory_path=r'C:\data')
#Descarga las imagenes de un uuid concreto
#api.get_product_odata('f3ba2485-e34f-4362-914d-91ce9e3900cb')
#api.download('53eee050-0041-4767-81d4-bf071a82205e')
