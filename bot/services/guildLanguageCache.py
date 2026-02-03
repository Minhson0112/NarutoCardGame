from typing import Dict

from bot.config.database import getDbSession
from bot.repository.guildLanguageSettingRepository import GuildLanguageSettingRepository


class GuildLanguageCache:
    def __init__(self):
        self.guildLanguageMap: Dict[int, str] = {}

    async def loadAll(self) -> int:
        with getDbSession() as session:
            repo = GuildLanguageSettingRepository(session)
            rows = repo.getAll()

        self.guildLanguageMap = {r.guild_id: r.language_code for r in rows}
        return len(self.guildLanguageMap)

    def getLanguage(self, guildId: int) -> str:
        return self.guildLanguageMap.get(guildId, "vi")

    def setLanguage(self, guildId: int, languageCode: str) -> None:
        self.guildLanguageMap[guildId] = languageCode


guildLanguageCache = GuildLanguageCache()
