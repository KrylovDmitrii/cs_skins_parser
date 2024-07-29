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

pistol_keys = [
    'pistol'
]

rifle_keys = [
    'rifle'
]

sniper_rifle_keys = [
    'sniper-rifle'
]

KNIFE_SECTIONS = {key: key for key in knife_keys}
PISTOL_SECTIONS = {key: key for key in pistol_keys}
RIFLE_SECTIONS = {key: key for key in rifle_keys}
SNIPER_RIFLE_SECTIONS = {key: key for key in sniper_rifle_keys}

SECTIONS = {
    **KNIFE_SECTIONS,
    **PISTOL_SECTIONS,
    **RIFLE_SECTIONS,
    **SNIPER_RIFLE_SECTIONS
}


BASE_URL = 'https://lis-skins.ru/market/csgo/'