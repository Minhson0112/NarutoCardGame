import discord
from discord.ext import commands
from discord import app_commands
from datetime import date

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.playerWeaponRepository import PlayerWeaponRepository
from bot.repository.gifcodeRepository import GifcodeRepository
from bot.repository.gifcodeLogRepository import GifcodeLogRepository
from bot.services.i18n import t


class GiftcodeGame(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="giftcode", description="Sử dụng mã GIFT để nhận quà")
    @app_commands.describe(code="Mã GIFT bạn muốn sử dụng")
    async def giftcode(self, interaction: discord.Interaction, code: str):
        await interaction.response.defer(thinking=True)
        player_id = interaction.user.id
        guild_id = interaction.guild.id if interaction.guild else None

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send(t(guild_id, "giftcode.not_registered"))
                    return

                gifcodeRepo = GifcodeRepository(session)
                gifcodeLogRepo = GifcodeLogRepository(session)
                playerCardRepo = PlayerCardRepository(session)
                playerWeaponRepo = PlayerWeaponRepository(session)

                gifcodeEntry = gifcodeRepo.getByGifCode(code)
                if not gifcodeEntry:
                    await interaction.followup.send(t(guild_id, "giftcode.not_found"))
                    return

                if gifcodeEntry.expiration_date is not None and date.today() > gifcodeEntry.expiration_date:
                    await interaction.followup.send(t(guild_id, "giftcode.expired"))
                    return

                if gifcodeLogRepo.hasPlayerUsed(player_id, gifcodeEntry.id):
                    await interaction.followup.send(t(guild_id, "giftcode.already_used"))
                    return

                rewards: list[str] = []

                if gifcodeEntry.bonus_ryo is not None:
                    player.coin_balance += gifcodeEntry.bonus_ryo
                    rewards.append(
                        t(guild_id, "giftcode.reward.ryo", amount=gifcodeEntry.bonus_ryo)
                    )

                if gifcodeEntry.card_key is not None:
                    playerCardRepo.incrementQuantity(player_id, gifcodeEntry.card_key, increment=1)
                    card_name = (
                        gifcodeEntry.cardTemplate.name
                        if gifcodeEntry.cardTemplate and gifcodeEntry.cardTemplate.name
                        else gifcodeEntry.gif_name
                    )
                    rewards.append(
                        t(guild_id, "giftcode.reward.card", name=card_name)
                    )

                if gifcodeEntry.weapon_key is not None:
                    playerWeaponRepo.incrementQuantity(player_id, gifcodeEntry.weapon_key, increment=1)
                    weapon_name = (
                        gifcodeEntry.weaponTemplate.name
                        if gifcodeEntry.weaponTemplate and gifcodeEntry.weaponTemplate.name
                        else t(guild_id, "giftcode.reward.weapon_default")
                    )
                    rewards.append(
                        t(guild_id, "giftcode.reward.weapon", name=weapon_name)
                    )

                gifcodeLogRepo.createGifcodeLog(player_id, gifcodeEntry.id)
                session.commit()

                reward_str = ", ".join(rewards) if rewards else t(guild_id, "giftcode.reward.none")

                response = (
                    f"{t(guild_id, 'giftcode.success.title')}\n"
                    f"{t(guild_id, 'giftcode.success.detail', rewards=reward_str)}\n"
                )
                await interaction.followup.send(response)

        except Exception as e:
            print("❌ Lỗi khi xử lý /giftcode:", e)
            await interaction.followup.send(
                t(guild_id, "giftcode.error_generic"),
                ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(GiftcodeGame(bot))
