from sqlalchemy import Column, String, BigInteger, TIMESTAMP, text
from bot.config.database import Base


class GuildLanguageSetting(Base):
    __tablename__ = 'guild_language_settings'

    guild_id = Column(BigInteger, primary_key=True)
    language_code = Column(String(10), nullable=False, server_default=text("'vi'"))

    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP")
    )

    def __repr__(self):
        return f"<GuildLanguageSetting(guild_id={self.guild_id}, language_code='{self.language_code}')>"
