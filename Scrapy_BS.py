from bs4 import BeautifulSoup
import requests


class ScrapMercadoLibre:
    def __init__(self):
        self.url = 'https://listado.mercadolibre.com.co/'

    def scrapper(self, parametro):
        link_list = []
        response = requests.get(self.url + parametro)
        print(self.url + parametro)
        soup = BeautifulSoup(response.content, 'html.parser')
        a_list = soup.find_all('a', class_='ui-search-item__group__element ui-search-link')
        if a_list:
            for a in a_list[:5:]:
                link_list.append(a.get_attribute_list('href'))
        else:
            div_list = soup.find_all('div', class_='ui-search-result__image')
            print(div_list)
            for d in div_list[:5:]:
                link_list.append(d.a.get_attribute_list('href'))
                print(d.a.get_attribute_list('title'))
        return link_list
