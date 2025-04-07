import discord
from discord.ext import commands
from discord import app_commands
import random

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.playerWeaponRepository import PlayerWeaponRepository
from bot.repository.playerActiveSetupRepository import PlayerActiveSetupRepository
from bot.config.config import VS_IMAGE, NONE_CARD_IMAGE_URL, NONE_WEAPON_IMAGE_URL
from bot.config.imageMap import CARD_IMAGE_MAP, WEAPON_IMAGE_MAP
from bot.entity.player import Player  # model Player

class FightWith(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="fightwith", description="Pk vui với người chơi đã tag (không cập nhật rank)")
    @app_commands.describe(
        target="Tag của người chơi bạn muốn pk"
    )
    async def fightwith(self, interaction: discord.Interaction, target: discord.Member):
        await interaction.response.defer(thinking=True)
        attacker_id = interaction.user.id
        defender_id = target.id

        try:
            with getDbSession() as session:
                # Lấy các repository cần thiết
                playerRepo = PlayerRepository(session)
                cardRepo = PlayerCardRepository(session)
                weaponRepo = PlayerWeaponRepository(session)
                activeSetupRepo = PlayerActiveSetupRepository(session)
                
                # Lấy thông tin người tấn công
                attacker = playerRepo.getById(attacker_id)
                if not attacker:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!")
                    return
                
                # Kiểm tra active setup của người tấn công
                attackerSetup = activeSetupRepo.getByPlayerId(attacker_id)
                if not attackerSetup or attackerSetup.active_card_id is None:
                    await interaction.followup.send("⚠️ Bạn chưa lắp thẻ chiến đấu. Hãy dùng /setcard trước khi pk.")
                    return
                attackerCard = cardRepo.getById(attackerSetup.active_card_id)
                attackerWeapon = None
                if attackerSetup.weapon_slot1 is not None:
                    attackerWeapon = weaponRepo.getById(attackerSetup.weapon_slot1)
                
                # Tính sức mạnh của người tấn công
                try:
                    attackerCardStrength = attackerCard.template.base_power * attackerCard.level
                except Exception:
                    attackerCardStrength = 0
                attackerWeaponStrength = 0
                if attackerWeapon:
                    try:
                        attackerWeaponStrength = attackerWeapon.template.bonus_power * attackerWeapon.level
                    except Exception:
                        attackerWeaponStrength = 0
                attackerTotalStrength = attackerCardStrength + attackerWeaponStrength
                
                # Lấy thông tin người bị pk (defender)
                defender = playerRepo.getById(defender_id)
                if not defender:
                    await interaction.followup.send("⚠️ Người chơi được tag chưa đăng ký tài khoản.")
                    return
                defenderSetup = activeSetupRepo.getByPlayerId(defender_id)
                if not defenderSetup or defenderSetup.active_card_id is None:
                    await interaction.followup.send("⚠️ Người chơi được tag chưa sẵn sàng pk (chưa lắp thẻ).")
                    return
                defenderCard = cardRepo.getById(defenderSetup.active_card_id)
                defenderWeapon = None
                if defenderSetup.weapon_slot1 is not None:
                    defenderWeapon = weaponRepo.getById(defenderSetup.weapon_slot1)
                
                # Tính sức mạnh của người bị pk
                try:
                    defenderCardStrength = defenderCard.template.base_power * defenderCard.level
                except Exception:
                    defenderCardStrength = 0
                defenderWeaponStrength = 0
                if defenderWeapon:
                    try:
                        defenderWeaponStrength = defenderWeapon.template.bonus_power * defenderWeapon.level
                    except Exception:
                        defenderWeaponStrength = 0
                defenderTotalStrength = defenderCardStrength + defenderWeaponStrength
                
                # Xác định kết quả trận đấu (friendly pk: không cập nhật rank hay winning streak)
                if attackerTotalStrength > defenderTotalStrength:
                    result = "win"
                    outcome_text = f"Người tấn công (**{attacker.username}**) thắng!"
                elif attackerTotalStrength < defenderTotalStrength:
                    result = "loss"
                    outcome_text = f"Người tấn công (**{attacker.username}**) thua!"
                else:
                    result = "draw"
                    outcome_text = "Trận đấu hòa!"
                
                # Không cập nhật điểm rank hay chuỗi thắng – friendly pk chỉ để vui.
                # (Nếu cần ghi log hay lưu lại kết quả thì có thể thực hiện lưu riêng.)

                # Tạo embed cho thông tin người tấn công
                embed_attacker = discord.Embed(
                    title="Người tấn công",
                    description=f"Thông tin của người tấn công: **{attacker.username}**",
                    color=discord.Color.gold()
                )
                embed_attacker.add_field(name="Tên thẻ", value=f"**{attackerCard.template.name}**", inline=True)
                embed_attacker.add_field(name="Bậc thẻ", value=f"**{attackerCard.template.tier}**", inline=True)
                embed_attacker.add_field(name="Cấp thẻ", value=f"**{attackerCard.level}**", inline=True)
                # Thông tin vũ khí của attacker
                if attackerWeapon:
                    embed_attacker.add_field(name="Tên vũ khí", value=f"**{attackerWeapon.template.name}**", inline=True)
                    embed_attacker.add_field(name="Bậc vũ khí", value=f"**{attackerWeapon.template.grade}**", inline=True)
                    embed_attacker.add_field(name="Cấp vũ khí", value=f"**{attackerWeapon.level}**", inline=True)
                else:
                    embed_attacker.add_field(name="Vũ khí", value="Chưa cài đặt", inline=False)
                embed_attacker.add_field(name="Tổng sức mạnh", value=f"**{attackerTotalStrength}**", inline=True)
                embed_attacker.set_image(url=CARD_IMAGE_MAP.get(attackerCard.template.image_url, NONE_CARD_IMAGE_URL))
                embed_attacker.set_thumbnail(url=WEAPON_IMAGE_MAP.get(attackerWeapon.template.image_url, NONE_WEAPON_IMAGE_URL) if attackerWeapon else NONE_WEAPON_IMAGE_URL)
                embed_attacker.set_footer(text=f"Điểm rank: {attacker.rank_points}")
                
                # Embed VS: sử dụng hình ảnh từ VS_IMAGE
                embed_vs = discord.Embed(color=discord.Color.dark_red())
                embed_vs.set_image(url=VS_IMAGE)
                
                # Tạo embed cho thông tin người bị pk (defender)
                embed_defender = discord.Embed(
                    title="Người bị pk",
                    description=f"Thông tin của người bị pk: **{defender.username}**",
                    color=discord.Color.gold()
                )
                embed_defender.add_field(name="Tên thẻ", value=f"**{defenderCard.template.name}**", inline=True)
                embed_defender.add_field(name="Bậc thẻ", value=f"**{defenderCard.template.tier}**", inline=True)
                embed_defender.add_field(name="Cấp thẻ", value=f"**{defenderCard.level}**", inline=True)
                # Thông tin vũ khí của defender
                if defenderWeapon:
                    embed_defender.add_field(name="Tên vũ khí", value=f"**{defenderWeapon.template.name}**", inline=True)
                    embed_defender.add_field(name="Bậc vũ khí", value=f"**{defenderWeapon.template.grade}**", inline=True)
                    embed_defender.add_field(name="Cấp vũ khí", value=f"**{defenderWeapon.level}**", inline=True)
                else:
                    embed_defender.add_field(name="Vũ khí", value="Chưa cài đặt", inline=False)
                embed_defender.add_field(name="Tổng sức mạnh", value=f"**{defenderTotalStrength}**", inline=True)
                embed_defender.set_image(url=CARD_IMAGE_MAP.get(defenderCard.template.image_url, NONE_CARD_IMAGE_URL))
                embed_defender.set_thumbnail(url=WEAPON_IMAGE_MAP.get(defenderWeapon.template.image_url, NONE_WEAPON_IMAGE_URL) if defenderWeapon else NONE_WEAPON_IMAGE_URL)
                embed_defender.set_footer(text=f"Điểm rank: {defender.rank_points}")
                
                # Tạo embed kết quả trận đấu
                embed_result = discord.Embed(
                    title="Kết quả trận chiến (Friendly PK)",
                    description=(
                        f"**Kết quả:** {result.upper()}\n"
                        f"Người tấn công (**{attacker.username}**): **{attackerTotalStrength}**\n"
                        f"Người bị pk (**{defender.username}**): **{defenderTotalStrength}**\n\n"
                        f"{outcome_text}\n\n"
                        "Trận đấu này không làm thay đổi điểm rank hay chuỗi thắng."
                    ),
                    color=discord.Color.green() if result == "win" else discord.Color.red() if result == "loss" else discord.Color.orange()
                )
                
                # Gửi 4 embed cùng lúc
                await interaction.followup.send(embeds=[embed_attacker, embed_vs, embed_defender, embed_result])
        except Exception as e:
            print("❌ Lỗi khi xử lý fightwith:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(FightWith(bot))
