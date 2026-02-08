import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.services.i18n import t


class NarutoTrapGame:
    def __init__(self, user: discord.User, bet: int):
        self.user = user
        self.bet = bet
        self.rows = 5
        self.cols = 5

        self.grid = [["🌳" for _ in range(self.cols)] for _ in range(self.rows)]
        self.player_pos = [self.rows - 1, self.cols // 2]
        self.grid[self.player_pos[0]][self.player_pos[1]] = "🥷"

        possible_positions = [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if (r, c) != (self.player_pos[0], self.player_pos[1])
        ]
        self.bombs = random.sample(possible_positions, 4)

    def grid_to_str(self) -> str:
        return "\n".join("".join(row) for row in self.grid)

    def reveal_bombs(self):
        for r, c in self.bombs:
            if self.grid[r][c] == "🌳":
                self.grid[r][c] = "💣"

    def move_player(self, direction: str) -> tuple[bool, str]:
        r, c = self.player_pos
        new_r, new_c = r, c

        if direction == "up":
            new_r = r - 1
        elif direction == "left":
            new_c = c - 1
        elif direction == "right":
            new_c = c + 1
        else:
            return False, "invalid_direction"

        if new_r < 0 or new_r >= self.rows or new_c < 0 or new_c >= self.cols:
            return False, "out_of_bounds"

        self.grid[r][c] = "🌳"
        self.player_pos = [new_r, new_c]

        if (new_r, new_c) in self.bombs:
            self.grid[new_r][new_c] = "💣"
            return True, "bomb"

        self.grid[new_r][new_c] = "🥷"
        if new_r == 0:
            return True, "win"

        return True, "moved"


class NarutoTrap(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="narutotrap", description="Chơi minigame Naruto Trap với tiền cược")
    @app_commands.describe(bet="Số tiền cược bạn muốn đặt")
    async def narutotrap(self, interaction: discord.Interaction, bet: int):
        await interaction.response.defer(thinking=True)
        guild_id = interaction.guild.id if interaction.guild else None
        player_id = interaction.user.id

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                player = playerRepo.getById(player_id)

                if not player:
                    await interaction.followup.send(t(guild_id, "narutotrap.not_registered"), ephemeral=True)
                    return

                if bet <= 0:
                    await interaction.followup.send(t(guild_id, "narutotrap.bet.must_be_positive"), ephemeral=True)
                    return

                if bet > 1_000_000:
                    await interaction.followup.send(t(guild_id, "narutotrap.bet.too_high"), ephemeral=True)
                    return

                if player.coin_balance < bet:
                    await interaction.followup.send(t(guild_id, "narutotrap.bet.not_enough_balance"), ephemeral=True)
                    return

                playerRepo.incrementExp(player_id, amount=5)
                session.commit()

            game = NarutoTrapGame(interaction.user, bet)

            embed = discord.Embed(
                title=t(guild_id, "narutotrap.embed.title"),
                description=t(
                    guild_id,
                    "narutotrap.embed.playing",
                    bet=bet,
                    grid=game.grid_to_str()
                ),
                color=discord.Color.gold()
            )
            await interaction.followup.send(embed=embed)
            message = await interaction.original_response()

            directions = {"⬆️": "up", "➡️": "right", "⬅️": "left"}
            for emoji in directions:
                await message.add_reaction(emoji)

            def check(reaction, user):
                return (
                    user == interaction.user
                    and str(reaction.emoji) in directions
                    and reaction.message.id == message.id
                )

            while True:
                try:
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
                except asyncio.TimeoutError:
                    timeout_embed = discord.Embed(
                        title=t(guild_id, "narutotrap.timeout.title"),
                        description=t(guild_id, "narutotrap.timeout.desc", grid=game.grid_to_str()),
                        color=discord.Color.greyple()
                    )
                    await message.edit(embed=timeout_embed)
                    break

                direction = directions[str(reaction.emoji)]
                valid, result = game.move_player(direction)

                try:
                    await message.remove_reaction(reaction.emoji, user)
                except discord.HTTPException:
                    pass

                updated_embed = discord.Embed(
                    title=t(guild_id, "narutotrap.embed.title"),
                    description=t(
                        guild_id,
                        "narutotrap.embed.playing_hint",
                        bet=bet,
                        grid=game.grid_to_str()
                    ),
                    color=discord.Color.gold()
                )
                await message.edit(embed=updated_embed)

                if not valid:
                    continue

                if result == "bomb":
                    game.reveal_bombs()
                    with getDbSession() as session:
                        playerRepo = PlayerRepository(session)
                        player = playerRepo.getById(player_id)
                        player.coin_balance -= bet
                        session.commit()

                    lose_embed = discord.Embed(
                        title=t(guild_id, "narutotrap.lose.title"),
                        description=t(guild_id, "narutotrap.lose.desc", bet=bet, grid=game.grid_to_str()),
                        color=discord.Color.red()
                    )
                    await message.edit(embed=lose_embed)
                    break

                if result == "win":
                    game.reveal_bombs()
                    with getDbSession() as session:
                        playerRepo = PlayerRepository(session)
                        player = playerRepo.getById(player_id)
                        player.coin_balance = player.coin_balance - bet + (bet * 2)
                        session.commit()

                    win_embed = discord.Embed(
                        title=t(guild_id, "narutotrap.win.title"),
                        description=t(guild_id, "narutotrap.win.desc", grid=game.grid_to_str()),
                        color=discord.Color.green()
                    )
                    await message.edit(embed=win_embed)
                    break

        except Exception as e:
            print("❌ Lỗi khi xử lý narutotrap:", e)
            if interaction.response.is_done():
                await interaction.followup.send(t(guild_id, "narutotrap.error.generic"), ephemeral=True)
            else:
                await interaction.response.send_message(t(guild_id, "narutotrap.error.generic"), ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(NarutoTrap(bot))
