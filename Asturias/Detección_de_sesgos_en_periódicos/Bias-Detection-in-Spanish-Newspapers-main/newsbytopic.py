from scrapy.item import Item, Field
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

import re
import numpy as np
from datetime import datetime
import zoneinfo
import locale

categoryURLs = {
    "elconfidencial": {
        "aborto": "https://www.elconfidencial.com/tags/otros/aborto-7035/",
        "bildu": "https://www.elconfidencial.com/tags/organismos/bildu-4811/",
        "cambio-climatico": "https://www.elconfidencial.com/tags/temas/cambio-climatico-6047/",
        "casa-real": "https://www.elconfidencial.com/tags/organismos/casa-real-4106/",
        "ciudadanos": "https://www.elconfidencial.com/tags/organismos/ciudadanos-6359/",
        "covid": "https://www.elconfidencial.com/tags/temas/coronavirus-20888/",
        "cristianismo": "https://www.elconfidencial.com/tags/otros/cristianismo-5446/",
        "drogas": "https://www.elconfidencial.com/tags/temas/drogas-5933/",
        "erc": "https://www.elconfidencial.com/tags/organismos/esquerra-republicana-de-catalunya-erc-2560/",
        "franquismo": "https://www.elconfidencial.com/tags/personajes/francisco-franco-7351/",
        "guerra-ucrania": "https://www.elconfidencial.com/tags/temas/conflicto-de-ucrania-10136/",
        "impuestos": "https://www.elconfidencial.com/tags/temas/impuestos-5303/",
        "independentismo": "https://www.elconfidencial.com/tags/otros/independentismo-6955/",
        "inmigracion": "https://www.elconfidencial.com/tags/otros/inmigracion-7550/",
        "iu": "https://www.elconfidencial.com/tags/organismos/izquierda-unida-2547/",
        "junts": "https://www.elconfidencial.com/tags/organismos/junts-per-catalunya-19613/",
        "pnv": "https://www.elconfidencial.com/tags/organismos/pnv-5779/",
        "podemos": "https://www.elconfidencial.com/tags/organismos/unidas-podemos-17822/",
        "pp": "https://www.elconfidencial.com/tags/organismos/partido-popular-pp-3113/",
        "psoe": "https://www.elconfidencial.com/tags/organismos/psoe-7017/",
        "sindicatos": "https://www.elconfidencial.com/tags/organismos/sindicatos-5867/",
        "sumar": "https://www.elconfidencial.com/tags/topics/sumar-21377/",
        "terrorismo": "https://www.elconfidencial.com/tags/otros/terrorismo-5599/",
        "toros": "https://www.elconfidencial.com/tags/personajes/tauromaquia-18326/",
        "vox": "https://www.elconfidencial.com/tags/organismos/vox-9934/",
        "yihadismo": "https://www.elconfidencial.com/tags/organismos/al-qaeda-3347/"
    },
    "publico": {
        "aborto": "https://www.publico.es/tag/aborto",
        "bildu": "https://www.publico.es/tag/eh-bildu",
        "cambio-climatico": "https://www.publico.es/tag/cambio-climatico",
        "casa-real": "https://www.publico.es/tag/casa-real",
        "ciudadanos": "https://www.publico.es/tag/ciudadanos",
        "covid": "https://www.publico.es/tag/covid-19",
        "cristianismo": "https://www.publico.es/tag/cristianismo",
        "drogas": "https://www.publico.es/tag/drogas",
        "erc": "https://www.publico.es/tag/erc",
        "franquismo": "https://www.publico.es/tag/franquismo",
        "guerra-ucrania": "https://www.publico.es/tag/guerra-rusia-ucrania",
        "impuestos": "https://www.publico.es/tag/impuestos",
        "independentismo": "https://www.publico.es/tag/independentismo",
        "inmigracion": "https://www.publico.es/tag/migrantes",
        "iu": "https://www.publico.es/tag/izquierda-unida",
        "junts": "https://www.publico.es/tag/junts-per-catalunya",
        "pnv": "https://www.publico.es/tag/pnv",
        "podemos": "https://www.publico.es/tag/podemos",
        "pp": "https://www.publico.es/tag/partido-popular",
        "psoe": "https://www.publico.es/tag/psoe",
        "sindicatos": "https://www.publico.es/tag/sindicatos",
        "terrorismo": "https://www.publico.es/tag/terrorismo",
        "toros": "https://www.publico.es/tag/toros",
        "vox": "https://www.publico.es/tag/vox",
        "yihadismo": "https://www.publico.es/tag/yihadismo"
    },

    "lavanguardia": {
        "aborto": None,
        "bildu": "https://www.lavanguardia.com/topics/eh-bildu",
        "cambio-climatico": "https://www.lavanguardia.com/natural/cambio-climatico",
        "casa-real": None,
        "ciudadanos": "https://www.lavanguardia.com/topics/ciudadanos",
        "covid": None,
        "cristianismo": None,
        "drogas": None,
        "erc": "https://www.lavanguardia.com/topics/erc",
        "franquismo": "https://www.lavanguardia.com/topics/francisco-franco",
        "guerra-ucrania": "https://www.lavanguardia.com/temas/guerra-ucrania",
        "impuestos": None,
        "independentismo": None,
        "inmigracion": None,
        "iu": None,
        "junts": None,
        "pnv": "https://www.lavanguardia.com/topics/pnv",
        "podemos": "https://www.lavanguardia.com/topics/podemos",
        "pp": "https://www.lavanguardia.com/topics/partido-popular",
        "psoe": "https://www.lavanguardia.com/topics/psoe",
        "sindicatos": None,
        "terrorismo": None,
        "toros": "https://www.lavanguardia.com/topics/toros",
        "vox": "https://www.lavanguardia.com/topics/vox",
        "yihadismo": "https://www.lavanguardia.com/topics/estado-islamico"
    },


    "eldiario": {
        "aborto": None,
        "bildu": None,
        "cambio-climatico": None,
        "casa-real": None,
        "ciudadanos": None,
        "covid": None,
        "cristianismo": None,
        "drogas": None,
        "erc": None,
        "franquismo": None,
        "guerra-ucrania": None,
        "impuestos": None,
        "independentismo": None,
        "inmigracion": None,
        "iu": None,
        "junts": None,
        "pnv": None,
        "podemos": None,
        "pp": None,
        "psoe": None,
        "sindicatos": None,
        "terrorismo": None,
        "toros": None,
        "vox": None,
        "yihadismo": None
    },
    
    "lanuevaespana": {
        "aborto": "https://www.lne.es/tags/aborto/",
        "bildu": "https://www.lne.es/tags/eh-bildu/",
        "cambio-climatico": "https://www.lne.es/tags/cambio-climatico/",
        "casa-real": "https://www.lne.es/tags/casa-real/",
        "ciudadanos": "https://www.lne.es/tags/ciudadanos/",
        "covid": "https://www.lne.es/tags/covid-19/",
        "cristianismo": "https://www.lne.es/tags/cristianismo/",
        "drogas": "https://www.lne.es/tags/drogas/",
        "erc": "https://www.lne.es/tags/erc/",
        "franquismo": "https://www.lne.es/tags/franquismo/",
        "guerra-ucrania": "https://www.lne.es/tags/guerra-en-ucrania/",
        "impuestos": "https://www.lne.es/tags/impuestos/",
        "independentismo": "https://www.lne.es/tags/independentismo/",
        "inmigracion": "https://www.lne.es/tags/inmigracion/",
        "iu": "https://www.lne.es/tags/iu/",
        "junts": "https://www.lne.es/tags/junts/",
        "pnv": "https://www.lne.es/tags/pnv/",
        "podemos": "https://www.lne.es/tags/podemos/",
        "pp": "https://www.lne.es/tags/pp/",
        "psoe": "https://www.lavanguardia.com/topics/psoe",
        "sindicatos": "https://www.lne.es/tags/sindicatos/",
        "terrorismo": "https://www.lne.es/tags/terrorismo/",
        "toros": "https://www.lne.es/tags/toros/",
        "vox": "https://www.lne.es/tags/vox/",
        "yihadismo": "https://www.lne.es/tags/yihadismo/"
    },
    
    "lavozdeasturias": {
        "aborto": "https://www.lavozdeasturias.es/temas/aborto/",
        "bildu": "https://www.lavozdeasturias.es/temas/bildu/",
        "cambio-climatico": "https://www.lavozdeasturias.es/temas/cambio-climatico/",
        "casa-real": "https://www.lavozdeasturias.es/temas/casa-real/",
        "ciudadanos": "https://www.lavozdeasturias.es/temas/ciudadanos/",
        "covid": "https://www.lavozdeasturias.es/temas/covid-19/",
        "cristianismo": "https://www.lavozdeasturias.es/temas/iglesia-catolica/",
        "drogas": None,
        "erc": "https://www.lavozdeasturias.es/temas/erc/",
        "franquismo": "https://www.lavozdeasturias.es/temas/francisco-franco/",
        "guerra-ucrania": "https://www.lavozdeasturias.es/temas/guerra-en-ucrania/",
        "impuestos": "https://www.lavozdeasturias.es/temas/impuestos/",
        "independentismo": "https://www.lavozdeasturias.es/temas/desafio-secesionista/",
        "inmigracion": "https://www.lavozdeasturias.es/temas/inmigracion/",
        "iu": "https://www.lavozdeasturias.es/temas/iu/",
        "junts": "https://www.lavozdeasturias.es/temas/junts/",
        "pnv": "https://www.lavozdeasturias.es/temas/pnv/",
        "podemos": "https://www.lavozdeasturias.es/temas/podemos/",
        "pp": "https://www.lavozdeasturias.es/temas/pp/",
        "psoe": "https://www.lavozdeasturias.es/temas/psoe/",
        "sindicatos": "https://www.lavozdeasturias.es/temas/ugt/",
        "terrorismo": "https://www.lavozdeasturias.es/temas/terrorismo/",
        "toros": None,
        "vox": "https://www.lavozdeasturias.es/temas/vox/",
        "yihadismo": "https://www.lavozdeasturias.es/temas/estado-islamico/"
    },

    "elpais": {
        "aborto": "https://elpais.com/noticias/aborto/",
        "bildu": "https://elpais.com/noticias/bildu/",
        "cambio-climatico": "https://elpais.com/noticias/cambio-climatico/",
        "casa-real": "https://elpais.com/noticias/casa-real/",
        "ciudadanos": "https://elpais.com/noticias/cs-ciudadanos-partido-de-la-ciudadania/",
        "covid": "https://elpais.com/noticias/covid-19/",
        "cristianismo": "https://elpais.com/noticias/cristianismo/",
        "drogas": "https://elpais.com/noticias/drogas/",
        "erc": "https://elpais.com/noticias/erc-esquerra-republicana-catalunya/",
        "franquismo": "https://elpais.com/noticias/franquismo/",
        "guerra-ucrania": "https://elpais.com/noticias/ofensiva-rusia-ucrania/",
        "impuestos": "https://elpais.com/noticias/impuestos/",
        "independentismo": "https://elpais.com/noticias/independentismo/",
        "inmigracion": "https://elpais.com/noticias/inmigracion/",
        "iu": "https://elpais.com/noticias/iu-izquierda-unida/",
        "junts": "https://elpais.com/noticias/juntsxcat-junts-per-catalunya/",
        "pnv": "https://elpais.com/noticias/pnv-partido-nacionalista-vasco/",
        "podemos": "https://elpais.com/noticias/podemos/",
        "pp": "https://elpais.com/noticias/pp-partido-popular/",
        "psoe": "https://elpais.com/noticias/psoe-partido-socialista-obrero-espanol/",
        "sindicatos": "https://elpais.com/noticias/sindicatos/",
        "terrorismo": "https://elpais.com/noticias/terrorismo/",
        "toros": "https://elpais.com/noticias/toros/",
        "vox": "https://elpais.com/noticias/vox-espana/",
        "yihadismo": "https://elpais.com/noticias/yihad/"
    },


    "elespanol": {
        "aborto": "https://www.elespanol.com/temas/aborto/",
        "bildu": "https://www.elespanol.com/temas/bildu/",
        "cambio-climatico": "https://www.elespanol.com/temas/cambio_climatico/",
        "casa-real": "https://www.elespanol.com/temas/casa_real/",
        "ciudadanos": "https://www.elespanol.com/organismos/ciudadanos_partido_politico/",
        "covid": "https://www.elespanol.com/temas/covid_19/",
        "cristianismo": "https://www.elespanol.com/temas/cristianismo/",
        "drogas": "https://www.elespanol.com/temas/drogas/",
        "erc": "https://www.elespanol.com/temas/erc/",
        "franquismo": "https://www.elespanol.com/temas/franquismo/",
        "guerra-ucrania": "https://www.elespanol.com/temas/guerra_rusia_ucrania/",
        "impuestos": "https://www.elespanol.com/temas/impuestos/",
        "independentismo": "https://www.elespanol.com/temas/independentismo/",
        "inmigracion": "https://www.elespanol.com/temas/inmigracion/",
        "iu": "https://www.elespanol.com/organismos/iu/",
        "junts": "https://www.elespanol.com/temas/junts/",
        "pnv": "https://www.elespanol.com/organismos/pnv/",
        "podemos": "https://www.elespanol.com/organismos/pnv/",
        "pp": "https://www.elespanol.com/organismos/pp_partido_popular/",
        "psoe": "https://www.elespanol.com/organismos/psoe/",
        "sindicatos": "https://www.elespanol.com/temas/sindicatos/",
        "terrorismo": "https://www.elespanol.com/temas/terrorismo/",
        "toros": "https://www.elespanol.com/temas/tauromaquia/",
        "vox": "https://www.elespanol.com/organismos/vox_partido_politico/",
        "yihadismo": "https://www.elespanol.com/temas/yihadismo/"
    },


    "elmundo": {
        "aborto": "https://www.elmundo.es/t/ab/aborto.html",
        "bildu": "https://www.elmundo.es/e/bi/bildu.html",
        "cambio-climatico": "https://www.elmundo.es/t/ca/cambio-climatico.html",
        "casa-real": "https://www.elmundo.es/e/ca/casa-real.html",
        "ciudadanos": "https://elmundo.es/e/cs/cs-ciudadanos.html",
        "covid": "https://www.elmundo.es/ciencia-y-salud/salud/covid-19.html",
        "cristianismo": "https://www.elmundo.es/t/re/religion.html",
        "drogas": "https://www.elmundo.es/t/dr/drogas.html",
        "erc": "https://www.elmundo.es/e/er/erc-esquerra-republicana.html",
        "franquismo": "https://www.elmundo.es/e/fr/francisco-franco.html",
        "guerra-ucrania": "https://www.elmundo.es/internacional/guerra-ucrania-rusia.html",
        "impuestos": "https://www.elmundo.es/t/im/impuestos.html",
        "independentismo": "https://www.elmundo.es/t/in/independencia-catalunya.html",
        "inmigracion": "https://www.elmundo.es/t/in/inmigracion.html",
        "iu": "https://www.elmundo.es/e/iu/iu-izquierda-unida.html",
        "junts": "https://www.elmundo.es/e/ju/junts-per-catalunya.html",
        "pnv": "https://www.elmundo.es/e/pn/pnv-partido-nacionalista-vasco.html",
        "podemos": "https://www.elmundo.es/e/po/podemos.html",
        "pp": "https://www.elmundo.es/e/pp/pp-partido-popular.html",
        "psoe": "https://www.elmundo.es/e/ps/psoe-partido-socialista-obrero-espanol.html",
        "sindicatos": "https://www.elmundo.es/e/ug/ugt.html",
        "terrorismo": "https://www.elmundo.es/t/te/terrorismo.html",
        "toros": "https://www.elmundo.es/cultura/toros.html",
        "vox": "https://www.elmundo.es/e/vo/vox.html",
        "yihadismo": "https://www.elmundo.es/t/yi/yihadismo.html"
    },


    "larazon": {
        "aborto": "https://www.larazon.es/tags/aborto/",
        "bildu": "https://www.larazon.es/tags/bildu/",
        "cambio-climatico": "https://www.larazon.es/tags/cambio-climatico/",
        "casa-real": "https://www.larazon.es/tags/casa-real/",
        "ciudadanos": "https://www.larazon.es/tags/ciudadanos/",
        "covid": "https://www.larazon.es/tags/covid-19/",
        "cristianismo": "https://www.larazon.es/tags/cristianismo/",
        "drogas": "https://www.larazon.es/tags/drogas/",
        "erc": "https://www.larazon.es/tags/erc/",
        "franquismo": "https://www.larazon.es/tags/franquismo/",
        "guerra-ucrania": "https://www.larazon.es/tags/guerra-en-ucrania/",
        "impuestos": "https://www.larazon.es/tags/impuestos/",
        "independentismo": "https://www.larazon.es/tags/independentismo/",
        "inmigracion": "https://www.larazon.es/tags/inmigracion/",
        "iu": "https://www.larazon.es/tags/iu/",
        "junts": "https://www.larazon.es/tags/juntsxcat/",
        "pnv": "https://www.larazon.es/tags/pnv/",
        "podemos": "https://www.larazon.es/tags/podemos/",
        "pp": "https://www.larazon.es/tags/pp/",
        "psoe": "https://www.larazon.es/tags/psoe/",
        "sindicatos": "https://www.larazon.es/tags/sindicatos/",
        "terrorismo": "https://www.larazon.es/tags/terrorismo/",
        "toros": "https://www.larazon.es/tags/toros/",
        "vox": "https://www.larazon.es/tags/vox/",
        "yihadismo": "https://www.larazon.es/tags/yihadismo/"
    },


    "elcomercio": {
        "aborto": "https://www.elcomercio.es/temas/generales/aborto.html",
        "bildu": "https://www.elcomercio.es/temas/entidades/eh-bildu.html",
        "cambio-climatico": "https://www.elcomercio.es/temas/generales/cambio-climatico.html",
        "casa-real": "https://www.elcomercio.es/temas/entidades/casa-real.html",
        "ciudadanos": "https://www.elcomercio.es/temas/entidades/ciudadanos-partido-de-la-ciudadania.html",
        "covid": "https://www.elcomercio.es/temas/generales/covid-19.html",
        "cristianismo": "https://www.elcomercio.es/temas/entidades/iglesia-catolica.html",
        "drogas": "https://www.elcomercio.es/temas/generales/droga.html",
        "erc": "https://www.elcomercio.es/temas/entidades/erc-esquerra-republicana-de-catalunya.html",
        "franquismo": "https://www.elcomercio.es/temas/personajes/francisco-franco-bahamonde.html",
        "guerra-ucrania": "https://www.elcomercio.es/temas/generales/guerra-en-ucrania.html",
        "impuestos": "https://www.elcomercio.es/economia/fiscalidad/",
        "independentismo": "https://www.elcomercio.es/temas/generales/proces-de-independencia-de-cataluna.html",
        "inmigracion": "https://www.elcomercio.es/temas/generales/migrantes.html",
        "iu": "https://www.elcomercio.es/temas/entidades/iu-izquierda-unida.html",
        "junts": "https://www.elcomercio.es/temas/entidades/junts-per-catalunya.html",
        "pnv": "https://www.elcomercio.es/temas/entidades/pnv-partido-nacionalista-vasco.html",
        "podemos": "https://www.elcomercio.es/temas/entidades/podemos.html",
        "pp": "https://www.elcomercio.es/temas/entidades/pp-partido-popular.html",
        "psoe": "https://www.elcomercio.es/temas/entidades/psoe-partido-socialista-obrero-espanol.html",
        "sindicatos": "https://www.elcomercio.es/temas/entidades/ugt-union-general-de-trabajadores.html",
        "terrorismo": None,
        "toros": "https://www.elcomercio.es/temas/generales/toros.html",
        "vox": "https://www.elcomercio.es/temas/entidades/vox.html",
        "yihadismo": "https://www.elcomercio.es/temas/generales/yihadismo.html"
    },


    "abc": {
        "aborto": "https://www.abc.es/sociedad/aborto/",
        "bildu": "https://www.abc.es/espana/partidos-politicos/eh-bildu/",
        "cambio-climatico": "https://www.abc.es/natural/cambio-climatico/",
        "casa-real": "https://www.abc.es/temas/casa-real/",
        "ciudadanos": "https://www.abc.es/espana/partidos-politicos/ciudadanos-partido-de-la-ciudadania/",
        "covid": "https://www.abc.es/salud/enfermedades/covid-19/",
        "cristianismo": "https://www.abc.es/sociedad/religion/cristianismo/",
        "drogas": "https://www.abc.es/salud/drogas/",
        "erc": "https://www.abc.es/espana/partidos-politicos/esquerra-republicana/",
        "franquismo": "https://www.abc.es/historia/personajes/francisco-franco/",
        "guerra-ucrania": "https://www.abc.es/internacional/guerra-ucrania-rusia/",
        "impuestos": "https://www.abc.es/economia/impuestos/",
        "independentismo": "https://www.abc.es/espana/independentismo/",
        "inmigracion": "https://www.abc.es/espana/inmigracion/",
        "iu": "https://www.abc.es/espana/partidos-politicos/iu-izquierda-unida/",
        "junts": "https://www.abc.es/espana/partidos-politicos/junts-per-catalunya/",
        "pnv": "https://www.abc.es/espana/partidos-politicos/pnv-partido-nacionalista-vasco/",
        "podemos": "https://www.abc.es/espana/partidos-politicos/podemos/",
        "pp": "https://www.abc.es/espana/partidos-politicos/pp-partido-popular/",
        "psoe": "https://www.abc.es/espana/partidos-politicos/psoe/",
        "sindicatos": "https://www.abc.es/economia/sindicatos/",
        "terrorismo": "https://www.abc.es/temas/terrorismo/",
        "toros": "https://www.abc.es/temas/tauromaquia/",
        "vox": "https://www.abc.es/espana/partidos-politicos/vox/",
        "yihadismo": "https://www.abc.es/internacional/terrorismo/yihad-islamica/"
    },
}

