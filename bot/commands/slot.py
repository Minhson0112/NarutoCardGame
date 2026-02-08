import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.dailyTaskRepository import DailyTaskRepository
from bot.services.i18n import t


class Slot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.slot_emojis = ["🍒", "🍋", "🍊", "🍇", "🍉", "⭐", "💎"]

    @app_commands.command(name="slot", description="Chơi máy slot để trúng thưởng 🎰")
    @app_commands.describe(bet="Số tiền cược bạn muốn đặt (Ryo)")
    async def slot(self, interaction: discord.Interaction, bet: int):
        await interaction.response.defer(thinking=True)
        player_id = interaction.user.id
        guild_id = interaction.guild.id if interaction.guild else None

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                dailyTaskRepo = DailyTaskRepository(session)

                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send(t(guild_id, "slot.not_registered"))
                    return

                if bet <= 0:
                    await interaction.followup.send(t(guild_id, "slot.bet_must_be_positive"))
                    return

                if bet > 1_000_000:
                    await interaction.followup.send(t(guild_id, "slot.bet_too_large"))
                    return

                if player.coin_balance < bet:
                    await interaction.followup.send(t(guild_id, "slot.not_enough_balance"))
                    return

                dailyTaskRepo.updateMinigame(player_id)

                outcome = [random.choice(self.slot_emojis) for _ in range(3)]
                unique_count = len(set(outcome))
                if unique_count == 1:
                    multiplier = 10
                elif unique_count == 2:
                    multiplier = 2
                else:
                    multiplier = 0

                initial_embed = discord.Embed(
                    title=t(guild_id, "slot.initial.title"),
                    description=t(guild_id, "slot.initial.desc", bet=bet),
                    color=discord.Color.gold()
                )
                msg = await interaction.followup.send(embed=initial_embed)

                await asyncio.sleep(0.5)
                embed_step1 = discord.Embed(
                    title=t(guild_id, "slot.initial.title"),
                    description=f"{outcome[0]}",
                    color=discord.Color.gold()
                )
                await msg.edit(embed=embed_step1)

                await asyncio.sleep(0.5)
                embed_step2 = discord.Embed(
                    title=t(guild_id, "slot.initial.title"),
                    description=f"{outcome[0]} | {outcome[1]}",
                    color=discord.Color.gold()
                )
                await msg.edit(embed=embed_step2)

                await asyncio.sleep(0.5)
                embed_step3 = discord.Embed(
                    title=t(guild_id, "slot.initial.title"),
                    description=f"{outcome[0]} | {outcome[1]} | {outcome[2]}",
                    color=discord.Color.gold()
                )
                await msg.edit(embed=embed_step3)

                await asyncio.sleep(1)

                outcome_joined = " | ".join(outcome)

                if multiplier > 0:
                    reward = bet * multiplier
                    if multiplier == 10:
                        outcome_text = t(guild_id, "slot.result.jackpot", outcome=outcome_joined, reward=reward)
                    else:
                        outcome_text = t(guild_id, "slot.result.win", outcome=outcome_joined, reward=reward)

                    player.coin_balance = player.coin_balance - bet + reward
                    final_color = discord.Color.green()
                else:
                    outcome_text = t(guild_id, "slot.result.lose", outcome=outcome_joined, bet=bet)
                    player.coin_balance -= bet
                    final_color = discord.Color.red()

                playerRepo.incrementExp(player_id, amount=2)
                session.commit()

                final_embed = discord.Embed(
                    title=t(guild_id, "slot.result.title"),
                    description=(
                        f"{t(guild_id, 'slot.result.spin_line', outcome=outcome_joined)}\n\n"
                        f"{outcome_text}\n\n"
                        f"{t(guild_id, 'slot.result.balance', balance=f'{player.coin_balance:,}')}"
                    ),
                    color=final_color
                )
                await msg.edit(embed=final_embed)

        except Exception as e:
            print("❌ Lỗi khi xử lý /slot:", e)
            await interaction.followup.send(t(guild_id, "slot.error"))

async def setup(bot):
    await bot.add_cog(Slot(bot))