from typing import Dict, Any

from bot.services.guildLanguageCache import guildLanguageCache
from bot.i18n.vi import VI


LANG_MAP: Dict[str, Dict[str, str]] = {
    "vi": VI,
}


def t(guildId: int | None, key: str, **kwargs: Any) -> str:
    language = "vi"
    if guildId is not None:
        language = guildLanguageCache.getLanguage(guildId)

    table = LANG_MAP.get(language, VI)
    template = table.get(key)

    if template is None:
        template = VI.get(key, key)

    try:
        return template.format(**kwargs)
    except Exception:
        return template
