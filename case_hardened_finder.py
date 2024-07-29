from typing import Dict, Any, List, Union
from constants import CASE_HARDENED_BASE_URL
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import json
import argparse


def page_with_seleniun(url: str) -> str:
    s = Service(executable_path='chromedriver-win32/chromedriver.exe')
    driver = webdriver.Chrome(service=s)
    try:
        driver.get(url)
        time.sleep(3)
        page_source = driver.page_source
        return page_source
    except Exception as e:
        print(f'Ошибка - {e}')
        raise
    finally:
        driver.close()
        driver.quit()


def page_response_json(url: str) -> List[Dict[str, Union[str, List[str]]]]:
    page_source = page_with_seleniun(url)
    if page_source:
        soup = BeautifulSoup(page_source, 'lxml')
        items = soup.find_all('div', class_='item')

        item_list = []

        for item in items:
            row_dict = {}
            skin_name = item.find('div', class_='name-inner')
            skin_name_value = skin_name.get_text(strip=True) if skin_name else ''

            skin_info = item.find_all('div', class_='info-item')
            skin_info_values = [info_value.get_text(strip=True) for info_value in skin_info if
                                'hold' not in info_value.get('class', [])]

            skin_price = item.find('div', class_='price')
            skin_price_value = skin_price.get_text(strip=True) if skin_price else ''

            skin_steam_price_diff = item.find('div', class_='steam-price-discount')
            skin_steam_price_diff_value = skin_steam_price_diff.get_text(strip=True) if skin_steam_price_diff else ''

            skin_link = item.find('a', class_='name')
            skin_link_value = skin_link.get('href')

            row_dict['Название'] = skin_name_value
            row_dict['Цена'] = skin_price_value
            row_dict['Разница с ценой в Steam'] = skin_steam_price_diff_value
            row_dict['Информация'] = {k: v for k, v in zip(('Качество', 'Float'), skin_info_values)}
            row_dict['Ссылка на товар'] = skin_link_value

            item_list.append(row_dict)

        return item_list


def main():
    all_items = []
    pages = 3
    for page in range(1, pages + 1):
        url = f'{CASE_HARDENED_BASE_URL}&page={page}'
        items = page_response_json(url)
        all_items.extend(items)

    with open('skins_data/case_hardened.json', 'w', encoding='utf-8') as out_file:
        json.dump(all_items, out_file, ensure_ascii=False, indent=4)

    print(f'Запрос скинов "Поверхносткая закалка" выполнен')


if __name__ == '__main__':
    main()
