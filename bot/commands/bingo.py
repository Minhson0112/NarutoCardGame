import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.dailyTaskRepository import DailyTaskRepository
from bot.services.i18n import t


class Bingo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji_map = {
            1: "1️⃣",
            2: "2️⃣",
            3: "3️⃣",
            4: "4️⃣",
            5: "5️⃣",
        }

    @app_commands.command(name="bingo", description="Chơi bingo để trúng thưởng 🎉")
    @app_commands.describe(bet="Số tiền cược bạn muốn đặt 💰")
    async def bingo(self, interaction: discord.Interaction, bet: int):
        await interaction.response.defer(thinking=True)

        player_id = interaction.user.id
        guild_id = interaction.guild.id if interaction.guild else None

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                dailyTaskRepo = DailyTaskRepository(session)

                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send(t(guild_id, "bingo.not_registered"))
                    return

                if bet <= 0:
                    await interaction.followup.send(t(guild_id, "bingo.bet_invalid"))
                    return

                if bet > 1_000_000:
                    await interaction.followup.send(t(guild_id, "bingo.bet_too_large"))
                    return

                if player.coin_balance < bet:
                    await interaction.followup.send(t(guild_id, "bingo.not_enough_balance"))
                    return

                dailyTaskRepo.updateMinigame(player_id)

                win_number = random.randint(1, 5)
                win_emoji = self.emoji_map[win_number]

                description = t(guild_id, "bingo.intro", bet=bet)

                # Send 1 message, then add reactions to that same message.
                msg = await interaction.followup.send(content=description, wait=True)
                for i in range(1, 6):
                    await msg.add_reaction(self.emoji_map[i])

                attempt = 0
                correct = False
                chosen_multiplier = 0

                def check(reaction: discord.Reaction, user: discord.User) -> bool:
                    return (
                        user.id == player_id
                        and reaction.message.id == msg.id
                        and str(reaction.emoji) in self.emoji_map.values()
                    )

                while attempt < 2 and not correct:
                    try:
                        reaction, user = await self.bot.wait_for(
                            "reaction_add",
                            timeout=30.0,
                            check=check
                        )
                    except asyncio.TimeoutError:
                        break

                    if str(reaction.emoji) == win_emoji:
                        correct = True
                        chosen_multiplier = 4 if attempt == 0 else 2
                    else:
                        try:
                            await msg.clear_reaction(reaction.emoji)
                        except Exception:
                            pass
                        attempt += 1

                if correct:
                    reward = bet * chosen_multiplier
                    if attempt == 0:
                        outcome_text = t(
                            guild_id,
                            "bingo.win_first_try",
                            numberEmoji=win_emoji,
                            reward=reward
                        )
                    else:
                        outcome_text = t(
                            guild_id,
                            "bingo.win_second_try",
                            numberEmoji=win_emoji,
                            reward=reward
                        )

                    player.coin_balance = player.coin_balance - bet + reward
                else:
                    outcome_text = t(
                        guild_id,
                        "bingo.lose",
                        numberEmoji=win_emoji,
                        bet=bet
                    )
                    player.coin_balance -= bet

                playerRepo.incrementExp(player_id, amount=2)
                session.commit()

                embed_outcome = discord.Embed(
                    title=t(guild_id, "bingo.result_embed.title"),
                    description=t(
                        guild_id,
                        "bingo.result_embed.desc",
                        numberEmoji=win_emoji,
                        outcomeText=outcome_text,
                        balance=player.coin_balance
                    ),
                    color=discord.Color.blue()
                )

                # Edit the same message that has reactions
                await msg.edit(content=None, embed=embed_outcome)

        except Exception as e:
            print("❌ Lỗi khi xử lý /bingo:", e)
            await interaction.followup.send(t(guild_id, "bingo.error"))


async def setup(bot):
    await bot.add_cog(Bingo(bot))
