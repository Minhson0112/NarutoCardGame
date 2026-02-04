import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.config.config import ADMIN_OVERRIDE_ID
from bot.services.i18n import t


class GiveawayRyo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="giveawayryo", description="Give Ryo (admin only)")
    @app_commands.describe(
        target="Tag của người nhận",
        amount="Số Ryo muốn tặng"
    )
    async def giveawayRyo(self, interaction: discord.Interaction, target: discord.Member, amount: int):
        await interaction.response.defer(thinking=True)
        guild_id = interaction.guild.id if interaction.guild else None
        dev_id = interaction.user.id

        # permission
        if dev_id not in ADMIN_OVERRIDE_ID:
            await interaction.followup.send(t(guild_id, "giveawayryo.no_permission"))
            return

        if amount <= 0:
            await interaction.followup.send(t(guild_id, "giveawayryo.amount_invalid"))
            return

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                receiver = playerRepo.getById(target.id)
                if not receiver:
                    await interaction.followup.send(t(guild_id, "giveawayryo.receiver_not_registered"))
                    return

                receiver.coin_balance += amount
                session.commit()

                await interaction.followup.send(
                    t(guild_id, "giveawayryo.success", amount=amount, mention=target.mention)
                )

        except Exception as e:
            print("❌ Lỗi khi xử lý giveawayryo:", e)
            await interaction.followup.send(t(guild_id, "giveawayryo.error_generic"))


async def setup(bot):
    await bot.add_cog(GiveawayRyo(bot))
