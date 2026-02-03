import discord
from discord.ext import commands
from discord import app_commands
import random

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.dailyTaskRepository import DailyTaskRepository
from bot.services.i18n import t


class CoinFlip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="coinflip", description="Chơi lật đồng xu để trúng thưởng (dự đoán úp hoặc ngửa)")
    @app_commands.describe(
        bet="Số tiền cược bạn muốn đặt",
        guess="Dự đoán của bạn: u:úp hoặc n:ngửa"
    )
    async def coinflip(self, interaction: discord.Interaction, bet: int, guess: str):
        await interaction.response.defer(thinking=True)

        guild_id = interaction.guild.id if interaction.guild else None
        player_id = interaction.user.id

        guess = (guess or "").lower().strip()
        if guess not in ["u", "n"]:
            await interaction.followup.send(t(guild_id, "coinflip.invalid_guess"))
            return

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                dailyTaskRepo = DailyTaskRepository(session)

                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send(t(guild_id, "coinflip.not_registered"))
                    return

                if bet <= 0:
                    await interaction.followup.send(t(guild_id, "coinflip.bet_must_be_positive"))
                    return

                if bet > 1000000:
                    await interaction.followup.send(t(guild_id, "coinflip.bet_too_large"))
                    return

                if player.coin_balance < bet:
                    await interaction.followup.send(t(guild_id, "coinflip.not_enough_money"))
                    return

                dailyTaskRepo.updateMinigame(player_id)

                coin_result = random.choice(["u", "n"])
                result_text = coin_result.upper()

                if guess == coin_result:
                    reward = bet * 2
                    outcome_text = t(
                        guild_id,
                        "coinflip.result.win",
                        result=result_text,
                        reward=reward
                    )
                    player.coin_balance = player.coin_balance - bet + reward
                else:
                    outcome_text = t(
                        guild_id,
                        "coinflip.result.lose",
                        result=result_text,
                        bet=bet
                    )
                    player.coin_balance -= bet

                playerRepo.incrementExp(player_id, amount=2)
                session.commit()

                embed_outcome = discord.Embed(
                    title=t(guild_id, "coinflip.result.title"),
                    description=(
                        f"{t(guild_id, 'coinflip.result.line_result', result=result_text)}\n"
                        f"{outcome_text}\n\n"
                        f"{t(guild_id, 'coinflip.result.balance', coin=player.coin_balance)}"
                    ),
                    color=discord.Color.purple()
                )
                await interaction.followup.send(embed=embed_outcome)

        except Exception as e:
            print("❌ Lỗi khi xử lý /coinflip:", e)
            await interaction.followup.send(t(guild_id, "coinflip.error"))


async def setup(bot):
    await bot.add_cog(CoinFlip(bot))
