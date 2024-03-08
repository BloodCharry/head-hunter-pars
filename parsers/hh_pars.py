import random
import time

import requests
from bs4 import BeautifulSoup
import re
import json

from common.HH_cockie import cookies, headers

list_urls = [
    'https://hh.ru/search/vacancy?L_save_area=true&text=&excluded_text=&area=113&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=30&items_on_page=100',
    'https://hh.ru/search/vacancy?L_save_area=true&text=&excluded_text=&area=1317&area=1368&area=1475&area=1414&area=1020&area=1422&area=1061&area=1556&area=1216&area=1948&area=1806&area=1596&area=1384&area=1975&area=1943&area=2&area=2019&area=1229&area=1041&area=1481&area=1255&area=1754&area=1463&area=1575&area=1716&area=1982&area=1985&area=1434&area=1739&area=1347&area=1932&area=1941&area=145&area=1342&area=1103&area=1202&area=1471&area=2155&area=1614&area=1090&area=1960&area=1771&area=1051&area=1438&area=1&area=1783&area=1946&area=1249&area=1077&area=1261&area=1586&area=1424&area=1308&area=1563&area=1008&salary=&currency_code=RUR&experience=doesNotMatter&order_by=publication_time&search_period=30&items_on_page=100',
    'https://hh.ru/search/vacancy?L_save_area=true&text=&excluded_text=&area=1932&area=1596&area=1424&area=1434&area=1463&area=1960&area=1041&area=1941&area=1317&area=1229&area=1077&area=1384&area=1982&area=1948&area=1368&area=1&area=2&area=1438&area=1261&area=1308&area=1946&area=2019&area=1422&area=1202&area=1556&area=1008&area=1051&area=2155&area=1754&area=1475&area=1481&area=1020&area=1614&area=1347&area=1090&area=1806&area=1586&area=1985&area=1471&area=1216&area=1575&area=1061&area=1783&area=1255&area=145&area=1414&area=1342&area=1975&area=1943&area=1563&area=1103&area=1716&area=1771&area=1249&area=1739&salary=&currency_code=RUR&experience=doesNotMatter&order_by=salary_desc&search_period=30&items_on_page=100',
    'https://hh.ru/search/vacancy?L_save_area=true&text=&excluded_text=&area=1716&area=1982&area=1575&area=1347&area=1261&area=1434&area=1946&area=1103&area=1255&area=1368&area=1739&area=145&area=1061&area=1481&area=1090&area=1424&area=1249&area=1948&area=1216&area=1586&area=1943&area=1471&area=1229&area=1422&area=1051&area=1041&area=1202&area=1384&area=2019&area=1563&area=1932&area=1985&area=1308&area=1414&area=1020&area=1463&area=1438&area=1960&area=1783&area=1475&area=1771&area=1317&area=1342&area=1975&area=1008&area=1556&area=2155&area=1596&area=1614&area=1806&area=1754&area=1&area=1941&area=1077&area=2&salary=&currency_code=RUR&experience=doesNotMatter&order_by=salary_asc&search_period=30&items_on_page=100',
    'https://hh.ru/search/vacancy?L_save_area=true&text=&excluded_text=&area=1739&area=1077&area=1948&area=1317&area=1229&area=1946&area=1982&area=1475&area=1103&area=1090&area=1008&area=1960&area=1438&area=1051&area=1563&area=1754&area=1384&area=1202&area=1471&area=2155&area=1716&area=1061&area=1586&area=1434&area=1783&area=1041&area=1308&area=1771&area=1463&area=1368&area=1941&area=1614&area=1575&area=1422&area=1985&area=1481&area=1342&area=1424&area=1249&area=1596&area=1806&area=1414&area=1&area=1020&area=1943&area=2019&area=1261&area=1255&area=1556&area=1347&area=1216&area=1932&area=1975&area=145&area=2&salary=&currency_code=RUR&experience=doesNotMatter&schedule=fullDay&order_by=relevance&search_period=7&items_on_page=100',
    'https://hh.ru/search/vacancy?L_save_area=true&area=1739&area=1077&area=1948&area=1317&area=1229&area=1946&area=1982&area=1475&area=1103&area=1090&area=1008&area=1960&area=1438&area=1051&area=1563&area=1754&area=1384&area=1202&area=1471&area=2155&area=1716&area=1061&area=1586&area=1434&area=1783&area=1041&area=1308&area=1771&area=1463&area=1368&area=1941&area=1614&area=1575&area=1422&area=1985&area=1481&area=1342&area=1424&area=1249&area=1596&area=1806&area=1414&area=1&area=1020&area=1943&area=2019&area=1261&area=1255&area=1556&area=1347&area=1216&area=1932&area=1975&area=145&area=2&search_period=7&items_on_page=100&search_field=name&search_field=company_name&search_field=description&enable_snippets=false&text=&only_with_salary=true',
    'https://hh.ru/search/vacancy?L_save_area=true&area=1739&area=1077&area=1948&area=1317&area=1229&area=1946&area=1982&area=1475&area=1103&area=1090&area=1008&area=1960&area=1438&area=1051&area=1563&area=1754&area=1384&area=1202&area=1471&area=2155&area=1716&area=1061&area=1586&area=1434&area=1783&area=1041&area=1308&area=1771&area=1463&area=1368&area=1941&area=1614&area=1575&area=1422&area=1985&area=1481&area=1342&area=1424&area=1249&area=1596&area=1806&area=1414&area=1&area=1020&area=1943&area=2019&area=1261&area=1255&area=1556&area=1347&area=1216&area=1932&area=1975&area=145&area=2&search_period=7&items_on_page=100&search_field=name&search_field=company_name&search_field=description&enable_snippets=false&text=&salary=65000&only_with_salary=true',
    'https://hh.ru/search/vacancy?L_save_area=true&area=1739&area=1077&area=1948&area=1317&area=1229&area=1946&area=1982&area=1475&area=1103&area=1090&area=1008&area=1960&area=1438&area=1051&area=1563&area=1754&area=1384&area=1202&area=1471&area=2155&area=1716&area=1061&area=1586&area=1434&area=1783&area=1041&area=1308&area=1771&area=1463&area=1368&area=1941&area=1614&area=1575&area=1422&area=1985&area=1481&area=1342&area=1424&area=1249&area=1596&area=1806&area=1414&area=1&area=1020&area=1943&area=2019&area=1261&area=1255&area=1556&area=1347&area=1216&area=1932&area=1975&area=145&area=2&search_period=7&items_on_page=100&search_field=name&search_field=company_name&search_field=description&enable_snippets=false&text=&salary=130000&only_with_salary=true',
    'https://hh.ru/search/vacancy?L_save_area=true&area=1739&area=1077&area=1948&area=1317&area=1229&area=1946&area=1982&area=1475&area=1103&area=1090&area=1008&area=1960&area=1438&area=1051&area=1563&area=1754&area=1384&area=1202&area=1471&area=2155&area=1716&area=1061&area=1586&area=1434&area=1783&area=1041&area=1308&area=1771&area=1463&area=1368&area=1941&area=1614&area=1575&area=1422&area=1985&area=1481&area=1342&area=1424&area=1249&area=1596&area=1806&area=1414&area=1&area=1020&area=1943&area=2019&area=1261&area=1255&area=1556&area=1347&area=1216&area=1932&area=1975&area=145&area=2&search_period=7&items_on_page=100&search_field=name&search_field=company_name&search_field=description&enable_snippets=false&text=&salary=195000&only_with_salary=true',
    'https://hh.ru/search/vacancy?L_save_area=true&area=1739&area=1077&area=1948&area=1317&area=1229&area=1946&area=1982&area=1475&area=1103&area=1090&area=1008&area=1960&area=1438&area=1051&area=1563&area=1754&area=1384&area=1202&area=1471&area=2155&area=1716&area=1061&area=1586&area=1434&area=1783&area=1041&area=1308&area=1771&area=1463&area=1368&area=1941&area=1614&area=1575&area=1422&area=1985&area=1481&area=1342&area=1424&area=1249&area=1596&area=1806&area=1414&area=1&area=1020&area=1943&area=2019&area=1261&area=1255&area=1556&area=1347&area=1216&area=1932&area=1975&area=145&area=2&search_period=7&items_on_page=100&search_field=name&search_field=company_name&search_field=description&enable_snippets=false&text=&salary=260000&only_with_salary=true',
    'https://hh.ru/search/vacancy?L_save_area=true&area=1739&area=1077&area=1948&area=1317&area=1229&area=1946&area=1982&area=1475&area=1103&area=1090&area=1008&area=1960&area=1438&area=1051&area=1563&area=1754&area=1384&area=1202&area=1471&area=2155&area=1716&area=1061&area=1586&area=1434&area=1783&area=1041&area=1308&area=1771&area=1463&area=1368&area=1941&area=1614&area=1575&area=1422&area=1985&area=1481&area=1342&area=1424&area=1249&area=1596&area=1806&area=1414&area=1&area=1020&area=1943&area=2019&area=1261&area=1255&area=1556&area=1347&area=1216&area=1932&area=1975&area=145&area=2&search_period=7&items_on_page=100&search_field=name&search_field=company_name&search_field=description&enable_snippets=false&text=&salary=325000&only_with_salary=true',
    'https://hh.ru/search/vacancy?area=1739&area=1077&area=1948&area=1317&area=1229&area=1946&area=1982&area=1475&area=1103&area=1090&area=1008&area=1960&area=1438&area=1051&area=1563&area=1754&area=1384&area=1202&area=1471&area=2155&area=1716&area=1061&area=1586&area=1434&area=1783&area=1041&area=1308&area=1771&area=1463&area=1368&area=1941&area=1614&area=1575&area=1422&area=1985&area=1481&area=1342&area=1424&area=1249&area=1596&area=1806&area=1414&area=1&area=1020&area=1943&area=2019&area=1261&area=1255&area=1556&area=1347&area=1216&area=1932&area=1975&area=145&area=2&items_on_page=100&ored_clusters=true&search_period=30'
]


