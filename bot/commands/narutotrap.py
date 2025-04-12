import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository

class NarutoTrapGame:
    def __init__(self, user: discord.User, bet: int):
        self.user = user
        self.bet = bet
        self.rows = 5
        self.cols = 5
        # Tạo grid 5x5 với emoji 🌳
        self.grid = [["🌳" for _ in range(self.cols)] for _ in range(self.rows)]
        # Vị trí ban đầu của người chơi: ô dưới cùng, giữa cột
        self.player_pos = [self.rows - 1, self.cols // 2]
        self.grid[self.player_pos[0]][self.player_pos[1]] = "🥷"
        # Random 3 vị trí bẫy (bomb) từ các ô không phải vị trí bắt đầu
        possible_positions = [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if (r, c) != (self.player_pos[0], self.player_pos[1])
        ]
        self.bombs = random.sample(possible_positions, 3)
    
    def grid_to_str(self) -> str:
        """Chuyển grid thành chuỗi hiển thị."""
        return "\n".join("".join(row) for row in self.grid)
    
    def move_player(self, direction: str) -> (bool, str):
        """
        Di chuyển nhân vật theo hướng: "up", "left" hoặc "right".
        Trả về tuple (bool, message):
          - Nếu di chuyển hợp lệ: 
              "bomb" nếu đi vào bom,
              "win" nếu đến hàng đầu,
              "moved" nếu di chuyển thành công.
          - Nếu không hợp lệ: (False, thông báo lỗi).
        """
        r, c = self.player_pos
        new_r, new_c = r, c
        if direction == "up":
            new_r = r - 1
        elif direction == "left":
            new_c = c - 1
        elif direction == "right":
            new_c = c + 1
        else:
            return False, "Hướng di chuyển không hợp lệ."

        # Kiểm tra biên giới
        if new_r < 0 or new_r >= self.rows or new_c < 0 or new_c >= self.cols:
            return False, "Hướng di chuyển không hợp lệ (ra ngoài biên)."

        # Xoá vị trí cũ, chuyển ô đó về 🌳
        self.grid[r][c] = "🌳"
        self.player_pos = [new_r, new_c]

        # Nếu ô mới chứa bom, hiển thị bom (💣)
        if (new_r, new_c) in self.bombs:
            self.grid[new_r][new_c] = "💣"
            return True, "bomb"
        else:
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
        # Sử dụng defer để báo cho Discord biết bot đang xử lý
        await interaction.response.defer(thinking=True)

        # Kiểm tra tài khoản và số dư
        with getDbSession() as session:
            playerRepo = PlayerRepository(session)
            player = playerRepo.getById(interaction.user.id)
            if not player:
                await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!")
                return
            if bet <= 0:
                await interaction.followup.send("⚠️ Số tiền cược phải lớn hơn 0.")
                return
            if player.coin_balance < bet:
                await interaction.followup.send("⚠️ Số dư của bạn không đủ.")
                return

        # Khởi tạo game (không cần session ở đây)
        game = NarutoTrapGame(interaction.user, bet)
        initial_embed = discord.Embed(
            title="🔥 Naruto Trap Game 🔥",
            description=f"Tiền cược: **{bet} Ryo**\n\n{game.grid_to_str()}\n\nDi chuyển bằng emoji: ⬆️, ➡️, ⬅️",
            color=discord.Color.gold()
        )
        # Gửi tin nhắn phản hồi ban đầu
        await interaction.response.send_message(embed=initial_embed)
        message = await interaction.original_response()

        # Thêm reaction cho các hướng di chuyển
        directions = {
            "⬆️": "up",
            "➡️": "right",
            "⬅️": "left"
        }
        for emoji in directions.keys():
            await message.add_reaction(emoji)

        def check(reaction, user):
            return (
                user == interaction.user and
                str(reaction.emoji) in directions and
                reaction.message.id == message.id
            )

        # Vòng lặp di chuyển
        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
            except asyncio.TimeoutError:
                # Nếu hết thời gian chờ, edit tin nhắn với thông báo timeout và kết thúc game
                final_embed = discord.Embed(
                    title="⏰ Naruto Trap Game",
                    description=f"Hết thời gian chờ. Trò chơi kết thúc!\n\n{game.grid_to_str()}",
                    color=discord.Color.greyple()
                )
                await message.edit(embed=final_embed)
                break

            direction = directions[str(reaction.emoji)]
            valid, result = game.move_player(direction)

            # Xoá reaction của người chơi để cho phép lựa chọn lại
            try:
                await message.remove_reaction(reaction.emoji, user)
            except discord.HTTPException:
                pass

            # Cập nhật tin nhắn với grid mới
            new_content = f"🔥 Naruto Trap Game 🔥\nTiền cược: **{bet} Ryo**\n\n{game.grid_to_str()}\n\nDi chuyển: ⬆️, ➡️, ⬅️"
            await message.edit(content=new_content)

            if not valid:
                # Nếu di chuyển không hợp lệ, chỉ thông báo và tiếp tục vòng lặp
                continue

            if result == "bomb":
                # Nếu người chơi bị bom, cập nhật DB: trừ tiền cược
                with getDbSession() as session:
                    playerRepo = PlayerRepository(session)
                    player = playerRepo.getById(interaction.user.id)
                    player.coin_balance -= bet
                    session.commit()
                final_embed = discord.Embed(
                    title="💣 Naruto Trap Game",
                    description=f"Bạn rơi vào bẫy!\n\n{game.grid_to_str()}\n\nBạn mất hết **{bet} Ryo**.",
                    color=discord.Color.red()
                )
                await message.edit(embed=final_embed)
                break
            elif result == "win":
                # Nếu người chơi thắng, cập nhật DB: trừ tiền cược, cộng thưởng x2
                with getDbSession() as session:
                    playerRepo = PlayerRepository(session)
                    player = playerRepo.getById(interaction.user.id)
                    player.coin_balance = player.coin_balance - bet + (bet * 2)
                    session.commit()
                final_embed = discord.Embed(
                    title="🎉 Naruto Trap Game",
                    description=f"Chúc mừng! Bạn đã vượt qua chướng ngại và nhận thưởng: x2 tiền cược!\n\n{game.grid_to_str()}",
                    color=discord.Color.green()
                )
                await message.edit(embed=final_embed)
                break
            # Nếu kết quả là "moved", vòng lặp tiếp tục cập nhật grid

async def setup(bot: commands.Bot):
    await bot.add_cog(NarutoTrap(bot))
