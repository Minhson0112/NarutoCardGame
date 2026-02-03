import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.dailyTaskRepository import DailyTaskRepository
from bot.services.i18n import t


class Blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
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
        deck = []
        for _, info in self.card_map.items():
            for emoji in info["emojis"]:
                deck.append({"card": emoji, "value": info["value"]})
        random.shuffle(deck)
        return deck

    def calculate_total(self, cards):
        return sum(card["value"] for card in cards)

    def get_rank(self, card_emoji: str) -> str:
        if card_emoji.startswith("10"):
            return "10"
        return card_emoji[0]

    def is_blackjack(self, cards):
        if len(cards) != 2:
            return False
        ranks = [self.get_rank(card["card"]) for card in cards]
        return (ranks.count("A") == 1) and any(rank in ["10", "J", "Q", "K"] for rank in ranks if rank != "A")

    def is_double_ace(self, cards):
        if len(cards) != 2:
            return False
        return self.get_rank(cards[0]["card"]) == "A" and self.get_rank(cards[1]["card"]) == "A"

    def _build_embed_desc(
        self,
        guild_id,
        player_cards,
        player_total,
        dealer_display,
        bet,
        extra_lines=None,
    ):
        extra_lines = extra_lines or []
        lines = [
            t(
                guild_id,
                "blackjack.embed.player_hand",
                cards=" ".join(card["card"] for card in player_cards),
                total=player_total,
            ),
            "",
            t(guild_id, "blackjack.embed.dealer_hidden", cards=dealer_display),
            "",
            t(guild_id, "blackjack.embed.actions"),
            t(guild_id, "blackjack.embed.bet", bet=bet),
        ]
        if extra_lines:
            lines += [""] + extra_lines
        return "\n".join(lines)

    @app_commands.command(name="blackjack", description="Chơi blackjack đơn giản với số tiền cược")
    @app_commands.describe(bet="Số tiền cược bạn muốn đặt 💰")
    async def blackjack(self, interaction: discord.Interaction, bet: int):
        await interaction.response.defer(thinking=True)

        player_id = interaction.user.id
        guild_id = interaction.guild.id if interaction.guild else None

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                dailyTaskRepo = DailyTaskRepository(session)

                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send(t(guild_id, "blackjack.not_registered"))
                    return

                if bet <= 0:
                    await interaction.followup.send(t(guild_id, "blackjack.bet_invalid"))
                    return

                if bet > 1_000_000:
                    await interaction.followup.send(t(guild_id, "blackjack.bet_too_large"))
                    return

                if player.coin_balance < bet:
                    await interaction.followup.send(t(guild_id, "blackjack.not_enough_balance"))
                    return

                dailyTaskRepo.updateMinigame(player_id)

                deck = self.create_deck()
                player_cards = [deck.pop(), deck.pop()]
                dealer_cards = [deck.pop(), deck.pop()]

                player_total = self.calculate_total(player_cards)

                dealer_display_hidden = dealer_cards[0]["card"] + " " + " ".join("❓" for _ in dealer_cards[1:])

                embed = discord.Embed(
                    title=t(guild_id, "blackjack.embed.title"),
                    description=self._build_embed_desc(
                        guild_id=guild_id,
                        player_cards=player_cards,
                        player_total=player_total,
                        dealer_display=dealer_display_hidden,
                        bet=bet,
                    ),
                    color=discord.Color.green(),
                )

                msg = await interaction.followup.send(embed=embed)

                # --- Double Aces (xi bàn) ưu tiên ---
                player_double_ace = self.is_double_ace(player_cards)
                dealer_double_ace = self.is_double_ace(dealer_cards)
                if player_double_ace or dealer_double_ace:
                    final_dealer_display = " ".join(card["card"] for card in dealer_cards)

                    if player_double_ace and not dealer_double_ace:
                        outcome = t(guild_id, "blackjack.outcome.double_ace_win")
                        player.coin_balance += bet * 4
                    elif dealer_double_ace and not player_double_ace:
                        outcome = t(guild_id, "blackjack.outcome.double_ace_lose")
                        player.coin_balance -= bet * 4
                    else:
                        outcome = t(guild_id, "blackjack.outcome.double_ace_draw")

                    embed.description = "\n".join([
                        t(guild_id, "blackjack.embed.player_hand", cards=" ".join(c["card"] for c in player_cards), total=self.calculate_total(player_cards)),
                        "",
                        t(guild_id, "blackjack.embed.dealer_hidden", cards=final_dealer_display),
                        "",
                        outcome,
                        t(guild_id, "blackjack.embed.balance", balance=player.coin_balance),
                    ])
                    await msg.edit(embed=embed)
                    session.commit()
                    return

                # --- Blackjack check ---
                player_blackjack = self.is_blackjack(player_cards)
                dealer_blackjack = self.is_blackjack(dealer_cards)
                if player_blackjack or dealer_blackjack:
                    final_dealer_display = " ".join(card["card"] for card in dealer_cards)

                    if player_blackjack and not dealer_blackjack:
                        outcome = t(guild_id, "blackjack.outcome.blackjack_win")
                        player.coin_balance += bet * 3
                    elif player_blackjack and dealer_blackjack:
                        outcome = t(guild_id, "blackjack.outcome.blackjack_both")
                        player.coin_balance -= bet
                    else:
                        outcome = t(guild_id, "blackjack.outcome.blackjack_lose")
                        player.coin_balance -= bet

                    embed.description = "\n".join([
                        t(guild_id, "blackjack.embed.player_hand", cards=" ".join(c["card"] for c in player_cards), total=self.calculate_total(player_cards)),
                        "",
                        t(guild_id, "blackjack.embed.dealer_hidden", cards=final_dealer_display),
                        "",
                        outcome,
                        t(guild_id, "blackjack.embed.balance", balance=player.coin_balance),
                    ])
                    await msg.edit(embed=embed)
                    session.commit()
                    return

                HIT_EMOJI = "🟢"
                STAND_EMOJI = "🔴"
                await msg.add_reaction(HIT_EMOJI)
                await msg.add_reaction(STAND_EMOJI)

                def check(reaction, user):
                    return (
                        user.id == player_id
                        and reaction.message.id == msg.id
                        and str(reaction.emoji) in [HIT_EMOJI, STAND_EMOJI]
                    )

                player_busted = False
                player_five_card = False

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
                        embed.description = self._build_embed_desc(
                            guild_id=guild_id,
                            player_cards=player_cards,
                            player_total=player_total,
                            dealer_display=dealer_display_hidden,
                            bet=bet,
                        )
                        await msg.edit(embed=embed)
                        continue

                    if str(reaction.emoji) == STAND_EMOJI:
                        break

                if player_five_card:
                    outcome = t(guild_id, "blackjack.outcome.five_card_win")
                    player.coin_balance += bet

                    final_player_display = " ".join(card["card"] for card in player_cards)
                    final_dealer_display = " ".join(card["card"] for card in dealer_cards)

                    embed.description = "\n".join([
                        t(guild_id, "blackjack.embed.player_hand", cards=final_player_display, total=player_total),
                        "",
                        t(guild_id, "blackjack.embed.dealer_hidden", cards=final_dealer_display),
                        "",
                        outcome,
                        t(guild_id, "blackjack.embed.balance", balance=player.coin_balance),
                    ])
                    await msg.edit(embed=embed)
                    session.commit()
                    return

                if player_busted:
                    dealer_total = self.calculate_total(dealer_cards)
                    final_dealer_display = " ".join(card["card"] for card in dealer_cards)

                    if dealer_total >= 15:
                        outcome = t(guild_id, "blackjack.outcome.player_bust_lose")
                        player.coin_balance -= bet
                    else:
                        embed.description = "\n".join([
                            t(guild_id, "blackjack.embed.player_hand", cards=" ".join(c["card"] for c in player_cards), total=player_total),
                            "",
                            t(guild_id, "blackjack.embed.dealer_hand", cards=final_dealer_display, total=dealer_total),
                            "",
                            t(guild_id, "blackjack.embed.dealer_drawing"),
                        ])
                        await msg.edit(embed=embed)
                        await asyncio.sleep(1)

                        while dealer_total < 15 and len(deck) > 0:
                            new_card = deck.pop()
                            dealer_cards.append(new_card)
                            dealer_total = self.calculate_total(dealer_cards)
                            final_dealer_display = " ".join(card["card"] for card in dealer_cards)

                            embed.description = "\n".join([
                                t(guild_id, "blackjack.embed.player_hand", cards=" ".join(c["card"] for c in player_cards), total=player_total),
                                "",
                                t(guild_id, "blackjack.embed.dealer_hand", cards=final_dealer_display, total=dealer_total),
                                "",
                                t(guild_id, "blackjack.embed.dealer_drawing"),
                            ])
                            await msg.edit(embed=embed)
                            await asyncio.sleep(1)

                        if dealer_total > 21:
                            outcome = t(guild_id, "blackjack.outcome.both_bust_draw")
                        else:
                            outcome = t(guild_id, "blackjack.outcome.dealer_after_draw_lose", dealerTotal=dealer_total)
                            player.coin_balance -= bet

                    final_player_display = " ".join(card["card"] for card in player_cards)
                    final_dealer_display = " ".join(card["card"] for card in dealer_cards)

                    embed.description = "\n".join([
                        t(guild_id, "blackjack.embed.player_hand", cards=final_player_display, total=player_total),
                        "",
                        t(guild_id, "blackjack.embed.dealer_hand", cards=final_dealer_display, total=dealer_total),
                        "",
                        outcome,
                        t(guild_id, "blackjack.embed.balance", balance=player.coin_balance),
                    ])
                    await msg.edit(embed=embed)
                    session.commit()
                    return

                dealer_total = self.calculate_total(dealer_cards)
                final_dealer_display = " ".join(card["card"] for card in dealer_cards)

                embed.description = "\n".join([
                    t(guild_id, "blackjack.embed.player_hand", cards=" ".join(c["card"] for c in player_cards), total=player_total),
                    "",
                    t(guild_id, "blackjack.embed.dealer_hand", cards=final_dealer_display, total=dealer_total),
                    "",
                    t(guild_id, "blackjack.embed.dealer_start_drawing"),
                ])
                await msg.edit(embed=embed)
                await asyncio.sleep(1)

                dealer_five_card = False
                while dealer_total < 17 and len(deck) > 0:
                    new_card = deck.pop()
                    dealer_cards.append(new_card)
                    dealer_total = self.calculate_total(dealer_cards)
                    final_dealer_display = " ".join(card["card"] for card in dealer_cards)

                    if len(dealer_cards) == 5 and dealer_total <= 21:
                        dealer_five_card = True
                        outcome = t(guild_id, "blackjack.outcome.dealer_five_card_lose")
                        player.coin_balance -= bet
                        break

                    embed.description = "\n".join([
                        t(guild_id, "blackjack.embed.player_hand", cards=" ".join(c["card"] for c in player_cards), total=player_total),
                        "",
                        t(guild_id, "blackjack.embed.dealer_hand", cards=final_dealer_display, total=dealer_total),
                        "",
                        t(guild_id, "blackjack.embed.dealer_draw"),
                    ])
                    await msg.edit(embed=embed)
                    await asyncio.sleep(1)

                if dealer_five_card:
                    final_player_display = " ".join(card["card"] for card in player_cards)
                    final_dealer_display = " ".join(card["card"] for card in dealer_cards)

                    embed.description = "\n".join([
                        t(guild_id, "blackjack.embed.player_hand", cards=final_player_display, total=player_total),
                        "",
                        t(guild_id, "blackjack.embed.dealer_hand", cards=final_dealer_display, total=dealer_total),
                        "",
                        outcome,
                        t(guild_id, "blackjack.embed.balance", balance=player.coin_balance),
                    ])
                    await msg.edit(embed=embed)
                    session.commit()
                    return

                final_player_display = " ".join(card["card"] for card in player_cards)
                final_dealer_display = " ".join(card["card"] for card in dealer_cards)

                if dealer_total > 21:
                    outcome = t(guild_id, "blackjack.outcome.dealer_bust_win")
                    player.coin_balance += bet
                else:
                    if player_total > dealer_total:
                        outcome = t(guild_id, "blackjack.outcome.win")
                        player.coin_balance += bet
                    elif player_total == dealer_total:
                        outcome = t(guild_id, "blackjack.outcome.draw")
                    else:
                        outcome = t(guild_id, "blackjack.outcome.lose")
                        player.coin_balance -= bet

                embed.description = "\n".join([
                    t(guild_id, "blackjack.embed.player_hand", cards=final_player_display, total=player_total),
                    "",
                    t(guild_id, "blackjack.embed.dealer_hand", cards=final_dealer_display, total=dealer_total),
                    "",
                    outcome,
                    t(guild_id, "blackjack.embed.balance", balance=player.coin_balance),
                ])
                await msg.edit(embed=embed)

                playerRepo.incrementExp(player_id, amount=2)
                session.commit()

        except Exception as e:
            print("❌ Lỗi khi xử lý /blackjack:", e)
            await interaction.followup.send(t(guild_id, "blackjack.error"))


async def setup(bot):
    await bot.add_cog(Blackjack(bot))
