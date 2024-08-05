knife_keys = [
    'knife',
    'bayonet',
    'bowie-knife',
    'butterfly-knife',
    'classic-knife',
    'falchion-knife',
    'flip-knife',
    'gut-knife',
    'huntsman-knife',
    'karambit',
    'kukri-knife',
    'm9-bayonet',
    'navaja-knife',
    'nomad-knife',
    'paracord-knife',
    'shadow-daggers',
    'skeleton-knife',
    'stiletto-knife',
    'survival-knife',
    'talon-knife',
    'ursus-knife'
]

gloves_keys = [
    'bloodhound-gloves',
    'broken-fang-gloves',
    'driver-gloves',
    'hand-wraps',
    'hydra-gloves',
    'moto-gloves',
    'specialist-gloves',
    'sport-gloves'
]

pistol_keys = [
    'pistol',
    'desert-eagle',
    'dual-berettas',
    'five-seven',
    'glock-18',
    'p250',
    'tec-9',
    'usp-s'
]

rifle_keys = [
    'rifle',
    'ak-47',
    'famas',
    'm4a4',
    'm4a1-s',
    'galil-ar'
]

sniper_rifle_keys = [
    'sniper-rifle',
    'awp',
    'ssg-08'
]

another_weapons_keys = [
    'smg',
    'mp9',
    'mac-10',
    'shotgun',
    'xm1014',
    'machinegun',
    'sticker',

]

KNIFE_SECTIONS = {key: key for key in knife_keys}
GLOVE_SECTIONS = {key: key for key in gloves_keys}
PISTOL_SECTIONS = {key: key for key in pistol_keys}
RIFLE_SECTIONS = {key: key for key in rifle_keys}
SNIPER_RIFLE_SECTIONS = {key: key for key in sniper_rifle_keys}
ANOTHER_WEAPONS_SECTIONS = {key: key for key in another_weapons_keys}

SECTIONS = {
    **KNIFE_SECTIONS,
    **GLOVE_SECTIONS,
    **PISTOL_SECTIONS,
    **RIFLE_SECTIONS,
    **SNIPER_RIFLE_SECTIONS,
    **ANOTHER_WEAPONS_SECTIONS
}

BASE_URL = 'https://lis-skins.ru/market/csgo/'

CASE_HARDENED_BASE_URL = 'https://lis-skins.ru/market/csgo/?sort_by=hot&query=case%20hardened'

SKINS_DATA_PATH = {
    'Выгодные скины': 'skins_data/all_async_responses.json',
    'Поверхносткая закалка': 'skins_data/case_hardened.json',
}