class HHParser:
    def __init__(self, hh_head, hh_coockie):
        self.hh_head = hh_head
        self.hh_coockie = hh_coockie
        self.base_hh_url = None
        self.urls = []
        self.jobs = {}
        self.first_hoock_url = 'https://cloud.roistat.com/integration/webhook?key=a58c86c38a259de63562d533d7c7edf4'
        self.last_hoock_url = 'https://c6ce863bb1eb.vps.myjino.ru/contacts?apiKey=Wy7RXAzSRZpD4a3q'

    def hh_parse(self, retry=5):
        for base_url in list_urls:
            session = requests.Session()
            try:
                request = session.get(base_url, headers=self.hh_head, cookies=self.hh_coockie)
                retry = 5
            except Exception as ex:
                if retry == 0:
                    print(
                        f'Произошла ошибка при парсинге hh.ru: {ex} '
                        f'\n \n парсер попробует перезапуститься через некоторе время...'
                    )
                    return
                elif retry > 0:
                    time.sleep(random.randint(1, 5))
                    return self.hh_parse(retry - 1)

            if request.status_code == 200:
                soup = BeautifulSoup(request.content, 'lxml')
                try:
                    retry = 5
                    pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
                    count_pages = int(pagination[-1].text)
                    for i in range(count_pages):
                        url = f'{base_url}&page={i}'
                        if url not in self.urls:
                            self.urls.append(url)
                    try:
                        retry = 5
                        self.follow_the_links(session)
                    except:
                        retry -= 1
                        time.sleep(random.randint(1, 5))
                        continue
                except Exception as exc:
                    if retry == 0:
                        print(
                            f'Произошла ошибка при парсинге hh.ru: {exc} '
                            f'\n \n парсер попробует перезапуститься через некоторе время...'
                        )
                        return
                    elif retry > 0:
                        time.sleep(random.randint(1, 5))
                        return self.hh_parse(retry - 1)
            session.close()
            time.sleep(random.randint(5, 15))

    def follow_the_links(self, session, retry=5):
        for url in self.urls:
            request = session.get(url, headers=self.hh_head, cookies=self.hh_coockie)
            soup = BeautifulSoup(request.content, 'lxml')
            divs = soup.find_all('div', class_='serp-item vacancy-serp-item_clickme serp-item_link')
            try:
                retry = 5
                self.link_vacancy(divs, session)
            except:
                retry -= 1
                time.sleep(random.randint(1, 5))
                continue
        self.urls.clear()

    def link_vacancy(self, divs, session):
        for div in divs:
            if not div.find('button',
                            class_='bloko-button bloko-button_kind-success bloko-button_scale-small bloko-button_collapsible bloko-button_appearance-outlined'):
                continue
            id_vacancy = (div.find(
                'a', class_='bloko-button bloko-button_kind-success bloko-button_scale-small').get('href')
                          )
            id_vacancy = re.findall(r'\d+', id_vacancy)
            if id_vacancy[0] in self.jobs:
                continue

            href_id = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).get('href')
            pl_id = re.findall(r'\d+', href_id)

            title = div.find('span', class_='serp-item__title serp-item__title-link').text
            names = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
            name = names.replace('\xa0', ' ')
            city = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text

            request_mail = session.get(
                f'https://hh.ru/vacancy/{id_vacancy[0]}/contacts?employerId={pl_id[0]}',
                headers=self.hh_head,
                cookies=self.hh_coockie
            )

            self.jobs[id_vacancy[0]] = pl_id[0]

            comment = div.find('a', class_='bloko-link').get('href')

            response_data = request_mail.json()
            email = response_data['email']

            first_hoock = {"title": title,
                           "name": name,
                           "email": email,
                           "phone": None,
                           "comment": comment,
                           "roistat_visit": "https://hh.ru",
                           "fields": {
                               "site": "https://hh.ru",
                               "source": "https://hh.ru",
                               "promocode": 'Null'
                           }
                           }
            # requests.post(self.first_hoock_url, json=first_hoock)
            # time.sleep(1)

            last_hoock = {
                "source": "https://hh.ru",
                "name": name,
                "email": email,
                "phone": None,
                "data": f"ссылка на вакансию; {comment}, Имя контакта; {name}, email контакта; {email}, "
                        f"телефон контакта; {None}, Адрес вакансии или город: {city}"
            }
            # requests.post(self.last_hoock_url, json=last_hoock)
            # time.sleep(1)

    def run(self):
        while True:
            try:
                session = self.hh_parse()
                self.follow_the_links(session)
            except:
                pass


jobber = HHParser(hh_head=headers, hh_coockie=cookies)
jobber.run()
