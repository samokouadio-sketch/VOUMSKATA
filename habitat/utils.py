from django.utils.text import slugify

_LIGATURES = {
    'œ': 'oe', 'Œ': 'OE',
    'æ': 'ae', 'Æ': 'AE',
}


def slugify_fr(value: str) -> str:
    """slugify() qui gère aussi les ligatures françaises (œ, æ) que
    l'unicodedata standard ne décompose pas (ex. « Gros œuvre » -> « gros-oeuvre »)."""
    for lig, replacement in _LIGATURES.items():
        value = value.replace(lig, replacement)
    return slugify(value)
