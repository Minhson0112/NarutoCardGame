import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository

class Rename(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="rename", description="Đổi tên của bạn (tối đa 16 ký tự)")
    @app_commands.describe(new_name="Tên mới của bạn (tối đa 16 ký tự)")
    async def rename(self, interaction: discord.Interaction, new_name: str):
        # Kiểm tra độ dài tên mới
        if len(new_name) > 16:
            await interaction.response.send_message("⚠️ Tên mới không được vượt quá 16 ký tự.", ephemeral=True)
            return
        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                player = playerRepo.getById(interaction.user.id)
                if not player:
                    await interaction.response.send_message(
                        "⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!", ephemeral=True
                    )
                    return
                # Cập nhật tên mới
                player.username = new_name
                session.commit()
                await interaction.response.send_message(
                    f"✅ Đổi tên thành công! Tên mới của bạn: **{new_name}**", ephemeral=True
                )
        except Exception as e:
            print("❌ Lỗi khi đổi tên:", e)
            await interaction.response.send_message(
                "❌ Có lỗi xảy ra trong quá trình đổi tên. Vui lòng thử lại sau.", ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Rename(bot))
