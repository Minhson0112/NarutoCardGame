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
from bot.config.config import LEVEL_CONFIG
from bot.services.i18n import t


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
        guild_id = interaction.guild.id if interaction.guild else None

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                cardRepo = PlayerCardRepository(session)
                weaponRepo = PlayerWeaponRepository(session)
                setupRepo = PlayerActiveSetupRepository(session)

                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send(
                        t(guild_id, "showprofile.not_registered")
                    )
                    return

                setup = setupRepo.getByPlayerId(player_id)

                card_ids = [setup.card_slot1, setup.card_slot2, setup.card_slot3] if setup else [None] * 3
                weapon_ids = [setup.weapon_slot1, setup.weapon_slot2, setup.weapon_slot3] if setup else [None] * 3

                card_image_paths = []
                weapon_image_paths = []
                cards_info = []
                weapons_info = []
                total_strength = 0

                slot_names = [
                    t(guild_id, "showprofile.section.cards.slot.tanker"),
                    t(guild_id, "showprofile.section.cards.slot.middle"),
                    t(guild_id, "showprofile.section.cards.slot.back"),
                ]

                # Cards
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

                # Weapons
                for idx, wid in enumerate(weapon_ids):
                    if wid:
                        weapon = weaponRepo.getById(wid)
                        stats = get_weapon_effective_stats(weapon)
                        bonus = stats.get("bonus_damage") or 0
                        lvl = weapon.level or 1
                        total_strength += int(bonus * lvl)
                        weapon_image_paths.append(
                            WEAPON_IMAGE_LOCAL_PATH_MAP.get(weapon.template.image_url, NON_WEAPON_PATH)
                        )
                        weapons_info.append((idx + 1, weapon, stats))
                    else:
                        weapons_info.append((idx + 1, None, None))
                        weapon_image_paths.append(NON_WEAPON_PATH)

                image_buffer = renderImage(
                    card_image_paths[0], card_image_paths[1], card_image_paths[2],
                    weapon_image_paths[0], weapon_image_paths[1], weapon_image_paths[2],
                    BG
                )
                filename = f"{player_id}.png"

                lines = []

                # Card section
                for slot_name, card, stats in cards_info:
                    if card:
                        lines.append(
                            t(
                                guild_id,
                                "showprofile.card.line",
                                slotName=slot_name,
                                cardName=card.template.name,
                                level=card.level,
                                hp=stats["hp"],
                                damage=stats["strength"],
                                tier=card.template.tier,
                                element=card.template.element
                            )
                        )
                    else:
                        lines.append(t(guild_id, "showprofile.card.empty", slotName=slot_name))

                lines.append("")

                # Weapon section
                for slot_idx, weapon, stats in weapons_info:
                    slot_name = slot_names[slot_idx - 1]
                    weapon_title = t(guild_id, "showprofile.weapon.title", slotIndex=slot_idx, slotName=slot_name)

                    if weapon:
                        header = t(
                            guild_id,
                            "showprofile.weapon.line.header",
                            weaponTitle=weapon_title,
                            weaponName=weapon.template.name,
                            level=weapon.level,
                            grade=weapon.template.grade
                        )

                        bonus_items = []
                        for key, val in stats.items():
                            if val not in (None, 0):
                                pretty = key.replace("bonus_", "").replace("_", " ").title()
                                if isinstance(val, float):
                                    formatted = f"{val:.0%}"
                                else:
                                    formatted = str(val)
                                bonus_items.append((pretty, formatted))

                        block = [header]
                        for i, (pretty, formatted) in enumerate(bonus_items):
                            bullet = "┗" if i == len(bonus_items) - 1 else "┣"
                            block.append(
                                t(
                                    guild_id,
                                    "showprofile.weapon.bonus_item",
                                    bullet=bullet,
                                    name=pretty,
                                    value=formatted
                                )
                            )

                        lines.append("\n".join(block))
                    else:
                        lines.append(t(guild_id, "showprofile.weapon.empty", weaponTitle=weapon_title))

                lines.append("")

                # Level / EXP bar
                exp = player.exp or 0
                thresholds = sorted(int(k) for k in LEVEL_CONFIG.keys())
                current_level = 0
                prev_thresh = 0
                next_thresh = None

                for th in thresholds:
                    lvl = LEVEL_CONFIG[str(th)]
                    if exp >= th:
                        current_level = lvl
                        prev_thresh = th
                    elif next_thresh is None:
                        next_thresh = th

                bar_length = 20
                if next_thresh:
                    ratio = (exp - prev_thresh) / (next_thresh - prev_thresh)
                    filled = int(ratio * bar_length)
                    bar = "█" * filled + "░" * (bar_length - filled)
                    exp_text = f"{exp - prev_thresh}/{next_thresh - prev_thresh}"

                    lines.append(t(guild_id, "showprofile.level.current", level=current_level))
                    lines.append(
                        t(
                            guild_id,
                            "showprofile.level.to_next",
                            nextLevel=current_level + 1,
                            bar=bar,
                            expText=exp_text
                        )
                    )
                else:
                    bar = "█" * bar_length
                    exp_text = str(exp)

                    lines.append(t(guild_id, "showprofile.level.current", level=current_level))
                    lines.append(t(guild_id, "showprofile.level.max", bar=bar, expText=exp_text))

                embed = discord.Embed(
                    title=t(guild_id, "showprofile.title"),
                    description="\n\n".join(lines),
                    color=discord.Color.gold()
                )
                embed.set_image(url=f"attachment://{filename}")
                embed.set_footer(
                    text=t(
                        guild_id,
                        "showprofile.footer",
                        coin=player.coin_balance,
                        rankPoints=player.rank_points
                    )
                )

                await interaction.followup.send(
                    embed=embed,
                    file=discord.File(fp=image_buffer, filename=filename)
                )

        except Exception as e:
            await interaction.followup.send(
                t(guild_id, "showprofile.error", error=str(e)),
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(ShowProfile(bot))
