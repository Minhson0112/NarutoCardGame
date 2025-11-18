import math
import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
import traceback

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.playerWeaponRepository import PlayerWeaponRepository
from bot.services.help import get_card_effective_stats, get_weapon_effective_stats

# Số mục tối đa mỗi trang
ITEMS_PER_PAGE = 3

class CardInventoryView(View):
    def __init__(self, cards, author):
        super().__init__(timeout=300)
        self.author = author
        self.cards = sorted(
            cards,
            key=lambda c: get_card_effective_stats(c)["strength"],
            reverse=True
        )
        self.current_page = 0
        self.total_pages = math.ceil(len(cards) / ITEMS_PER_PAGE) if cards else 1
        self.embeds = self.generate_embeds()

    def generate_embeds(self):
        pages = []
        for page in range(self.total_pages):
            embed = discord.Embed(title="🎴 Kho Thẻ Bài", color=discord.Color.green())
            start = page * ITEMS_PER_PAGE
            end   = start + ITEMS_PER_PAGE
            subset = self.cards[start:end]

            if subset:
                lines = []
                for card in subset:
                    stats = get_card_effective_stats(card)
                    nameMsg = f"•🥷 **{card.template.name}** (Lv {card.level}) (🔒)\n" if card.locked else f"•🥷 **{card.template.name}** (Lv {card.level})\n"
                    lines.append(
                        f"{nameMsg}"
                        f"  ┣ **ID:** `{card.id}`\n"
                        f"  ┣ **Bậc:** {card.template.tier}\n"
                        f"  ┣ **Damage:** {stats['strength']}\n"
                        f"  ┣ **HP:** {stats['hp'] or 'N/A'}\n"
                        f"  ┣ **Giáp:** {stats['armor'] or 'N/A'}\n"
                        f"  ┣ **Tỉ lệ chí mạng:** {stats['crit_rate']:.0%}\n"
                        f"  ┣ **Né:** {stats['speed']:.0%}\n"
                        f"  ┣ **Chakra:** {stats['chakra']}\n"
                        f"  ┣ **Tanker:** {'✅' if card.template.first_position else '❌'}\n"
                        f"  ┣ **Hệ chakra:** {card.template.element}\n"
                        f"  ┗ **Số Lượng:** {card.quantity}\n"
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
        if self.current_page > 0:
            self.current_page -= 1
            await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)
        else:
            await interaction.response.send_message("Bạn đang ở trang đầu!", ephemeral=True)

    @discord.ui.button(label="Tiếp", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: Button):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)
        else:
            await interaction.response.send_message("Bạn đang ở trang cuối!", ephemeral=True)


class WeaponInventoryView(View):
    def __init__(self, weapons, author):
        super().__init__(timeout=300)
        self.author       = author
        self.weapons      = weapons
        self.current_page = 0
        self.total_pages  = math.ceil(len(weapons) / ITEMS_PER_PAGE) if weapons else 1
        self.embeds       = self.generate_embeds()

    def generate_embeds(self):
        pages = []
        for page in range(self.total_pages):
            embed = discord.Embed(title="🔪 Kho Vũ Khí", color=discord.Color.purple())
            start  = page * ITEMS_PER_PAGE
            subset = self.weapons[start : start + ITEMS_PER_PAGE]

            if subset:
                lines = []
                for weapon in subset:
                    stats = get_weapon_effective_stats(weapon)
                    # lấy ra những key,val mà val!=None và !=0
                    buffs = [
                        (k.replace("bonus_", "").replace("_", " ").title(),
                        f"{v:.0%}" if isinstance(v, float) else str(v))
                        for k, v in stats.items() if v
                    ]

                    # header + bậc
                    block = [
                        f"•🔪 **{weapon.template.name}** (Lv {weapon.level})",
                        f"  ┣ **ID:** `{weapon.id}`",
                        f"  ┣ **Bậc:** {weapon.template.grade}",
                        f"  ┣ **Số Lượng:** {weapon.quantity}"
                    ]
                    # thêm danh sách buffs
                    for i, (label, val) in enumerate(buffs):
                        bullet = "┗" if i == len(buffs)-1 else "┣"
                        block.append(f"  {bullet} **{label}:** {val}")

                    lines.append("\n".join(block))

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
        if self.current_page > 0:
            self.current_page -= 1
            await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)
        else:
            await interaction.response.send_message("Bạn đang ở trang đầu!", ephemeral=True)

    @discord.ui.button(label="Tiếp", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: Button):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)
        else:
            await interaction.response.send_message("Bạn đang ở trang cuối!", ephemeral=True)


class Inventory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="inventory", description="Hiển thị kho đồ của bạn")
    async def inventory(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        player_id = interaction.user.id

        try:
            with getDbSession() as session:
                player_repo = PlayerRepository(session)
                card_repo   = PlayerCardRepository(session)
                weapon_repo = PlayerWeaponRepository(session)

                player = player_repo.getById(player_id)
                if not player:
                    await interaction.followup.send(
                        "⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng `/register` trước nhé!"
                    )
                    return

                cards   = card_repo.getByPlayerId(player_id)
                weapons = weapon_repo.getByPlayerId(player_id)

                card_view   = CardInventoryView(cards, interaction.user)
                weapon_view = WeaponInventoryView(weapons, interaction.user)

                await interaction.followup.send(embed=card_view.embeds[0], view=card_view)
                await interaction.followup.send(embed=weapon_view.embeds[0], view=weapon_view)

        except Exception as e:
            tb = traceback.format_exc()
            # Gửi riêng cho user (ephemeral) để không spam kênh chung
            await interaction.followup.send(
                f"❌ Có lỗi xảy ra:\n```{tb}```",
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(Inventory(bot))
