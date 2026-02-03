from typing import Optional, List
from bot.entity.guildLanguageSetting import GuildLanguageSetting


class GuildLanguageSettingRepository:
    def __init__(self, session):
        self.session = session

    def getByGuildId(self, guildId: int) -> Optional[GuildLanguageSetting]:
        return (
            self.session
            .query(GuildLanguageSetting)
            .filter_by(guild_id=guildId)
            .first()
        )

    def upsertLanguage(self, guildId: int, languageCode: str) -> GuildLanguageSetting:
        setting = self.getByGuildId(guildId)

        if setting:
            setting.language_code = languageCode
            self.session.add(setting)
        else:
            setting = GuildLanguageSetting(
                guild_id=guildId,
                language_code=languageCode
            )
            self.session.add(setting)

        self.session.commit()
        return setting

    def getAll(self) -> List[GuildLanguageSetting]:
        return self.session.query(GuildLanguageSetting).all()
