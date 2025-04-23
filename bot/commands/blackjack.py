import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.dailyTaskRepository import DailyTaskRepository

class Blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Định nghĩa các lá bài bằng emoji và giá trị tương ứng
        self.card_map = {
            "A": {"value": 1, "emojis": ["A♠️", "A♣️", "A♥️", "A♦️"]},
            "2": {"value": 2, "emojis": ["2♠️", "2♣️", "2♥️", "2♦️"]},
            "3": {"value": 3, "emojis": ["3♠️", "3♣️", "3♥️", "3♦️"]},
            "4": {"value": 4, "emojis": ["4♠️", "4♣️", "4♥️", "4♦️"]},
            "5": {"value": 5, "emojis": ["5♠️", "5♣️", "5♥️", "5♦️"]},
            "6": {"value": 6, "emojis": ["6♠️", "6♣️", "6♥️", "6♦️"]},
            "7": {"value": 7, "emojis": ["7♠️", "7♣️", "7♥️", "7♦️"]},
            "8": {"value": 8, "emojis": ["8♠️", "8♣️", "8♥️", "8♦️"]},
            "9": {"value": 9, "emojis": ["9♠️", "9♣️", "9♥️", "9♦️"]},
            "10": {"value": 10, "emojis": ["10♠️", "10♣️", "10♥️", "10♦️"]},
            "J": {"value": 10, "emojis": ["J♠️", "J♣️", "J♥️", "J♦️"]},
            "Q": {"value": 10, "emojis": ["Q♠️", "Q♣️", "Q♥️", "Q♦️"]},
            "K": {"value": 10, "emojis": ["K♠️", "K♣️", "K♥️", "K♦️"]},
        }
        
    def create_deck(self):
        """Tạo một bộ bài dựa theo card_map và trộn ngẫu nhiên."""
        deck = []
        for rank, info in self.card_map.items():
            for emoji in info["emojis"]:
                deck.append({"card": emoji, "value": info["value"]})
        random.shuffle(deck)
        return deck
    
    def calculate_total(self, cards):
        """Tính tổng điểm của các lá bài trong list cards."""
        return sum(card["value"] for card in cards)
    
    def get_rank(self, card_emoji: str) -> str:
        """Lấy xếp hạng của lá bài từ emoji.
           Với lá "10" trả về '10', còn lại trả về ký tự đầu tiên."""
        if card_emoji.startswith("10"):
            return "10"
        return card_emoji[0]
    
    def is_blackjack(self, cards):
        """Kiểm tra bài có phải blackjack không: đúng 2 lá, trong đó có đúng 1 lá A và
           lá còn lại thuộc nhóm ['10', 'J', 'Q', 'K']."""
        if len(cards) != 2:
            return False
        ranks = [self.get_rank(card["card"]) for card in cards]
        return (ranks.count("A") == 1) and any(rank in ["10", "J", "Q", "K"] for rank in ranks if rank != "A")
    
    def is_double_ace(self, cards):
        """Kiểm tra xem bài có phải 2 con A không (xi bàn)."""
        if len(cards) != 2:
            return False
        return self.get_rank(cards[0]["card"]) == "A" and self.get_rank(cards[1]["card"]) == "A"
    
    @app_commands.command(name="blackjack", description="Chơi blackjack đơn giản với số tiền cược")
    @app_commands.describe(bet="Số tiền cược bạn muốn đặt 💰")
    async def blackjack(self, interaction: discord.Interaction, bet: int):
        await interaction.response.defer(thinking=True)
        player_id = interaction.user.id

        try:
            with getDbSession() as session:
                # Lấy thông tin người chơi
                playerRepo = PlayerRepository(session)
                dailyTaskRepo = DailyTaskRepository(session)
                
                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!")
                    return
                
                if bet <= 0:
                    await interaction.followup.send("⚠️ Số tiền cược phải lớn hơn 0.")
                    return

                if bet > 1000000:
                    await interaction.followup.send("⚠️ Số tiền cược không được quá 1m.")
                    return

                if player.coin_balance < bet:
                    await interaction.followup.send("⚠️ Số dư của bạn không đủ.")
                    return
                dailyTaskRepo.updateMinigame(player_id)
                # Tạo bộ bài và chia bài ban đầu
                deck = self.create_deck()
                player_cards = [deck.pop(), deck.pop()]
                dealer_cards = [deck.pop(), deck.pop()]

                player_total = self.calculate_total(player_cards)
                # Ban đầu chỉ hiện thị lá đầu của nhà cái, các lá còn lại ẩn bằng ❓
                dealer_display = dealer_cards[0]["card"] + " " + " ".join("❓" for _ in dealer_cards[1:])
                
                # Tạo embed ban đầu
                embed = discord.Embed(
                    title="♠️ Blackjack Game ♣️",
                    description=(
                        f"**Bài của bạn:** {' '.join(card['card'] for card in player_cards)} (Tổng: {player_total})\n\n"
                        f"**Bài của Nhà Cái:** {dealer_display}\n\n"
                        "🟢: Rút bài (Hit) | 🔴: Dừng (Stand)\n"
                        f"Bet: {bet}"
                    ),
                    color=discord.Color.green()
                )
                # Gửi tin nhắn game ban đầu
                msg = await interaction.followup.send(embed=embed)
                
                # --- Kiểm tra tình huống “xi bàn” 2 A ngay ban đầu (ưu tiên so với blackjack) ---
                player_double_ace = self.is_double_ace(player_cards)
                dealer_double_ace = self.is_double_ace(dealer_cards)
                if player_double_ace or dealer_double_ace:
                    final_dealer_display = " ".join(card["card"] for card in dealer_cards)
                    if player_double_ace and not dealer_double_ace:
                        outcome = "🎉 Bạn có 2 con A (xi bàn)! Bạn thắng x4 tiền!"
                        player.coin_balance += bet * 4
                    elif dealer_double_ace and not player_double_ace:
                        outcome = "😢 Nhà Cái có 2 con A (xi bàn)! Bạn thua x4 tiền!"
                        player.coin_balance -= bet * 4
                    else:
                        outcome = "🤝 Cả hai đều có 2 con A (xi bàn)! Hòa!"
                    embed.description = (
                        f"**Bài của bạn:** {' '.join(card['card'] for card in player_cards)}\n\n"
                        f"**Bài của Nhà Cái:** {final_dealer_display}\n\n"
                        f"{outcome}\n"
                        f"Số dư hiện tại: **{player.coin_balance}**"
                    )
                    await msg.edit(embed=embed)
                    session.commit()
                    return
                
                # Kiểm tra ngay blackjack (1 A và 1 trong [10,J,Q,K])
                player_blackjack = self.is_blackjack(player_cards)
                dealer_blackjack = self.is_blackjack(dealer_cards)
                if player_blackjack or dealer_blackjack:
                    final_dealer_display = " ".join(card["card"] for card in dealer_cards)
                    if player_blackjack and not dealer_blackjack:
                        outcome = "🎉 Blackjack! Bạn thắng x3 tiền!"
                        player.coin_balance += bet * 3
                    elif player_blackjack and dealer_blackjack:
                        outcome = "😢 Cả hai cùng blackjack! Nhà Cái thắng!"
                        player.coin_balance -= bet
                    elif dealer_blackjack and not player_blackjack:
                        outcome = "😢 Nhà Cái có blackjack! Bạn thua!"
                        player.coin_balance -= bet
                    embed.description = (
                        f"**Bài của bạn:** {' '.join(card['card'] for card in player_cards)}\n\n"
                        f"**Bài của Nhà Cái:** {final_dealer_display}\n\n"
                        f"{outcome}\n"
                        f"Số dư hiện tại: **{player.coin_balance}**"
                    )
                    await msg.edit(embed=embed)
                    session.commit()
                    return
                
                # Nếu không xảy ra tình huống đặc biệt, cho người chơi tương tác (Hit/Stand)
                HIT_EMOJI = "🟢"
                STAND_EMOJI = "🔴"
                await msg.add_reaction(HIT_EMOJI)
                await msg.add_reaction(STAND_EMOJI)
                
                def check(reaction, user):
                    return (
                        user.id == player_id and 
                        reaction.message.id == msg.id and 
                        str(reaction.emoji) in [HIT_EMOJI, STAND_EMOJI]
                    )
                
                player_busted = False
                player_five_card = False  # cờ kiểm tra “ngũ linh” của người chơi
                # Vòng lặp lượt của người chơi
                while True:
                    try:
                        reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
                    except asyncio.TimeoutError:
                        break
                    if str(reaction.emoji) == HIT_EMOJI:
                        try:
                            await msg.remove_reaction(HIT_EMOJI, user)
                        except Exception:
                            pass
                        new_card = deck.pop()
                        player_cards.append(new_card)
                        player_total = self.calculate_total(player_cards)
                        if player_total > 21:
                            player_busted = True
                            break
                        if len(player_cards) == 5 and player_total <= 21:
                            player_five_card = True
                            break
                        player_display = " ".join(card["card"] for card in player_cards)
                        embed.description = (
                            f"**Bài của bạn:** {player_display} (Tổng: {player_total})\n\n"
                            f"**Bài của Nhà Cái:** {dealer_display}\n\n"
                            "🟢: Rút bài (Hit) | 🔴: Dừng (Stand)\n"
                            f"Bet: {bet}"
                        )
                        await msg.edit(embed=embed)
                    elif str(reaction.emoji) == STAND_EMOJI:
                        break

                if player_five_card:
                    outcome = "🎉 Bạn đạt 5 lá không quá 21 (Ngũ linh)! Bạn thắng ngay!"
                    player.coin_balance += bet
                    final_player_display = " ".join(card["card"] for card in player_cards)
                    final_dealer_display = " ".join(card["card"] for card in dealer_cards)
                    embed.description = (
                        f"**Bài của bạn:** {final_player_display} (Tổng: {player_total})\n\n"
                        f"**Bài của Nhà Cái:** {final_dealer_display}\n\n"
                        f"{outcome}\n"
                        f"Số dư hiện tại: **{player.coin_balance}**"
                    )
                    await msg.edit(embed=embed)
                    session.commit()
                    return

                if player_busted:
                    dealer_total = self.calculate_total(dealer_cards)
                    final_dealer_display = " ".join(card["card"] for card in dealer_cards)
                    if dealer_total >= 15:
                        outcome = "😢 Bạn bị quắc, bạn thua!"
                        player.coin_balance -= bet
                    else:
                        embed.description = (
                            f"**Bài của bạn:** {' '.join(card['card'] for card in player_cards)} (Tổng: {player_total})\n\n"
                            f"**Bài của Nhà Cái:** {final_dealer_display} (Tổng: {dealer_total})\n\n"
                            "Nhà Cái đang bốc bài..."
                        )
                        await msg.edit(embed=embed)
                        await asyncio.sleep(1)
                        while dealer_total < 15 and len(deck) > 0:
                            new_card = deck.pop()
                            dealer_cards.append(new_card)
                            dealer_total = self.calculate_total(dealer_cards)
                            final_dealer_display = " ".join(card["card"] for card in dealer_cards)
                            embed.description = (
                                f"**Bài của bạn:** {' '.join(card['card'] for card in player_cards)} (Tổng: {player_total})\n\n"
                                f"**Bài của Nhà Cái:** {final_dealer_display} (Tổng: {dealer_total})\n\n"
                                "Nhà Cái đang bốc bài..."
                            )
                            await msg.edit(embed=embed)
                            await asyncio.sleep(1)
                        if dealer_total > 21:
                            outcome = "🤝 Cả Nhà Cái cũng quắc, kết quả hòa, bạn không mất tiền!"
                        else:
                            outcome = f"😢 Sau khi bốc, Nhà Cái có {dealer_total} điểm, bạn thua!"
                            player.coin_balance -= bet

                    final_player_display = " ".join(card["card"] for card in player_cards)
                    final_dealer_display = " ".join(card["card"] for card in dealer_cards)
                    embed.description = (
                        f"**Bài của bạn:** {final_player_display} (Tổng: {player_total})\n\n"
                        f"**Bài của Nhà Cái:** {final_dealer_display} (Tổng: {dealer_total})\n\n"
                        f"{outcome}\n"
                        f"Số dư hiện tại: **{player.coin_balance}**"
                    )
                    await msg.edit(embed=embed)
                    session.commit()
                    return

                dealer_total = self.calculate_total(dealer_cards)
                final_dealer_display = " ".join(card["card"] for card in dealer_cards)
                embed.description = (
                    f"**Bài của bạn:** {' '.join(card['card'] for card in player_cards)} (Tổng: {player_total})\n\n"
                    f"**Bài của Nhà Cái:** {final_dealer_display} (Tổng: {dealer_total})\n\n"
                    "Nhà Cái bắt đầu rút bài..."
                )
                await msg.edit(embed=embed)
                await asyncio.sleep(1)

                dealer_five_card = False  # cờ kiểm tra “ngũ linh” của Nhà Cái
                while dealer_total < 17 and len(deck) > 0:
                    new_card = deck.pop()
                    dealer_cards.append(new_card)
                    dealer_total = self.calculate_total(dealer_cards)
                    final_dealer_display = " ".join(card["card"] for card in dealer_cards)
                    if len(dealer_cards) == 5 and dealer_total <= 21:
                        dealer_five_card = True
                        outcome = "😢 Nhà Cái đạt 5 lá không quá 21 (Ngũ linh)! Bạn thua!"
                        player.coin_balance -= bet
                        break

                    embed.description = (
                        f"**Bài của bạn:** {' '.join(card['card'] for card in player_cards)} (Tổng: {player_total})\n\n"
                        f"**Bài của Nhà Cái:** {final_dealer_display} (Tổng: {dealer_total})\n\n"
                        "Nhà Cái rút bài..."
                    )
                    await msg.edit(embed=embed)
                    await asyncio.sleep(1)

                if dealer_five_card:
                    final_player_display = " ".join(card["card"] for card in player_cards)
                    final_dealer_display = " ".join(card["card"] for card in dealer_cards)
                    embed.description = (
                        f"**Bài của bạn:** {final_player_display} (Tổng: {player_total})\n\n"
                        f"**Bài của Nhà Cái:** {final_dealer_display} (Tổng: {dealer_total})\n\n"
                        f"{outcome}\n"
                        f"Số dư hiện tại: **{player.coin_balance}**"
                    )
                    await msg.edit(embed=embed)
                    session.commit()
                    return

                final_player_display = " ".join(card["card"] for card in player_cards)
                final_dealer_display = " ".join(card["card"] for card in dealer_cards)
                if dealer_total > 21:
                    outcome = "🎉 Nhà Cái bị quắc! Bạn thắng!"
                    player.coin_balance += bet
                else:
                    if player_total > dealer_total:
                        outcome = "🎉 Bạn thắng!"
                        player.coin_balance += bet
                    elif player_total == dealer_total:
                        outcome = "🤝 Hòa!"
                    else:
                        outcome = "😢 Bạn thua!"
                        player.coin_balance -= bet

                embed.description = (
                    f"**Bài của bạn:** {final_player_display} (Tổng: {player_total})\n\n"
                    f"**Bài của Nhà Cái:** {final_dealer_display} (Tổng: {dealer_total})\n\n"
                    f"{outcome}\n"
                    f"Số dư hiện tại: **{player.coin_balance}**"
                )
                await msg.edit(embed=embed)
                session.commit()

        except Exception as e:
            print("❌ Lỗi khi xử lý /blackjack:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(Blackjack(bot))