articleRules = {
    "elconfidencial": Rule(LinkExtractor(allow=r"^https://www\.elconfidencial\.com", deny=r"^elconfidencial\.com/tags"), callback="parse_elconfidencial"),

    "publico": Rule(LinkExtractor(allow=r"^https://www\.publico\.es", deny=[r"publico\.es/podcasts/", r"publico\.es/public/", r"publico\.es/tag"]), callback="parse_publico"),

    "lavanguardia": Rule(LinkExtractor(allow=r"^https://www\.lavanguardia\.com", deny=r"lavanguardia\.com/topics"), callback="parse_lavanguardia"),

    "eldiario": Rule(LinkExtractor(allow=r"^https://www\.eldiario\.es", deny=[r"eldiario\.es/cuadernos/"]), callback="parse_eldiario"),

    "lanuevaespana": Rule(LinkExtractor(allow=r"^https://www\.lne\.es", deny=[r"lne\.es/asturias/n-asturianu/", r"lne\.es/tags"]), callback="parse_lanuevaespana"),

    "lavozdeasturias": Rule(LinkExtractor(allow=r"^https://www\.lavozdeasturias\.es", deny=[r"lavozdeasturias\.es/publicaciones/", r"lavozdeasturias\.es/noticia/agora/", r"lavozdeasturias\.es/temas"]), callback="parse_lavozdeasturias"),

    "elpais": Rule(LinkExtractor(allow=r"^https://elpais\.com", deny=r"elpais\.com/cat/"), callback="parse_elpais"),

    "elespanol": Rule(LinkExtractor(allow=r"^https://www\.elespanol\.com", deny = [r"elespanol\.com/temas/", r"elespanol\.com/organismos/"]), callback="parse_elespanol"),

    "elmundo": Rule(LinkExtractor(allow=r"^https://www\.elmundo\.es", deny=[r"elmundo\.es/papel/", r"elmundo\.es/magazine/", r"elmundo\.es/elmundo", r"elmundo\.es/elmundo", r"elmundo\.es/e/", r"elmundo\.es/t/"]), callback="parse_elmundo"),

    "larazon": Rule(LinkExtractor(allow=r"^https://www\.larazon\.es", deny=r"larazon\.es/tags"), callback="parse_larazon"),

    "elcomercio": Rule(LinkExtractor(allow=r"^https://www\.elcomercio\.es", deny=[r"elcomercio\.es/gastronomia/recetas/", r"elcomercio\.es/extras/"]), callback="parse_elcomercio"),

    "abc": Rule(LinkExtractor(allow=r"^https://www\.abc\.es", deny=[r"abc\.es/voz/", r"abc\.es/archivo/"]), callback="parse_abc")
}

