import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.entity.playerCards import PlayerCard

class LevelUpCard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="levelupcard", description="Nâng cấp thẻ của bạn (tăng 1 cấp)")
    @app_commands.describe(
        card_id="ID thẻ bạn muốn nâng cấp (xem trong /inventory)"
    )
    async def levelUp(self, interaction: discord.Interaction, card_id: int):
        await interaction.response.defer(thinking=True)
        playerId = interaction.user.id

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                cardRepo   = PlayerCardRepository(session)

                # 1) Kiểm tra người chơi đã đăng ký
                player = playerRepo.getById(playerId)
                if not player:
                    await interaction.followup.send(
                        "⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!"
                    )
                    return

                # 2) Lấy thẻ theo ID
                mainCardCandidate = cardRepo.getById(card_id)
                if not mainCardCandidate or mainCardCandidate.player_id != playerId:
                    await interaction.followup.send(
                        f"⚠️ Bạn không sở hữu thẻ với ID `{card_id}`. Kiểm tra lại trong /inventory."
                    )
                    return

                card_name     = mainCardCandidate.template.name
                current_level = mainCardCandidate.level
                desired_level = current_level + 1

                # 3) Giới hạn max level
                if desired_level > 50:
                    await interaction.followup.send(
                        f"⚠️ Cấp thẻ lớn nhất có thể nâng cấp là 50. Thẻ này đang ở cấp {current_level}."
                    )
                    return

                # 4) Lấy tất cả các bản ghi cùng card_key của player
                cards = cardRepo.getByPlayerIdAndCardKey(playerId, mainCardCandidate.card_key)
                if not cards:
                    await interaction.followup.send(
                        "⚠️ Dữ liệu thẻ không hợp lệ. Vui lòng thử lại sau."
                    )
                    return

                # 5) Chỉ cho nâng từ thẻ cao nhất
                highestLevel = max(c.level for c in cards)
                if highestLevel != current_level:
                    await interaction.followup.send(
                        f"⚠️ Bạn chỉ có thể nâng cấp từ thẻ cấp cao nhất.\n"
                        f"Thẻ với ID `{card_id}` đang ở cấp {current_level}, "
                        f"nhưng thẻ cao nhất của bạn là cấp {highestLevel}."
                    )
                    return

                # 6) Thẻ chính không được đang equipped
                if mainCardCandidate.equipped:
                    await interaction.followup.send(
                        f"⚠️ Thẻ **{card_name}** (ID `{mainCardCandidate.id}`) đang được dùng làm thẻ chính, "
                        f"hãy tháo thẻ đó ra bằng lệnh /setcard một thẻ khác trước khi nâng cấp."
                    )
                    return

                # 7) Tính nguyên liệu phôi (thẻ cấp 1)
                # Logic gốc: requiredMaterials = 3 * (desired_level - 1)
                # Ở đây desired_level = current_level + 1 => requiredMaterials = 3 * current_level
                requiredMaterials = 3 * current_level

                level1Cards = [c for c in cards if c.level == 1]
                totalLevel1Quantity = sum(c.quantity for c in level1Cards)

                if totalLevel1Quantity < requiredMaterials:
                    await interaction.followup.send(
                        f"⚠️ Bạn không có đủ thẻ **{card_name}** cấp 1 để nâng cấp.\n"
                        f"Yêu cầu: {requiredMaterials}, hiện có: {totalLevel1Quantity}."
                    )
                    return

                # 8) Tiêu hao thẻ chính (1 bản)
                if mainCardCandidate.quantity > 1:
                    mainCardCandidate.quantity -= 1
                else:
                    cardRepo.deleteCard(mainCardCandidate)

                # 9) Tạo bản ghi mới cho thẻ đã nâng cấp
                newCard = PlayerCard(
                    player_id=playerId,
                    card_key=mainCardCandidate.card_key,
                    level=desired_level,
                    quantity=1,
                    equipped=False,
                    locked=mainCardCandidate.locked
                )
                cardRepo.create(newCard)

                # 10) Tiêu hao thẻ cấp 1 làm phôi
                remaining = requiredMaterials
                for c in level1Cards:
                    if remaining <= 0:
                        break
                    if c.quantity <= remaining:
                        remaining -= c.quantity
                        cardRepo.deleteCard(c)
                    else:
                        c.quantity -= remaining
                        if c.quantity == 0:
                            cardRepo.deleteCard(c)
                        remaining = 0

                # 11) Thưởng exp
                playerRepo.incrementExp(playerId, amount=5)

                session.commit()

                await interaction.followup.send(
                    f"✅ Nâng cấp thành công! Thẻ **{card_name}** "
                    f"(ID `{newCard.id}`) đã được nâng từ cấp {current_level} lên cấp {desired_level}."
                )

        except Exception as e:
            print("❌ Lỗi khi xử lý levelup:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(LevelUpCard(bot))
