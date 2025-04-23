import os
import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.playerWeaponRepository import PlayerWeaponRepository
from bot.repository.playerActiveSetupRepository import PlayerActiveSetupRepository

from bot.services.render import renderImage
from bot.services.help import get_card_effective_stats, get_weapon_effective_stats
from bot.config.imageMap import (
    CARD_IMAGE_LOCAL_PATH_MAP,
    WEAPON_IMAGE_LOCAL_PATH_MAP,
    NON_WEAPON_PATH,
    NON_CARD_PATH,
    BG
)

class ShowProfile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="showprofile",
        description="Hiển thị hồ sơ chiến đấu (3 thẻ + 3 vũ khí) của bạn"
    )
    async def showProfile(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        player_id = interaction.user.id

        try:
            with getDbSession() as session:
                playerRepo      = PlayerRepository(session)
                cardRepo        = PlayerCardRepository(session)
                weaponRepo      = PlayerWeaponRepository(session)
                setupRepo       = PlayerActiveSetupRepository(session)

                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send(
                        "⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng `/register` trước nhé!"
                    )
                    return

                setup = setupRepo.getByPlayerId(player_id)
                # Chuẩn bị slot
                card_ids   = [setup.card_slot1, setup.card_slot2, setup.card_slot3] if setup else [None]*3
                weapon_ids = [setup.weapon_slot1, setup.weapon_slot2, setup.weapon_slot3] if setup else [None]*3

                # Lưu đường dẫn ảnh
                card_image_paths = []
                weapon_image_paths = []
                cards_info = []
                weapons_info = []
                total_strength = 0

                # Xử lý thẻ
                slot_names = ["Tanker", "Middle", "Back"]
                for idx, cid in enumerate(card_ids):
                    if cid:
                        card = cardRepo.getById(cid)
                        stats = get_card_effective_stats(card)
                        total_strength += stats["strength"]
                        card_image_paths.append(
                            CARD_IMAGE_LOCAL_PATH_MAP.get(card.template.image_url, NON_CARD_PATH)
                        )
                        cards_info.append((slot_names[idx], card, stats))
                    else:
                        cards_info.append((slot_names[idx], None, None))
                        card_image_paths.append(NON_CARD_PATH)

                # Xử lý vũ khí
                for idx, wid in enumerate(weapon_ids):
                    if wid:
                        weapon = weaponRepo.getById(wid)
                        stats = get_weapon_effective_stats(weapon)
                        # tính strength để cộng vào tổng: dùng bonus_damage × level
                        bonus = stats["bonus_damage"] or 0
                        lvl = weapon.level or 1
                        total_strength += int(bonus * lvl)
                        weapon_image_paths.append(
                            WEAPON_IMAGE_LOCAL_PATH_MAP.get(weapon.template.image_url, NON_WEAPON_PATH)
                        )
                        weapons_info.append((idx+1, weapon, stats))
                    else:
                        weapons_info.append((idx+1, None, None))
                        weapon_image_paths.append(NON_WEAPON_PATH)

                # Render composite image
                image_buffer  = renderImage(
                    card_image_paths[0], card_image_paths[1], card_image_paths[2],
                    weapon_image_paths[0], weapon_image_paths[1], weapon_image_paths[2],
                    BG
                )
                filename = f"{player_id}.png"

                # Build embed description
                lines = []
                # Thẻ
                for slot_name, card, stats in cards_info:
                    if card:
                        lines.append(
                            f"**{slot_name}:** {card.template.name} (Lv {card.level})\n"
                            f"  ┣ HP♥️: {stats['hp']}\n"
                            f"  ┣ Damage⚔️: {stats['strength']}\n"
                            f"  ┣ Bậc🎖️: {card.template.tier}\n"
                            f"  ┗ Hệ📜: {card.template.element}"
                        )
                    else:
                        lines.append(f"**{slot_name}:** Chưa lắp thẻ")
                lines.append("")  # ngăn cách thẻ và vũ khí

                slot_names = ["Tanker", "Middle", "Back"]
                for slot_idx, weapon, stats in weapons_info:
                    if weapon:
                        # Tạo danh sách bonus items (key, val, pretty_name, formatted_val)
                        bonus_items = []
                        for key, val in stats.items():
                            if val not in (None, 0):
                                pretty = key.replace("bonus_", "").replace("_", " ").title()
                                if isinstance(val, float):
                                    formatted = f"{val:.0%}"
                                else:
                                    formatted = str(val)
                                bonus_items.append((pretty, formatted))

                        # Bắt đầu dòng header
                        block = [
                            f"**Vũ khí {slot_idx} (Thẻ {slot_names[slot_idx-1]}):** {weapon.template.name} (Lv {weapon.level})",
                            f"  ┣ Bậc: {weapon.template.grade}"
                        ]

                        # Thêm từng bonus với kí tự bullet
                        for i, (pretty, formatted) in enumerate(bonus_items):
                            bullet = "┗" if i == len(bonus_items)-1 else "┣"
                            block.append(f"  {bullet} **{pretty}:** {formatted}")

                        # Gom thành 1 string
                        lines.append("\n".join(block))
                    else:
                        lines.append(f"**Vũ khí {slot_idx} (Thẻ {slot_names[slot_idx-1]}):** Chưa lắp vũ khí")

                lines.append("")  # ngăn cách

                embed = discord.Embed(
                    title="🛡️ Hồ sơ Chiến Đấu của bạn",
                    description="\n\n".join(lines),
                    color=discord.Color.gold()
                )
                embed.set_image(url=f"attachment://{filename}")
                embed.set_footer(
                    text=f"Số dư: {player.coin_balance:,} Ryo | Điểm rank: {player.rank_points}"
                )

                await interaction.followup.send(
                    embed=embed,
                    file=discord.File(fp=image_buffer, filename=filename)
                )

        except Exception as e:
            await interaction.followup.send(
                f"❌ Lỗi khi xử lý ShowProfile:\n```{e}```",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(ShowProfile(bot))
