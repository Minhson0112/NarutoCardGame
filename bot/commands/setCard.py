import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.playerActiveSetupRepository import PlayerActiveSetupRepository

class SetCard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="setcard",
        description="Lắp thẻ chiến đấu của bạn vào một vị trí cụ thể"
    )
    @app_commands.describe(
        position="Chọn vị trí lắp: tanker/middle/back",
        card="Tên thẻ bạn sở hữu (ví dụ: Uchiha Madara)"
    )
    @app_commands.choices(position=[
        app_commands.Choice(name="tanker", value="tanker"),
        app_commands.Choice(name="middle",  value="middle"),
        app_commands.Choice(name="back",    value="back"),
    ])
    async def setCard(
        self,
        interaction: discord.Interaction,
        position: app_commands.Choice[str],
        card: str
    ):
        await interaction.response.defer(thinking=True)
        player_id = interaction.user.id

        try:
            with getDbSession() as session:
                # Khởi tạo repositories
                playerRepo = PlayerRepository(session)
                cardRepo   = PlayerCardRepository(session)
                setupRepo  = PlayerActiveSetupRepository(session)

                # 1) Kiểm tra người chơi đã đăng ký
                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send(
                        "⚠️ Bạn chưa đăng ký tài khoản. Dùng `/register` trước!"
                    )
                    return

                # 2) Tìm thẻ theo tên
                candidates = cardRepo.getByCardNameAndPlayerId(player_id, card)
                if not candidates:
                    await interaction.followup.send(
                        "⚠️ Nhập sai tên thẻ hoặc bạn không sở hữu thẻ đó."
                    )
                    return

                # 3) Chọn thẻ level cao nhất
                selected = max(candidates, key=lambda c: c.level)

                # 4) Kiểm first_position theo slot
                pos = position.value  # "tanker"/"middle"/"back"
                is_first = selected.template.first_position
                if pos == "tanker" and not is_first:
                    await interaction.followup.send(
                        "❌ Thẻ này không thể đứng hàng đầu (tanker)."
                    )
                    return
                if pos in ("middle", "back") and is_first:
                    await interaction.followup.send(
                        "❌ Thẻ này bắt buộc phải ở hàng đầu, không thể lắp middle|back."
                    )
                    return

                # 5) Lấy hoặc tạo setup
                setup = setupRepo.getByPlayerId(player_id)
                if not setup:
                    setup = setupRepo.createEmptySetup(player_id)

                # 6) Kiểm thẻ đã lắp chỗ khác chưa
                slot_map = {
                    "tanker": "card_slot1",
                    "middle": "card_slot2",
                    "back":   "card_slot3"
                }
                cur_attr = slot_map[pos]
                for other_pos, attr in slot_map.items():
                    if other_pos != pos and getattr(setup, attr) == selected.id:
                        await interaction.followup.send(
                            "❌ Thẻ này đã được lắp ở vị trí khác, không thể lắp trùng!",
                            ephemeral=True
                        )
                        return

                # 7) Unequip thẻ cũ ở slot hiện tại
                old_id = getattr(setup, cur_attr)
                if old_id is not None:
                    old_card = cardRepo.getById(old_id)
                    if old_card:
                        old_card.equipped = False

                # 8) Equip thẻ mới & cập nhật slot
                selected.equipped = True
                if pos == "tanker":
                    setupRepo.updateCardSlot1(player_id, selected.id)
                elif pos == "middle":
                    setupRepo.updateCardSlot2(player_id, selected.id)
                else:  # back
                    setupRepo.updateCardSlot3(player_id, selected.id)

                await interaction.followup.send(
                    f"✅ Đã lắp thẻ **{selected.template.name}** (Lv {selected.level}) vào **{pos}**."
                )

        except Exception as e:
            # Hiển thị lỗi chi tiết (ephemeral để chỉ người chơi thấy)
            await interaction.followup.send(
                f"❌ Lỗi khi setcard:\n```{e}```",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(SetCard(bot))
