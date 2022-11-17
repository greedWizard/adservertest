import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from locations.models import City, Country, State, Region, Subway
from django.conf import settings

class Command(BaseCommand):
    help = 'Парсер регионов и населенных пунктов РФ'

    def parser(self, url, city=False):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        data=[]
        validate_div = []
        if page.status_code == 200: #проверка соединения с сайтом
            if city == True:
                for div in soup.find_all('div'):
                    div_str = str(div)
                    validate_div.append([value for value in div_str.split('<br/>')])
                return validate_div
            else:
                for a in soup.find_all('a', href=True):
                    if a.text != 'В начало' and a.text != 'Назад':
                        data.append({'name': a.text, 'url': a['href']})
                return data


    def handle(self, *args, **kwargs):
        self.stdout.write("Начат процесс парсинга...")
        url = settings.PARSER_SITE_CITY_RF
        regions = self.parser(settings.PARSER_SITE_CITY_RF)
        country = Country.objects.get_or_create(name="Российская Федерация")
        for region in regions:
            state = State.objects.get_or_create(country_id= country[0].id, name=region['name'])
            cities = self.parser(url+region['url'])
            for city in cities:
                try:
                    city_db = City.objects.get_or_create(state_id =state[0].id, name=city['name'])
                except:
                    # При дублировании добавляется регион к названию города
                    name_city = city['name'] + ' (' +region['name'] +')'
                    city_db = City.objects.get_or_create(state_id =state[0].id, name=name_city)
                city_data = self.parser(url+city['url'], True)
                if city_data != []:
                    regs, subways = city_data[2][1:-1], city_data[3][1:-1]
                    #районы
                    for reg in regs:
                        Region.objects.get_or_create(city_id = city_db[0].id, name=reg)
                    #метро
                    for subway in subways:
                        Subway.objects.get_or_create(city_id = city_db[0].id, name=subway)
        self.stdout.write("Процесс окончен")