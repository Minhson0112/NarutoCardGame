import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.playerWeaponRepository import PlayerWeaponRepository

class Inventory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="inventory", description="Hiển thị kho đồ của bạn")
    async def inventory(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        playerId = interaction.user.id

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                playerCardRepo = PlayerCardRepository(session)
                playerWeaponRepo = PlayerWeaponRepository(session)

                # Lấy thông tin người chơi
                player = playerRepo.getById(playerId)
                if not player:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng `/register` trước nhé!")
                    return

                # Embed 1: Thông tin tài khoản
                embedPlayer = discord.Embed(
                    title="Thông tin tài khoản",
                    color=discord.Color.blue()
                )
                embedPlayer.add_field(name="Tên", value=interaction.user.display_name, inline=False)
                embedPlayer.add_field(name="Số dư", value=f"{player.coin_balance:,} Ryo", inline=False)
                embedPlayer.add_field(name="Điểm rank", value=str(player.rank_points), inline=False)

                # Embed 2: Kho Thẻ Bài
                cards = playerCardRepo.getByPlayerId(playerId)
                if cards:
                    # Sắp xếp theo sức mạnh giảm dần: sức mạnh = base_power * level
                    cards = sorted(cards, key=lambda card: (card.template.base_power * card.level) if card.template.base_power is not None else 0, reverse=True)
                    
                    cardLines = []
                    for card in cards:
                        try:
                            strength = card.template.base_power * card.level
                        except Exception:
                            strength = "N/A"
                        
                        cardLines.append(
                            f"• 🥷 **{card.template.name}**\n"
                            f"  ┣ **Bậc:** {card.template.tier}\n"
                            f"  ┣ **Cấp:** {card.level}\n"
                            f"  ┣ **Sức mạnh:** {strength}\n"
                            f"  ┗ **Số Lượng:** {card.quantity}"
                        )
                    
                    cardDescription = "\n\n".join(cardLines)
                else:
                    cardDescription = "Kho thẻ trống."

                embedCards = discord.Embed(
                    title="Kho Thẻ Bài",
                    description=cardDescription,
                    color=discord.Color.green()
                )

                # Embed 3: Kho Vũ Khí
                weapons = playerWeaponRepo.getByPlayerId(playerId)
                if weapons:
                    # Sắp xếp theo sức mạnh giảm dần: sức mạnh = bonus_power * level
                    weapons = sorted(weapons, key=lambda weapon: (weapon.template.bonus_power * weapon.level) if weapon.template.bonus_power is not None else 0, reverse=True)
                    
                    weaponLines = []
                    for weapon in weapons:
                        try:
                            strength = weapon.template.bonus_power * weapon.level
                        except Exception:
                            strength = "N/A"
                        
                        weaponLines.append(
                            f"• 🔪 **{weapon.template.name}**\n"
                            f"  ┣ **Grade:** {weapon.template.grade}\n"
                            f"  ┣ **Level:** {weapon.level}\n"
                            f"  ┣ **Sức Mạnh:** {strength}\n"
                            f"  ┗ **Số Lượng:** {weapon.quantity}"
                        )
                    
                    weaponDescription = "\n\n".join(weaponLines)
                else:
                    weaponDescription = "Kho vũ khí trống."

                embedWeapons = discord.Embed(
                    title="Kho Vũ Khí",
                    description=weaponDescription,
                    color=discord.Color.purple()
                )

                # Gửi 3 embed cùng lúc
                await interaction.followup.send(embeds=[embedPlayer, embedCards, embedWeapons])
        except Exception as e:
            print("❌ Lỗi khi xử lý inventory:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(Inventory(bot))
