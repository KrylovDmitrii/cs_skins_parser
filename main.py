from typing import Dict, Any, List, Union
from exceptions import PageQuantity, InvalidSection
from constants import SECTIONS, BASE_URL
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import logging
import json
import argparse

logging.basicConfig(level=logging.INFO)


def page_with_seleniun(url: str) -> str:
    s = Service(executable_path='chromedriver-win32/chromedriver.exe')
    driver = webdriver.Chrome(service=s)
    try:
        driver.get(url)
        time.sleep(3)
        page_source = driver.page_source
        return page_source
    except Exception as e:
        logging.error(f'Ошибка при получении страницы: {e}')
        raise
    finally:
        driver.close()
        driver.quit()


def page_response_json(url: str) -> List[Dict[str, Union[str, List[str]]]]:
    page_source = page_with_seleniun(url)
    if page_source:
        soup = BeautifulSoup(page_source, 'lxml')
        items = soup.find_all('div', class_='item')

        items_str = '\n\n\n\n\n'.join(str(item) for item in items)

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

        with open('response.json', 'w', encoding='utf-8') as out_file:
            json.dump(item_list, out_file, ensure_ascii=False, indent=4)

        with open('response.html', 'w', encoding='utf-8') as out_file:
            out_file.write(items_str)

        return item_list


def make_url(url: str, sorted_by_hot=True, page=1) -> str:
    if sorted_by_hot:
        url = f'{url}?sort_by=hot'
    if page < 1:
        raise PageQuantity('Количество страниц должно быть больше или равно 1')
    return f'{url}&page={page}'


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Сбор данных с сайта lis-skins.')
    parser.add_argument(
        'section',
        nargs='?',
        default='',
        help='Тип скина для выборки (например, "knife", "glove" и т.д).'
    )

    parser.add_argument(
        '--sorted_by_hot',
        type=bool,
        default=True,
        help='Сортировать по Горячим ценам (True или False).'
    )
    parser.add_argument(
        '--pages',
        type=int,
        default=1,
        help='Количество страниц для сбора данных.'
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    if args.section:
        if args.section in SECTIONS:
            url_section = f'{BASE_URL}{SECTIONS.get(args.section)}'
        else:
            raise InvalidSection('Такой секции скинов нет на сайте')
    else:
        url_section = BASE_URL

    all_items = []
    for page in range(1, args.pages + 1):
        url = make_url(url_section, sorted_by_hot=args.sorted_by_hot, page=page)
        items = page_response_json(url)
        all_items.extend(items)

    with open('all_responses.json', 'w', encoding='utf-8') as out_file:
        json.dump(all_items, out_file, ensure_ascii=False, indent=4)

    logging.info(f'Запросы выполнены на {args.pages} страницах')


if __name__ == '__main__':
    main()
