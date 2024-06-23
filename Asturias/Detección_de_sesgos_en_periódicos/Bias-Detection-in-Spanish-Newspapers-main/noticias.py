from scrapy.item import Item, Field
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

import re
from datetime import datetime
import zoneinfo
import locale

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

    def __init__(self, medio=None, **kwargs):
        self.start_urls = []
        self.allowed_domains = []
        self.rules = []

        if medio is not None:
            medio = medio.split(",")

        if medio is None or "elmundo" in medio:
            self.start_urls.append("https://www.elmundo.es")
            self.allowed_domains.append("elmundo.es")
            self.rules.append(Rule(LinkExtractor(allow=r"^https://www\.elmundo\.es", deny=[r"elmundo\.es/papel/", r"elmundo\.es/magazine/", r"elmundo\.es/elmundo"]), callback="parse_elmundo", follow=True))
        if medio is None or "lavanguardia"in medio:
            self.start_urls.append("https://www.lavanguardia.com")
            self.allowed_domains.append("lavanguardia.com")
            self.rules .append(Rule(LinkExtractor(allow=r"^https://www\.lavanguardia\.com"), callback="parse_lavanguardia", follow=True))
        if medio is None or "elpais" in medio:
            self.start_urls.append("https://elpais.com")
            self.allowed_domains.append("elpais.com")
            self.rules.append(Rule(LinkExtractor(allow=r"^https://elpais\.com", deny=r"elpais\.com/cat/"), callback="parse_elpais", follow=True))
        if medio is None or "abc" in medio:
            self.start_urls.append("https://www.abc.es")
            self.allowed_domains.append("abc.es")
            self.rules.append(Rule(LinkExtractor(allow=r"^https://www\.abc\.es", deny=[r"abc\.es/voz/", r"abc\.es/archivo/"]), callback="parse_abc", follow=True))
        if medio is None or "eldiario" in medio:
            self.start_urls.append("https://www.eldiario.es")
            self.allowed_domains.append("eldiario.es")
            self.rules.append(Rule(LinkExtractor(allow=r"^https://www\.eldiario\.es", deny=[r"eldiario\.es/cuadernos/"]), callback="parse_eldiario", follow=True))
        if medio is None or "larazon" in medio:
            self.start_urls.append("https://www.larazon.es")
            self.allowed_domains.append("larazon.es")
            self.rules.append(Rule(LinkExtractor(allow=r"^https://www\.larazon\.es"), callback="parse_larazon", follow=True))
        if medio is None or "elconfidencial" in medio:
            self.start_urls.append("https://www.elconfidencial.com")
            self.allowed_domains.append("elconfidencial.com")
            self.rules.append(Rule(LinkExtractor(allow=r"^https://www\.elconfidencial\.com"), callback="parse_elconfidencial", follow=True))
        if medio is None or "publico" in medio:
            self.start_urls = ["https://www.publico.es"]
            self.allowed_domains = ["publico.es"]
            self.rules.append(Rule(LinkExtractor(allow=r"^https://www\.publico\.es", deny=[r"publico\.es/podcasts/", r"publico\.es/public/"]), callback="parse_publico", follow=True))
        if medio is None or "elespanol" in medio:
            self.start_urls.append("https://www.elespanol.com")
            self.allowed_domains.append("elespanol.com")
            self.rules.append(Rule(LinkExtractor(allow=r"^https://www\.elespanol\.com"), callback="parse_elespanol", follow=True))
        if medio is None or "lanuevaespana" in medio:
            self.start_urls.append("https://www.lne.es/")
            self.allowed_domains.append("lne.es")
            self.rules.append(Rule(LinkExtractor(allow=r"^https://www\.lne\.es", deny=[r"lne\.es/asturias/n-asturianu/"]), callback="parse_lanuevaespana", follow=True))
        if medio is None or "elcomercio" in medio:
            self.start_urls.append("https://www.elcomercio.es/")
            self.allowed_domains.append("elcomercio.es")
            self.rules.append(Rule(LinkExtractor(allow=r"^https://www\.elcomercio\.es", deny=[r"elcomercio\.es/gastronomia/recetas/", r"elcomercio\.es/extras/"]), callback="parse_elcomercio", follow=True))
        if medio is None or "lavozdeasturias" in medio:
            self.start_urls.append("https://www.lavozdeasturias.es/")
            self.allowed_domains.append("lavozdeasturias.es")
            self.rules.append(Rule(LinkExtractor(allow=r"^https://www\.lavozdeasturias\.es", deny=[r"lavozdeasturias\.es/publicaciones/", r"lavozdeasturias\.es/noticia/agora/"]), callback="parse_lavozdeasturias", follow=True))

        self.custom_settings = {
            "DEFAULT_REQUEST_HEADERS": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                #"Accept-Language": "es-ES,es;q=0.9",
                #"Referer": "https://www.google.com/",
                #"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                #"Accept-Encoding": "gzip, deflate",
                #"Sec-Ch-Ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
                #"Sec-Fetch-Mode": "navigate",
                #"Sec-Fetch-Site": "none",
                #"Sec-Fetch-Dest": "document",
                #"Sec-Ch-Ua-Mobile": "?0",
                #"Upgrade-Insecure-Requests": "1",
                #"Sec-Ch-Ua-Platform": "\"Windows\""
            }
        }

        super().__init__(**kwargs)

    def processText(self, paragraphs):
        body = [re.sub(r"<.+?>", "", paragraph).strip(" \ufeff\xa0\n\t\r") for paragraph in paragraphs]
        text = "\n\n".join(body)
        text = text.replace("\xa0", " ")
        text = text.replace("\ufeff", "")
        text = re.sub(r"<br(?: ?/)?>", "\n\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
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

        if item["text"] != "" and item["title"] != None and item["datetime"] != None:
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

        if item["text"] != "" and item["title"] != None and item["datetime"] != None:
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

        if item["text"] != "" and item["title"] != None and item["datetime"] != None:
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

        author = self.stripIfNotNone(response.xpath("//p[@class='voc-author__name']/a/text()").get())

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

        if item["text"] != "" and item["title"] != None and item["datetime"] != None:
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

        if item["text"] != "" and item["title"] != None and item["datetime"] != None:
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

        if item["text"] != "" and item["title"] != None and item["datetime"] != None:
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

        if item["text"] != "" and item["title"] != None and item["datetime"] != None:
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

        if item["text"] != "" and item["title"] != None and item["datetime"] != None:
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

        if item["text"] != "" and item["title"] != None and item["datetime"] != None:
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

        if item["text"] != "" and item["title"] != None and item["datetime"] != None:
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

        if item["text"] != "" and item["title"] != None and item["datetime"] != None:
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

        if item["text"] != "" and item["title"] != None and item["datetime"] != None:
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

        if item["text"] != "" and item["title"] != None and item["datetime"] != None:
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

        if item["text"] != "" and item["title"] != None and item["datetime"] != None:
            return item