import math
import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.playerWeaponRepository import PlayerWeaponRepository

# Số mục tối đa mỗi trang
ITEMS_PER_PAGE = 5

class CardInventoryView(View):
    def __init__(self, cards, author):
        super().__init__(timeout=300)
        self.author = author
        self.cards = cards
        self.current_page = 0
        self.total_pages = math.ceil(len(cards) / ITEMS_PER_PAGE) if cards else 1
        self.embeds = self.generate_embeds()

    def generate_embeds(self):
        pages = []
        for page in range(self.total_pages):
            embed = discord.Embed(title="Kho Thẻ Bài", color=discord.Color.green())
            start_index = page * ITEMS_PER_PAGE
            end_index = start_index + ITEMS_PER_PAGE
            cards_subset = self.cards[start_index:end_index]
            if cards_subset:
                lines = []
                for card in cards_subset:
                    try:
                        strength = card.template.base_power * card.level
                    except Exception:
                        strength = "N/A"
                    lines.append(
                        f"•🥷 **{card.template.name}**\n"
                        f"  ┣ **Bậc:** {card.template.tier}\n"
                        f"  ┣ **Cấp:** {card.level}\n"
                        f"  ┣ **Sức mạnh:** {strength}\n"
                        f"  ┗ **Số Lượng:** {card.quantity}"
                    )
                embed.description = "\n\n".join(lines)
            else:
                embed.description = "Không có thẻ nào."
            embed.set_footer(text=f"Trang {page+1}/{self.total_pages}")
            pages.append(embed)
        return pages

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.author.id

    @discord.ui.button(label="Trước", style=discord.ButtonStyle.primary)
    async def previous_page(self, interaction: discord.Interaction, button: Button):
        try:
            if self.current_page > 0:
                self.current_page -= 1
                await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)
            else:
                await interaction.response.send_message("Bạn đang ở trang đầu!", ephemeral=True)
        except Exception:
            await interaction.response.send_message("❌ Lỗi khi chuyển trang.", ephemeral=True)

    @discord.ui.button(label="Tiếp", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: Button):
        try:
            if self.current_page < self.total_pages - 1:
                self.current_page += 1
                await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)
            else:
                await interaction.response.send_message("Bạn đang ở trang cuối!", ephemeral=True)
        except Exception:
            await interaction.response.send_message("❌ Lỗi khi chuyển trang.", ephemeral=True)

class WeaponInventoryView(View):
    def __init__(self, weapons, author):
        super().__init__(timeout=300)
        self.author = author
        self.weapons = weapons
        self.current_page = 0
        self.total_pages = math.ceil(len(weapons) / ITEMS_PER_PAGE) if weapons else 1
        self.embeds = self.generate_embeds()

    def generate_embeds(self):
        pages = []
        for page in range(self.total_pages):
            embed = discord.Embed(title="Kho Vũ Khí", color=discord.Color.purple())
            start_index = page * ITEMS_PER_PAGE
            end_index = start_index + ITEMS_PER_PAGE
            weapons_subset = self.weapons[start_index:end_index]
            if weapons_subset:
                lines = []
                for weapon in weapons_subset:
                    try:
                        strength = weapon.template.bonus_power * weapon.level
                    except Exception:
                        strength = "N/A"
                    lines.append(
                        f"•🔪 **{weapon.template.name}**\n"
                        f"  ┣ **Bậc:** {weapon.template.grade}\n"
                        f"  ┣ **Level:** {weapon.level}\n"
                        f"  ┣ **Sức Mạnh:** {strength}\n"
                        f"  ┗ **Số Lượng:** {weapon.quantity}"
                    )
                embed.description = "\n\n".join(lines)
            else:
                embed.description = "Không có vũ khí nào."
            embed.set_footer(text=f"Trang {page+1}/{self.total_pages}")
            pages.append(embed)
        return pages

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.author.id

    @discord.ui.button(label="Trước", style=discord.ButtonStyle.primary)
    async def previous_page(self, interaction: discord.Interaction, button: Button):
        try:
            if self.current_page > 0:
                self.current_page -= 1
                await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)
            else:
                await interaction.response.send_message("Bạn đang ở trang đầu!", ephemeral=True)
        except Exception:
            await interaction.response.send_message("❌ Lỗi khi chuyển trang.", ephemeral=True)

    @discord.ui.button(label="Tiếp", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: Button):
        try:
            if self.current_page < self.total_pages - 1:
                self.current_page += 1
                await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)
            else:
                await interaction.response.send_message("Bạn đang ở trang cuối!", ephemeral=True)
        except Exception:
            await interaction.response.send_message("❌ Lỗi khi chuyển trang.", ephemeral=True)

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

                # Kiểm tra xem người dùng đã đăng ký chưa
                player = playerRepo.getById(playerId)
                if not player:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng `/register` trước nhé!")
                    return

                # Lấy dữ liệu kho thẻ và kho vũ khí
                cards = playerCardRepo.getByPlayerId(playerId)
                weapons = playerWeaponRepo.getByPlayerId(playerId)

                # Nếu cần, sắp xếp theo tiêu chí (ví dụ: theo sức mạnh giảm dần)
                if cards:
                    cards = sorted(
                        cards,
                        key=lambda card: (card.template.base_power * card.level) if card.template.base_power is not None else 0,
                        reverse=True
                    )
                if weapons:
                    weapons = sorted(
                        weapons,
                        key=lambda weapon: (weapon.template.bonus_power * weapon.level) if weapon.template.bonus_power is not None else 0,
                        reverse=True
                    )

                # Tạo view riêng cho thẻ và vũ khí
                card_view = CardInventoryView(cards, interaction.user)
                weapon_view = WeaponInventoryView(weapons, interaction.user)

                # Gửi 2 message, mỗi message có embed và view phân trang riêng
                await interaction.followup.send(embed=card_view.embeds[0], view=card_view)
                await interaction.followup.send(embed=weapon_view.embeds[0], view=weapon_view)
        except Exception:
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(Inventory(bot))
