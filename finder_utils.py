import json
import re
from os import PathLike
from typing import Union, List, Dict, Tuple

from constants import SKINS_DATA_PATH, KNIFE_SECTIONS


def skin_finder(path: Union[str, PathLike]) -> List[Tuple[Dict[str, Union[str, List[str]]], str]]:
    result = []
    with open(path, encoding='utf-8') as file:
        data = json.load(file)
    for skin in data:
        match = re.match(r'^-(.*)%', skin['Разница с ценой в Steam'])
        if match:
            if int(match.group(1)) > 45:
                result.append((skin, 'Скидка больше 45 %'))
            elif int(match.group(1)) > 40 and 'knife' in skin['Название'].lower():
                result.append((skin, 'Нож со скидкой более 40%'))
    return result


def finder_main():
    skin_to_send = {}
    for key, path in SKINS_DATA_PATH.items():
        skin_to_send[key] = skin_finder(path)
    return skin_to_send

