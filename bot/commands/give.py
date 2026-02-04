import discord
from discord.ext import commands
from discord import app_commands
from datetime import date, datetime

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.config.config import LEVEL_RECEIVED_LIMIT, LEVEL_CONFIG
from bot.services.i18n import t


class Give(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="give", description="Chuyển tiền cho người khác")
    @app_commands.describe(
        target="Tag của người nhận",
        amount="Số Ryo cần chuyển"
    )
    async def give(self, interaction: discord.Interaction, target: discord.Member, amount: int):
        await interaction.response.defer(thinking=True)
        guild_id = interaction.guild.id if interaction.guild else None

        sender_id = interaction.user.id
        receiver_id = target.id

        if amount <= 0:
            await interaction.followup.send(t(guild_id, "give.amount_invalid"))
            return

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                sender = playerRepo.getById(sender_id)
                receiver = playerRepo.getById(receiver_id)

                if sender is None:
                    await interaction.followup.send(t(guild_id, "give.sender_not_registered"))
                    return

                if receiver is None:
                    await interaction.followup.send(t(guild_id, "give.receiver_not_registered"))
                    return

                if sender.coin_balance < amount:
                    await interaction.followup.send(t(guild_id, "give.insufficient_balance"))
                    return

                # --- DAILY LIMIT ---
                today = date.today()

                # reset nếu ngày khác (guard null)
                if receiver.daily_received_date is not None:
                    if receiver.daily_received_date.date() != today:
                        receiver.daily_received_amount = 0
                        receiver.daily_received_date = datetime.now()
                else:
                    receiver.daily_received_amount = 0
                    receiver.daily_received_date = datetime.now()

                # Tính level từ exp
                exp = receiver.exp or 0
                thresholds = sorted(int(k) for k in LEVEL_CONFIG.keys())
                level = 0
                for t_threshold in thresholds:
                    if exp >= t_threshold:
                        level = LEVEL_CONFIG[str(t_threshold)]
                    else:
                        break

                limit = LEVEL_RECEIVED_LIMIT.get(str(level), 0)

                received_today = receiver.daily_received_amount or 0
                if received_today + amount > limit:
                    await interaction.followup.send(
                        t(
                            guild_id,
                            "give.limit_exceeded",
                            level=level,
                            limit=limit,
                            received=received_today
                        )
                    )
                    return

                # --- Transfer ---
                sender.coin_balance -= amount
                receiver.coin_balance += amount
                receiver.daily_received_amount = received_today + amount

                session.commit()

                await interaction.followup.send(
                    t(guild_id, "give.success", amount=amount, mention=target.mention)
                )

        except Exception as e:
            print("❌ Lỗi khi xử lý give:", e)
            await interaction.followup.send(t(guild_id, "give.error_generic"))


async def setup(bot):
    await bot.add_cog(Give(bot))
