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

    @app_commands.command(name="levelupcard", description="Nâng cấp thẻ của bạn")
    @app_commands.describe(
        card="Tên thẻ bạn sở hữu (ví dụ: Uchiha Madara)",
        desired_level="Cấp mong muốn nâng cấp đến (ví dụ: 2, 3, 4, ...)"
    )
    async def levelUp(self, interaction: discord.Interaction, card: str, desired_level: int):
        await interaction.response.defer(thinking=True)
        playerId = interaction.user.id

        try:
            with getDbSession() as session:
                # Lấy thông tin người chơi
                playerRepo = PlayerRepository(session)
                player = playerRepo.getById(playerId)
                if not player:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!")
                    return

                # Lấy danh sách các thẻ của người chơi theo tên
                cardRepo = PlayerCardRepository(session)
                cards = cardRepo.getByCardNameAndPlayerId(playerId, card)
                if not cards:
                    await interaction.followup.send("⚠️ Bạn không sở hữu thẻ này hoặc nhập sai tên. Kiểm tra lại trong /inventory.")
                    return

                # Yêu cầu nâng cấp phải từ cấp 2 trở lên
                if desired_level < 2:
                    await interaction.followup.send("⚠️ Cấp nâng phải từ 2 trở lên.")
                    return
                
                if desired_level > 50:
                    await interaction.followup.send("⚠️ cấp thẻ lớn nhất có thể nâng cấp là 50.")
                    return

                # Kiểm tra: Người chơi chỉ có thể nâng cấp từ thẻ cao nhất
                # Tìm cấp cao nhất của các thẻ với tên đó
                highestLevel = max(c.level for c in cards)
                # Nếu thẻ cao nhất không phải là thẻ cần dùng làm nguyên liệu (desired_level - 1)
                if highestLevel != desired_level - 1:
                    await interaction.followup.send(
                        f"⚠️ Bạn chỉ có thể nâng cấp từ thẻ cao nhất. Hiện tại thẻ cao nhất của bạn là cấp {highestLevel}."
                    )
                    return

                # Xác định yêu cầu:
                # - Thẻ chính cần có level == desired_level - 1 (và không được đang equipped).
                # - Nguyên liệu bổ sung: cần số lượng thẻ cấp 1 bằng 3 * (desired_level - 1)
                requiredMaterials = 3 * (desired_level - 1)
                mainCardCandidate = None

                for c in cards:
                    if c.level == desired_level - 1:
                        if c.equipped:
                            await interaction.followup.send(
                                f"⚠️ Thẻ **{c.template.name}** đang được dùng làm thẻ chính, hãy tháo thẻ đó ra bằng lệnh /setcard một thẻ khác trước khi nâng cấp."
                            )
                            return
                        mainCardCandidate = c
                        break

                if mainCardCandidate is None:
                    await interaction.followup.send(
                        f"⚠️ Bạn không có thẻ **{card}** ở cấp {desired_level - 1} để nâng cấp lên cấp {desired_level}."
                    )
                    return

                # Đếm số lượng thẻ cấp 1 làm nguyên liệu
                level1Cards = [c for c in cards if c.level == 1]
                totalLevel1Quantity = sum(c.quantity for c in level1Cards)
                if totalLevel1Quantity < requiredMaterials:
                    await interaction.followup.send(
                        f"⚠️ Bạn không có đủ thẻ **{card}** cấp 1 để nâng cấp. Yêu cầu: {requiredMaterials}, hiện có: {totalLevel1Quantity}."
                    )
                    return

                # Tiêu hao thẻ chính (một bản sao) để nâng cấp:
                if mainCardCandidate.quantity > 1:
                    mainCardCandidate.quantity -= 1
                else:
                    cardRepo.deleteCard(mainCardCandidate)

                # Tạo bản ghi mới cho thẻ đã nâng cấp
                # Giả sử các thuộc tính card_key, template, ... được sao chép từ mainCardCandidate
                newCard = PlayerCard(
                    player_id=playerId,
                    card_key=mainCardCandidate.card_key,
                    level=desired_level,
                    quantity=1,
                    equipped=False,
                    locked = mainCardCandidate.locked
                )
                cardRepo.create(newCard)

                # Tiêu hao các thẻ cấp 1 làm nguyên liệu
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

                session.commit()
                await interaction.followup.send(
                    f"✅ Nâng cấp thành công! Thẻ **{newCard.template.name}** đã được nâng lên cấp {desired_level}."
                )
        except Exception as e:
            print("❌ Lỗi khi xử lý levelup:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(LevelUpCard(bot))
