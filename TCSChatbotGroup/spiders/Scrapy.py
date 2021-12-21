import re
import logging
import scrapy

lista = []
count_page = 0
amount_page = 0

""" logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

 """

class SuperSpider(scrapy.Spider):
    name = "items"
    links={}
    links['links']=[]

    def __init__(self,params='televisores'):
        self.params = params
        self.start_urls = ['https://listado.mercadolibre.com.co/{}'.format(self.params)]


    def parse(self, response):                                                
        try:
            #logger.info(f"Entro en la ejecucion de la araña")

            

            request = scrapy.FormRequest(url=self.start_urls[0],
                                     method='GET',cookies=self.define_cookies(),                                     
                                     callback=self.to_scrape)

            yield request
        except:
            yield [{'links':'no se encontro resultados'}]

    def define_cookies(self):
        return [{ '_ml_ga':'GA1.3.44422918.1639520530',
                    '_ml_ga_gid':'GA1.3.1660336248.1639520530',
                    '_ml_ci':'44422918.1639520530',
                    '_d2id':'542800f1-3c49-4f30-8e24-a4d5b2b4c7e4',
                    '__gads':'ID=c42008c9797a224c:T=1639520533:S=ALNI_MaURIHGI6lBt7ZmWmtfQ_gEhzbgWQ',
                    '_hjSessionUser_720735':'eyJpZCI6ImQ4ODI0NGNiLTFjYTQtNWEzNC05YmJjLTU1MjI0NzIwMjlkNCIsImNyZWF0ZWQiOjE2Mzk1MjA1MzI0MDksImV4aXN0aW5nIjp0cnVlfQ==',
                    '_csrf':'M40pJsJPcqn91aJU5_YZ3Ywr',
                    'c_ui-navigation':'5.18.2',
                    '_gcl_au':'1.1.863984351.1639521945',
                    '_ml_dc':'1',
                    '_hjSession_720735':'eyJpZCI6IjYzNzBjNWE1LTAyZmUtNGYzOC1hYjI1LWY3NWMwY2ZmZDAwMCIsImNyZWF0ZWQiOjE2Mzk1NDI2NDU1MTN9',
                    '_hjAbsoluteSessionInProgress':'0',
                    'LAST_SEARCH':self.params
                    }]


    def to_scrape(self,response):
        try:
            divs= response.css('.ui-search-result__content-wrapper')
            if divs[0].xpath('.//div[@class="ui-search-item__group ui-search-item__group--title"]/a/@href').get() is None:            
                self.get_links(response.css('.ui-search-result__image'),1)                                
            else:
                count=0
                self.get_links(divs,0)                
            yield self.links
        except:
            yield [{'links':'no se encontratos resultado'}]
    

    def get_links(self,selector,aux):
        count =0
        if(aux==1):
            while count < 5:
                a=selector[count].xpath('.//a/@href').get()
                self.links['links'].append(a)
                count+=1
        else:
            while count < 5:
                a= selector[count].xpath('.//div[@class="ui-search-item__group ui-search-item__group--title"]/a/@href').get()
                self.links['links'].append(a)
                count+=1
