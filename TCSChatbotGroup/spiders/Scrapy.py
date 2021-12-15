import re
import scrapy
from scrapy import loader
from scrapy.loader import ItemLoader 
from TCSChatbotGroup.items import TcschatbotgroupItem

lista = []
count_page = 0
amount_page = 0

class SuperSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['https://wl.superfinanciera.gov.co/SiriWeb/publico/sancion/rep_sanciones_general_par.jsf']
    custom_settings = {
        'ROBOTSTXT': True,
        'FEED_EXPORT_ENCODING':'utf-8'
    }

    def parse(self, response):
        
        java_x_faces = response.css('input[name="javax.faces.ViewState"]::attr(value)').extract_first()
        frm_submit = response.css('input[name="contentSV:frm2_SUBMIT"]::attr(value)').extract_first()
        my_data = {
                "contentSV:frm2:idFechaDesde.day": "10",
                "contentSV:frm2:idFechaDesde.month": "12",
                "contentSV:frm2:idFechaDesde.year": "2018",
                "contentSV:frm2:idFechaHasta.day": "10",
                "contentSV:frm2:idFechaHasta.month": "12",
                "contentSV:frm2:idFechaHasta.year": "2019",
                "contentSV:frm2:j_id_id15pc2": "",
                "contentSV:frm2:j_id_id17pc2": "",
                "contentSV:frm2:j_id_id19pc2": "",
                "contentSV:frm2:numeroResolucion": "",
                "contentSV:frm2:j_id_id25pc2": "",
                "contentSV:frm2:j_id_id26pc2": "Buscar",
                "autoScroll": "0,0",
                "contentSV:frm2_SUBMIT": frm_submit,
                "javax.faces.ViewState": java_x_faces
        }
               
        yield scrapy.FormRequest( self.start_urls[0], method='POST', 
                          formdata=my_data,
                          callback = self.page)
        
        
    def isNull(self, text):
        return '' if text == None else text
    
    
    def page(self, response):
        
        global lista, count_page, amount_page
        if amount_page == 0:
            value = response.css('div.tableCentro::text').get().split(' ')[3]
            amount_page = int(value)
        
        count_page = count_page + 1
        registers = response.xpath("//table[@class='tablaBorde']//tbody/tr")
        for register in registers:
            listRows = dict();
            row = register.css('td') 
            listRows["Persona o Entidad Multada"] = self.isNull(row[0].css('label::text').get())
            listRows["Identificación"] = self.isNull(row[1].css('label::text').get())
            listRows["Clase de Sanción"] = self.isNull(row[2].css('label::text').get())
            listRows["Tipo de Sanción"] = self.isNull(row[3].css('::text').get())
            listRows["Tema Clasificación"] = self.isNull(row[4].css('::text').get())
            listRows["Número de resolución"] =self.isNull(row[5].css('a::text').get())
            listRows["Fecha"] = self.isNull(row[6].css('span::text').get())
            listRows["Cargo multado"] = self.isNull(row[7].css('span::text').get())
            listRows["Monto de Sanción"] = self.isNull(row[8].css('::text').get())
            listRows["Fecha firmeza"] =self.isNull(row[9].css('::text').get())
            listRows["Recurso Interpuso"] = self.isNull(row[10].css('::text').get())
            listRows["Resolución que Resuelve el Recurso"] = self.isNull(row[11].css('::text').get())
            listRows["Fecha Resolución Recurso"] = self.isNull(row[12].css('::text').get())
            listRows["Descripció"] = self.isNull(row[13].css('::text').get())
            if listRows not in lista:
                lista.append(listRows) 
          
        
        if(count_page <= amount_page):
             yield scrapy.FormRequest.from_response(response,  formdata={"contentSV:frm2:j_id_id100pc2":"next"}, callback = self.page) 
        else:
            loader = ItemLoader(item=TcschatbotgroupItem(), selector=lista)
            loader.add_value('response',lista)
            yield loader.load_item()
            print('El tamano es {}'.format(len(lista)))