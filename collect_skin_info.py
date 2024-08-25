import argparse
import asyncio
import concurrent.futures
import json
import time
from typing import Dict, List, Union

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from constants import BASE_URL, SECTIONS
from exceptions import InvalidSection, PageQuantity


def page_with_selenium(url: str) -> str:
    s = Service(executable_path='chromedriver-win32/chromedriver.exe')
    driver = webdriver.Chrome(service=s)
    try:
        driver.get(url)
        time.sleep(5)
        page_source = driver.page_source
        return page_source
    except Exception as e:
        print(f'Ошибка - {e}')
        raise
    finally:
        driver.quit()


def parse_page_source(page_source: str) -> List[Dict[str, Union[str, List[str]]]]:
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
        skin_link_value = skin_link.get('href') if skin_link else ''

        row_dict['Название'] = skin_name_value
        row_dict['Цена'] = skin_price_value
        row_dict['Разница с ценой в Steam'] = skin_steam_price_diff_value
        row_dict['Информация'] = {k: v for k, v in zip(('Качество', 'Float'), skin_info_values)}
        row_dict['Ссылка на товар'] = skin_link_value

        item_list.append(row_dict)

    return item_list


async def get_page_data(url: str) -> List[Dict[str, Union[str, List[str]]]]:
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        page_source = await loop.run_in_executor(pool, page_with_selenium, url)
        items = parse_page_source(page_source)
        return items


def make_url(url: str, sorted_by_hot=True, page=1) -> str:
    if page < 1:
        raise PageQuantity('Количество страниц должно быть больше или равно 1')
    return f'{url}?sort_by=hot&page={page}' if sorted_by_hot else f'{url}&page={page}'


async def fetch_and_save_data(base_url: str, sorted_by_hot: bool = True, pages: int = 1):
    urls = [make_url(base_url, sorted_by_hot=sorted_by_hot, page=page) for page in range(1, pages + 1)]
    tasks = [get_page_data(url) for url in urls]
    results = await asyncio.gather(*tasks)

    all_items = [item for sublist in results for item in sublist]

    with open('data/skins_data/all_async_responses.json', 'w', encoding='utf-8') as out_file:
        json.dump(all_items, out_file, ensure_ascii=False, indent=4)

    print(f'Запрос выполнен на {pages} страницах')


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


if __name__ == '__main__':
    args = parse_arguments()
    if args.section:
        if args.section in SECTIONS:
            url_section = f'{BASE_URL}{SECTIONS.get(args.section)}'
        else:
            raise InvalidSection('Такой секции скинов нет на сайте')
    else:
        url_section = BASE_URL

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(fetch_and_save_data(base_url=url_section, sorted_by_hot=args.sorted_by_hot, pages=args.pages))
