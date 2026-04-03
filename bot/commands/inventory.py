import math
import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
import traceback
from sqlalchemy import func

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.playerWeaponRepository import PlayerWeaponRepository
<<<<<<< HEAD
from bot.services.help import get_card_effective_stats, get_weapon_effective_stats
=======
from bot.services.help import get_card_effective_stats
from bot.entity.playerCards import PlayerCard
>>>>>>> a810d81 (cập nhập chợ đen và thuế)

ITEMS_PER_PAGE = 4

class InventoryView(View):
<<<<<<< HEAD
    def __init__(self, cards, weapons, author):
=======
    def __init__(self, grouped_cards, weapons, author):
>>>>>>> a810d81 (cập nhập chợ đen và thuế)
        super().__init__(timeout=300)
        self.author = author
        self.cards = grouped_cards
        self.weapons = weapons
        self.mode = "cards"
        self.current_page = 0
        self._sync_labels()

<<<<<<< HEAD
    def get_total_pages(self) -> int:
=======
    def _sync_labels(self):
        for child in self.children:
            if isinstance(child, Button):
                if child.custom_id == "inv.prev": child.label = "Trước"
                elif child.custom_id == "inv.next": child.label = "Sau"
                elif child.custom_id == "inv.toggle":
                    child.label = "Sang Vũ Khí" if self.mode == "cards" else "Sang Thẻ Bài"

    def get_total_pages(self):
>>>>>>> a810d81 (cập nhập chợ đen và thuế)
        data = self.cards if self.mode == "cards" else self.weapons
        return math.ceil(len(data) / ITEMS_PER_PAGE) if data else 1

    def build_embed(self):
        total_p = self.get_total_pages()
        start = self.current_page * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE

        if self.mode == "cards":
<<<<<<< HEAD
            embed = discord.Embed(title="🎴 Kho Thẻ Bài", color=discord.Color.green())
=======
            embed = discord.Embed(title=f"🎒 Kho Thẻ Bài - {self.author.display_name}", color=discord.Color.green())
>>>>>>> a810d81 (cập nhập chợ đen và thuế)
            subset = self.cards[start:end]
            if subset:
<<<<<<< HEAD
                lines = []
                for card in subset:
                    stats = get_card_effective_stats(card)
                    nameMsg = (
                        f"•🥷 **{card.template.name}** (Lv {card.level}) (🔒)\n"
                        if card.locked
                        else f"•🥷 **{card.template.name}** (Lv {card.level})\n"
                    )
                    lines.append(
                        f"{nameMsg}"
                        f"  ┣ **ID:** `{card.id}`\n"
                        f"  ┣ **Bậc:** {card.template.tier}\n"
                        f"  ┣ **Tanker:** {'✅' if card.template.first_position else '❌'}\n"
                        f"  ┗ **Số Lượng:** {card.quantity}\n"
                    )
                embed.description = "\n\n".join(lines)
            else:
                embed.description = "Không có thẻ nào."

        else:
            embed = discord.Embed(title="🔪 Kho Vũ Khí", color=discord.Color.purple())
=======
                desc = []
                for card, count in subset:
                    tags = []
                    if card.locked: tags.append("🔒")
                    if card.equipped: tags.append("⚔️")
                    t_str = " ".join(tags)

                    line = (
                        f"ID: # {card.id} | ✅ {card.template.name} (Lv {card.level}) {t_str}\n"
                        f"┣ 🏷️ Tier: {card.template.tier} | 📦 SL: {count}\n"
                        f"┗ 👤 Chủ sở hữu: <@{self.author.id}>\n"
                        f"━━━━━━━━━━━━━━━━━━"
                    )
                    desc.append(line)
                embed.description = "\n".join(desc)
            else:
                embed.description = "Kho thẻ bài hiện đang trống."
        else:
            embed = discord.Embed(title=f"⚔️ Kho Vũ Khí - {self.author.display_name}", color=discord.Color.purple())
>>>>>>> a810d81 (cập nhập chợ đen và thuế)
            subset = self.weapons[start:end]
            if subset:
<<<<<<< HEAD
                lines = []
                for weapon in subset:
                    stats = get_weapon_effective_stats(weapon)
                    buffs = [
                        (
                            k.replace("bonus_", "").replace("_", " ").title(),
                            f"{v:.0%}" if isinstance(v, float) else str(v)
                        )
                        for k, v in stats.items() if v
                    ]

                    block = [
                        f"•🔪 **{weapon.template.name}** (Lv {weapon.level})",
                        f"  ┣ **ID:** `{weapon.id}`",
                        f"  ┣ **Bậc:** {weapon.template.grade}",
                        f"  ┣ **Số Lượng:** {weapon.quantity}"
                    ]

                    for i, (label, val) in enumerate(buffs):
                        bullet = "┗" if i == len(buffs) - 1 else "┣"
                        block.append(f"  {bullet} **{label}:** {val}")

                    lines.append("\n".join(block))

                embed.description = "\n\n".join(lines)
            else:
                embed.description = "Không có vũ khí nào."

        embed.set_footer(text=f"Trang {self.current_page + 1}/{total_pages}")
        return embed

    def sync_toggle_button_label(self, button: Button) -> None:
        if self.mode == "cards":
            button.label = "Kho vũ khí"
        else:
            button.label = "Kho thẻ"

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.author.id

    @discord.ui.button(label="Trước", style=discord.ButtonStyle.primary)
    async def previous_page(self, interaction: discord.Interaction, button: Button):
        if self.current_page > 0:
            self.current_page -= 1
            await interaction.response.edit_message(embed=self.build_embed(), view=self)
        else:
            await interaction.response.send_message("Bạn đang ở trang đầu!", ephemeral=True)

    @discord.ui.button(label="Tiếp", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: Button):
        total_pages = self.get_total_pages()
        if self.current_page < total_pages - 1:
            self.current_page += 1
            await interaction.response.edit_message(embed=self.build_embed(), view=self)
        else:
            await interaction.response.send_message("Bạn đang ở trang cuối!", ephemeral=True)

    @discord.ui.button(label="Kho vũ khí", style=discord.ButtonStyle.secondary)
    async def toggle_inventory(self, interaction: discord.Interaction, button: Button):
        self.mode = "weapons" if self.mode == "cards" else "cards"

        total_pages = self.get_total_pages()
        if self.current_page >= total_pages:
            self.current_page = max(0, total_pages - 1)

        self.sync_toggle_button_label(button)
=======
                desc = []
                for w in subset:
                    line = (
                        f"ID: # {w.id} | ⚔️ {w.template.name}\n"
                        f"┗ 📦 Số lượng: {w.quantity}\n"
                        f"━━━━━━━━━━━━━━━━━━"
                    )
                    desc.append(line)
                embed.description = "\n".join(desc)
            else:
                embed.description = "Kho vũ khí hiện đang trống."

        embed.set_footer(text=f"Trang {self.current_page + 1}/{total_p}")
        return embed

    @discord.ui.button(label="Trước", style=discord.ButtonStyle.primary, custom_id="inv.prev")
    async def prev(self, interaction: discord.Interaction, button: Button):
        if self.current_page > 0:
            self.current_page -= 1
            await interaction.response.edit_message(embed=self.build_embed(), view=self)

    @discord.ui.button(label="Sau", style=discord.ButtonStyle.primary, custom_id="inv.next")
    async def next(self, interaction: discord.Interaction, button: Button):
        if self.current_page < self.get_total_pages() - 1:
            self.current_page += 1
            await interaction.response.edit_message(embed=self.build_embed(), view=self)

    @discord.ui.button(label="Đổi", style=discord.ButtonStyle.secondary, custom_id="inv.toggle")
    async def toggle(self, interaction: discord.Interaction, button: Button):
        self.mode = "weapons" if self.mode == "cards" else "cards"
        self.current_page = 0
        self._sync_labels()
>>>>>>> a810d81 (cập nhập chợ đen và thuế)
        await interaction.response.edit_message(embed=self.build_embed(), view=self)

class Inventory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

<<<<<<< HEAD
    @app_commands.command(name="inventory", description="Hiển thị kho đồ của bạn")
    async def inventory(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        player_id = interaction.user.id

=======
    @app_commands.command(name="inventory", description="Xem kho đồ cá nhân")
    async def inventory(self, interaction: discord.Interaction):
        await interaction.response.defer()
>>>>>>> a810d81 (cập nhập chợ đen và thuế)
        try:
            with getDbSession() as session:
                # Lấy dữ liệu gộp
                q_res = (
                    session.query(func.min(PlayerCard.id), func.sum(PlayerCard.quantity))
                    .filter(PlayerCard.player_id == interaction.user.id)
                    .filter(PlayerCard.status.in_(['INVENTORY', None]))
                    .group_by(PlayerCard.card_key, PlayerCard.level, PlayerCard.locked, PlayerCard.equipped)
                    .all()
                )
                
                cards_list = []
                for rid, cnt in q_res:
                    c_obj = session.query(PlayerCard).filter(PlayerCard.id == rid).first()
                    if c_obj: cards_list.append((c_obj, cnt))
                
                # Sắp xếp theo sức mạnh
                cards_list.sort(key=lambda x: get_card_effective_stats(x[0])["strength"], reverse=True)
                
                weapons = PlayerWeaponRepository(session).getByPlayerId(interaction.user.id)

<<<<<<< HEAD
                player = player_repo.getById(player_id)
                if not player:
                    await interaction.followup.send(
                        "⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng `/register` trước nhé!"
                    )
                    return

                cards = card_repo.getByPlayerId(player_id)
                weapons = weapon_repo.getByPlayerId(player_id)

                view = InventoryView(cards, weapons, interaction.user)
=======
                if not cards_list and not weapons:
                    return await interaction.followup.send("🎒 Kho đồ của bạn hiện đang trống.")

                view = InventoryView(cards_list, weapons, interaction.user)
>>>>>>> a810d81 (cập nhập chợ đen và thuế)
                await interaction.followup.send(embed=view.build_embed(), view=view)
        except Exception:
            await interaction.followup.send(f"❌ Lỗi truy xuất kho đồ.")

async def setup(bot):
    await bot.add_cog(Inventory(bot))