domains = {
    "elconfidencial": "elconfidencial.com",
    "publico": "publico.es",
    "lavanguardia": "lavanguardia.com",
    "eldiario": "eldiario.es",
    "lanuevaespana": "lne.es",
    "lavozdeasturias": "lavozdeasturias.es",
    "elpais": "elpais.com",
    "elespanol": "elespanol.com",
    "elmundo": "elmundo.es",
    "larazon": "larazon.es",
    "elcomercio": "elcomercio.es",
    "abc": "abc.es"
}

downloadDelay = {
    "elconfidencial": 0,
    "publico": 0,
    "lavanguardia": 0,
    "eldiario": 0,
    "lanuevaespana": 0,
    "lavozdeasturias": 0,
    "elpais": 0,
    "elespanol": 0,
    "elmundo": 0,
    "larazon": 0,
    "elcomercio": 0,
    "abc": 0
}

class ArticleItem(Item):
    responsedatetime = Field()
    source = Field()
    url = Field()
    datetime = Field()
    title = Field()
    author = Field()
    text = Field()
    categories = Field()

class NoticiasSpider(CrawlSpider):
    name = "noticias"

    def __init__(self, sources=None, categories=None, items=None, **kwargs):
        self.start_urls = []
        self.allowed_domains = []
        self.rules = []

        if sources is None:
            sources = categoryURLs.keys()
        else:
            sources = sources.split(",")
        
        if categories is None:
            categories = categoryURLs[sources[0]].keys()
        else:
            categories = categories.split(",")
        
        for source in sources:
            self.allowed_domains.append(domains[source])
            for category in categories:
                if categoryURLs[source][category] is None:
                    continue
                categoryRuleURL = categoryURLs[source][category].replace(".html", "").replace(".", "\\.")
                self.start_urls.append(categoryURLs[source][category])
                self.rules.append(Rule(LinkExtractor(allow=f"^{categoryRuleURL}"), follow=True))
                self.rules.append(articleRules[source])

        self.custom_settings = {
            "DEFAULT_REQUEST_HEADERS": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                "Accept-Language": "es-ES,es;q=0.9",
                #"Referer": "https://www.google.es/",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Encoding": "gzip, deflate",
                #"Sec-Ch-Ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
                #"Sec-Fetch-Mode": "navigate",
                #"Sec-Fetch-Site": "none",
                #"Sec-Fetch-Dest": "document",
                #"Sec-Ch-Ua-Mobile": "?0",
                "Upgrade-Insecure-Requests": "1",
                #"Sec-Ch-Ua-Platform": "\"Windows\""
            }
        }

        if items is not None:
            self.custom_settings["CLOSESPIDER_ITEMCOUNT"] = int(items)
        
        self.custom_settings["DOWNLOAD_DELAY"] = np.max([downloadDelay[source] for source in sources])

        super().__init__(**kwargs)

    def processText(self, paragraphs):
        body = [re.sub(r"<.+?>", "", paragraph).strip(" \ufeff\xa0\n\t\r") for paragraph in paragraphs]
        text = "\n\n".join(body)
        text = text.replace("\xa0", " ")
        text = text.replace("\ufeff", "")
        text = re.sub(r"<br(?: ?/)?>", "\n\n", text)
        text = re.sub(r"[\n]{3,}", "\n\n", text)
        text = re.sub(r" {2,}", " ", text)
        text = re.sub(r"^[ \n]+$", "", text)

        return text

    def stripIfNotNone(self, var):
        if var is None:
            return None
        else:
            return var.strip(" \ufeff\xa0\n\t\r")
    
    def parse_elmundo(self, response):
        if response.xpath("//div[@class='ue-c-article__premium']").get() is not None:
            return
        
        item = ArticleItem()

        item["responsedatetime"] = datetime.now(zoneinfo.ZoneInfo("Europe/Madrid")).replace(microsecond=0)
        item["source"] = "El Mundo"
        item["url"] = response.url
        item["title"] = self.stripIfNotNone(response.xpath("//h1[contains(@class,'ue-c-article__headline')]/text()").get())
        item["author"] = self.stripIfNotNone(response.xpath("//div[@class='ue-c-article__author-name-item']/a/text()").get())

        categories = [self.stripIfNotNone(category) for category in response.xpath("//li[@class='ue-c-article__tags-item']/a/text()").getall()]
        if categories == []:
            item["categories"] = None
        else:
            item["categories"] = categories

        date = response.xpath("//time/@datetime").get()
        if date != None:
            try:
                date = datetime.fromisoformat(date)
                date = date.astimezone(zoneinfo.ZoneInfo("Europe/Madrid"))
            except:
                date = None
        item["datetime"] = date

        body = response.xpath("//div[contains(@class,'ue-c-article__body')]/p").getall()
        item["text"] = self.processText(body)

        if item["text"] != "" and item["title"] != None and item["datetime"] != None and item["categories"] != None:
            return item

    def parse_lavanguardia(self, response):
        item = ArticleItem()

        item["responsedatetime"] = datetime.now(zoneinfo.ZoneInfo("Europe/Madrid")).replace(microsecond=0)
        item["source"] = "La Vanguardia"
        item["url"] = response.url
        item["title"] = self.stripIfNotNone(response.xpath("//h1[@class='title']/text()").get())
        item["author"] = self.stripIfNotNone(response.xpath("//div[@class='article-author-name']/text()").get())

        categories = [self.stripIfNotNone(category) for category in response.xpath("//a[contains(@class, 'tag-name')]/text()").getall()]
        if categories == []:
            item["categories"] = None
        else:
            item["categories"] = categories

        date = response.xpath("//time[@class='created']/@datetime").get()
        if date != None:
            try:
                date = datetime.fromisoformat(date)
                date = date.astimezone(zoneinfo.ZoneInfo("Europe/Madrid"))
            except:
                date = None
        item["datetime"] = date
        
        body = response.xpath("//p[@class='paragraph']").getall()
        item["text"] = self.processText(body)

        if item["text"] != "" and item["title"] != None and item["datetime"] != None and item["categories"] != None:
            return item

    def parse_elpais(self, response):
        if response.xpath("//*[id='ctn_premium_article']").get() is not None or response.xpath("//*[id='ctn_freemium_article']").get() is not None:
            return
        
        item = ArticleItem()

        item["responsedatetime"] = datetime.now(zoneinfo.ZoneInfo("Europe/Madrid")).replace(microsecond=0)
        item["source"] = "El País"
        item["url"] = response.url
        item["title"] = self.stripIfNotNone(response.xpath("//h1[@class='a_t']/text()").get())
        item["author"] = self.stripIfNotNone(response.xpath("//div[@class='a_md_a']/a/text()").get())
        
        categories = [self.stripIfNotNone(category) for category in response.xpath("//ul[contains(@class, 'w_ul')]/li/a/text()").getall()]
        if categories == []:
            item["categories"] = None
        else:
            item["categories"] = categories
        
        date = response.xpath("(//div[contains(@class, 'a_md_f')]/span)[1]/time/a/@data-date").get()
        if date != None:
            try:
                date = datetime.fromisoformat(date)
                date = date.astimezone(zoneinfo.ZoneInfo("Europe/Madrid"))
            except:
                date = None
        item["datetime"] = date

        body = response.xpath("//p[@class]").getall()
        item["text"] = self.processText(body)

        if item["text"] != "" and item["title"] != None and item["datetime"] != None and item["categories"] != None:
            return item
    
    def parse_abc(self, response):
        if response.xpath("//div[@class='voc-paywall-notice']").get() is not None:
            return
        
        item = ArticleItem()

        item["responsedatetime"] = datetime.now(zoneinfo.ZoneInfo("Europe/Madrid")).replace(microsecond=0)
        item["source"] = "ABC"
        item["url"] = response.url
        item["title"] = self.stripIfNotNone(response.xpath("//h1[@class='voc-title']/text()").get())

        categories = [self.stripIfNotNone(category) for category in response.xpath("//a[@class='voc-topics__link']/text()").getall()]
        if categories == []:
            item["categories"] = None
        else:
            item["categories"] = categories

        item["author"] = self.stripIfNotNone(response.xpath("//p[@class='voc-author__name']/a/text()").get())

        date = response.xpath("//time[@class='voc-author__time']/@datetime").get()
        if date != None:
            try:
                date = datetime.fromisoformat(date)
                date = date.astimezone(zoneinfo.ZoneInfo("Europe/Madrid"))
            except:
                date = None
        item["datetime"] = date

        body = response.xpath("//p[@class='voc-p']").getall()
        item["text"] = self.processText(body)

        if item["text"] != "" and item["title"] != None and item["datetime"] != None and item["categories"] != None:
            return item
    
    def parse_eldiario(self, response):
        if response.xpath("//div[@class='paywall__wrapper']").get() is not None:
            return
        
        item = ArticleItem()

        item["responsedatetime"] = datetime.now(zoneinfo.ZoneInfo("Europe/Madrid")).replace(microsecond=0)
        item["source"] = "El Diario"
        item["url"] = response.url
        item["title"] = self.stripIfNotNone(response.xpath("//h1[@class='title']/text()").get())
        item["author"] = self.stripIfNotNone(response.xpath("//p[@class='authors']/a/text()").get())

        categories = [self.stripIfNotNone(category) for category in response.xpath("//a[@class='tag-link']/text()").getall()]
        if categories == []:
            item["categories"] = None
        else:
            item["categories"] = categories

        date = response.xpath("//time[@class='date']/@datetime").get()
        if date != None:
            try:
                date = datetime.fromisoformat(date)
                date = date.astimezone(zoneinfo.ZoneInfo("Europe/Madrid"))
            except:
                date = None
        item["datetime"] = date

        body = response.xpath("//p[@class='article-text']").getall()
        item["text"] = self.processText(body)

        if item["text"] != "" and item["title"] != None and item["datetime"] != None and item["categories"] != None:
            return item
    
    def parse_larazon(self, response):
        item = ArticleItem()

        item["responsedatetime"] = datetime.now(zoneinfo.ZoneInfo("Europe/Madrid")).replace(microsecond=0)
        item["source"] = "La Razón"
        item["url"] = response.url
        item["title"] = self.stripIfNotNone(response.xpath("//h1[@class='article-main__title']/text()").get())
        item["author"] = self.stripIfNotNone(response.xpath("//div[@class='article-author__name']/ul/li/a/text()").get())

        categories = [self.stripIfNotNone(category) for category in response.xpath("//a[@class='tags-list__link']/text()").getall()]
        if categories == []:
            item["categories"] = None
        else:
            item["categories"] = categories

        date = response.xpath("(//div[@class='article-dates']/div)[1]/time/@datetime").get()
        if date != None:
            try:
                date = datetime.fromisoformat(date)
                date = date.astimezone(zoneinfo.ZoneInfo("Europe/Madrid"))
            except:
                date = None
        item["datetime"] = date

        body = response.xpath("//div[@class='article-main__content']/p").getall()
        item["text"] = self.processText(body)

        if item["text"] != "" and item["title"] != None and item["datetime"] != None and item["categories"] != None:
            return item
    
    def parse_elconfidencial(self, response):
        if response.xpath("//div[@class='EC_payWall']").get() is not None:
            return
        
        item = ArticleItem()

        item["responsedatetime"] = datetime.now(zoneinfo.ZoneInfo("Europe/Madrid")).replace(microsecond=0)
        item["source"] = "El Confidencial"
        item["url"] = response.url
        item["title"] = self.stripIfNotNone(response.xpath("//h1[contains(@class, 'title')]/text()").get())
        item["author"] = self.stripIfNotNone(response.xpath("//a[@class='authorSignature__link']/text()").get())
        
        categories = [self.stripIfNotNone(category) for category in response.xpath("//span[@class='editorialTags__name']/text()").getall()]
        if categories == []:
            item["categories"] = None
        else:
            item["categories"] = categories
        
        date = response.xpath("//div[@class='dateTime']/time/@datetime").get()
        if date != None:
            try:
                date = datetime.fromisoformat(date)
                date = date.astimezone(zoneinfo.ZoneInfo("Europe/Madrid"))
            except:
                date = None
        item["datetime"] = date

        body = response.xpath("//div[@id='news-body-cc']/p").getall()
        item["text"] = self.processText(body)

        if item["text"] != "" and item["title"] != None and item["datetime"] != None and item["categories"] != None:
            return item
    
    def parse_publico(self, response):
        item = ArticleItem()

        item["responsedatetime"] = datetime.now(zoneinfo.ZoneInfo("Europe/Madrid")).replace(microsecond=0)
        item["source"] = "Público"
        item["url"] = response.url
        item["title"] = self.stripIfNotNone(response.xpath("//div[contains(@class, 'article-header-title')]/h1/text()").get())
        item["author"] = self.stripIfNotNone(response.xpath("(//p[@class='signature']/a)[1]/text()").get())

        categories = [self.stripIfNotNone(category) for category in response.xpath("//div[@class='article-tags']/ul/li/a/text()").getall()]
        if categories == []:
            item["categories"] = None
        else:
            item["categories"] = categories

        date = response.xpath("//span[@class='published']/@data-timestamp").get()
        if date != None:
            try:
                date = datetime.fromtimestamp(int(date))
                date = date.astimezone(zoneinfo.ZoneInfo("Europe/Madrid"))
            except:
                date = None
        item["datetime"] = date

        body = response.xpath("//div[@class='article-text']/p").getall()
        item["text"] = self.processText(body)

        if item["text"] != "" and item["title"] != None and item["datetime"] != None and item["categories"] != None:
            return item
    
    def parse_elespanol(self, response):
        locale.setlocale(locale.LC_TIME, "es_ES")

        if response.xpath("//div[@class='content-not-granted-paywall']").get() is not None:
            return
        
        item = ArticleItem()

        item["responsedatetime"] = datetime.now(zoneinfo.ZoneInfo("Europe/Madrid"))
        item["source"] = "El Español"
        item["url"] = response.url
        item["title"] = self.stripIfNotNone(response.xpath("//h1[contains(@class, 'article-header__heading')]/text()").get())
        item["author"] = self.stripIfNotNone(response.xpath("//span[@class='address__author']/a/text()").get())

        categories = [self.stripIfNotNone(category) for category in response.xpath("//li[@class='tags__list-item']/a/text()").getall()]
        if categories == []:
            item["categories"] = None
        else:
            item["categories"] = categories

        date = self.stripIfNotNone(response.xpath("//span[contains(@class, 'article-header__time-date')]/text()").get())
        time = self.stripIfNotNone(response.xpath("//span[contains(@class, 'article-header__time-hour')]/text()").get())
        if date != None and time != None:
            try:
                articledatetime = datetime.strptime(date + " " + time, "%d %B, %Y %H:%M")
                articledatetime.replace(tzinfo=zoneinfo.ZoneInfo("Europe/Madrid"))
                item["datetime"] = articledatetime
            except:
                item["datetime"] = None
        else:
            item["datetime"] = None

        body = response.xpath("//div[@class='article-body__content']/p").getall()
        item["text"] = self.processText(body)

        if item["text"] != "" and item["title"] != None and item["datetime"] != None and item["categories"] != None:
            return item
    
    def parse_lanuevaespana(self, response):
        if response.xpath("//div[@id='paywall']").get() is not None:
            return
        
        item = ArticleItem()

        item["responsedatetime"] = datetime.now(zoneinfo.ZoneInfo("Europe/Madrid"))
        item["source"] = "La Nueva España"
        item["url"] = response.url
        item["title"] = self.stripIfNotNone(response.xpath("//h1[contains(@class, 'ft-title')]/text()").get())
        item["author"] = self.stripIfNotNone(response.xpath("//div[@class='ft-mol-writer__title']/p/text()").get())

        categories = [self.stripIfNotNone(category) for category in response.xpath("//li[contains(@class, 'ft-tag')]/a/text()").getall()]
        if categories == []:
            item["categories"] = None
        else:
            item["categories"] = categories

        date = response.xpath("(//time[@class='ft-date__text'])[1]/@datetime").get()
        if date != None:
            try:
                date = datetime.fromisoformat(date)
                date = date.astimezone(zoneinfo.ZoneInfo("Europe/Madrid"))
            except:
                date = None
        item["datetime"] = date

        body = response.xpath("//p[@class='ft-text']").getall()
        item["text"] = self.processText(body)

        if item["text"] != "" and item["title"] != None and item["datetime"] != None and item["categories"] != None:
            return item
    
    def parse_elcomercio(self, response):
        if response.xpath("//div[contains(@class, 'content-exclusive-bg')]").get() is not None:
            return
        
        item = ArticleItem()

        item["responsedatetime"] = datetime.now(zoneinfo.ZoneInfo("Europe/Madrid"))
        item["source"] = "El Comercio"
        item["url"] = response.url
        item["title"] = self.stripIfNotNone(response.xpath("//h1[@class='v-a-t']/text()").get())
        item["author"] = self.stripIfNotNone(response.xpath("//p[contains(@class, 'p-mdl-ath__p--2')]/a/text()").get())

        categories = [self.stripIfNotNone(category) for category in response.xpath("//a[contains(@class, 'v-mdl-tpc__a']/text()").getall()]
        if categories == []:
            item["categories"] = None
        else:
            item["categories"] = categories

        date = response.xpath("//p[@class='v-mdl-ath__tm']/@datetime").get()
        if date != None:
            try:
                date = datetime.fromisoformat(date)
                date = date.astimezone(zoneinfo.ZoneInfo("Europe/Madrid"))
            except:
                date = None
        item["datetime"] = date

        body = response.xpath("//p[@class='v-p']").getall()
        item["text"] = self.processText(body)

        if item["text"] != "" and item["title"] != None and item["datetime"] != None and item["categories"] != None:
            return item
    
    def parse_lavozdeasturias(self, response):
        locale.setlocale(locale.LC_TIME, "es_ES")
        
        item = ArticleItem()

        item["responsedatetime"] = datetime.now(zoneinfo.ZoneInfo("Europe/Madrid"))
        item["source"] = "La Voz de Asturias"
        item["url"] = response.url
        item["title"] = self.stripIfNotNone(response.xpath("//h1[contains(@class, 'headline')]/text()").get())
        item["author"] = self.stripIfNotNone(response.xpath("//span[contains(@class, 'author')]/text()").get())

        categories = [self.stripIfNotNone(category) for category in response.xpath("//nav[@class='sz-t-xs']/a[@class='mg-l']/text()").getall()]
        if categories == []:
            item["categories"] = None
        else:
            item["categories"] = categories

        date = self.stripIfNotNone(response.xpath("//div[@class='date']/span/strong/text()").get())
        time = self.stripIfNotNone(response.xpath("//div[@class='date']/span/text()").get())
        if date != None and time != None:
            try:
                articledatetime = datetime.strptime(date[:6] + "." + date[6:] + time, "%d %b %Y. Actualizado a las %H:%M h.")
                articledatetime.replace(tzinfo=zoneinfo.ZoneInfo("Europe/Madrid"))
                item["datetime"] = articledatetime
            except:
                item["datetime"] = None
        else:
            item["datetime"] = None

        body = response.xpath("//div[contains(@class, 'txt-blk')]/p[contains(@class, 'txt')]").getall()
        body = [paragraph for paragraph in body if "<!-- embed article -->" not in paragraph]
        item["text"] = self.processText(body)

        if item["text"] != "" and item["title"] != None and item["datetime"] != None and item["categories"] != None:
            return item
    
    def parse_okdiario(self, response):
        item = ArticleItem()

        item["responsedatetime"] = datetime.now(zoneinfo.ZoneInfo("Europe/Madrid")).replace(microsecond=0)
        item["source"] = "Okdiario"
        item["url"] = response.url
        item["title"] = self.stripIfNotNone(response.xpath("//h1[@class='entry-title']/text()").get())
        item["author"] = self.stripIfNotNone(response.xpath("//li[@class='author-name']/strong/a/text()").get())

        categories = [self.stripIfNotNone(category) for category in response.xpath("//div[@class='topics']/ul/li/a/text()").getall()]
        if categories == []:
            item["categories"] = None
        else:
            item["categories"] = categories

        date = response.xpath("//li[@class='publish-time']/time/@datetime").get()
        if date != None:
            try:
                date = datetime.strptime(date, "%d/%m/%Y %H:%M")
                date = date.replace(tzinfo=zoneinfo.ZoneInfo("Europe/Madrid"))
            except:
                date = None
        item["datetime"] = date

        body = response.xpath("//div[@class='entry-content']/p").getall()
        item["text"] = self.processText(body)

        if item["text"] != "" and item["title"] != None and item["datetime"] != None and item["categories"] != None:
            return item

    def parse_20minutos(self, response):
        item = ArticleItem()

        item["responsedatetime"] = datetime.now(zoneinfo.ZoneInfo("Europe/Madrid")).replace(microsecond=0)
        item["source"] = "20 minutos"
        item["url"] = response.url
        item["title"] = self.stripIfNotNone(response.xpath("//h1[@class='article-title']/text()").get())
        item["author"] = self.stripIfNotNone(response.xpath("//span[@class='article-author']/strong/text()").get())
        item["categories"] = None

        date = self.stripIfNotNone(response.xpath("//span[@class='article-date']/text()").get())
        if date != None:
            try:
                date = datetime.strptime(date, r"%d.%m.%Y - %H:%MH")
                date = date.replace(tzinfo=zoneinfo.ZoneInfo("Europe/Madrid"))
            except:
                date = None
        item["datetime"] = date

        body = response.xpath("//p[@class='paragraph']").getall()
        item["text"] = self.processText(body)

        if item["text"] != "" and item["title"] != None and item["datetime"] != None and item["categories"] != None:
            return item