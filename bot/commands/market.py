import discord
from discord.ext import commands, tasks
from discord import app_commands
from discord.ui import View, Button
import math
from datetime import datetime
from sqlalchemy.orm import joinedload

from bot.config.database import getDbSession
from bot.services.marketService import MarketService
from bot.entity.playerCards import PlayerCard
from bot.entity.player import Player
from bot.entity.marketListing import MarketListing
from bot.entity.cardTemplate import CardTemplate

ITEMS_PER_PAGE = 5

async def resolve_seller_name(bot, interaction: discord.Interaction, seller_id: int) -> str:
    """Lấy danh tính người bán để hiển thị"""
    if interaction.guild:
        member = interaction.guild.get_member(seller_id)
        if member: return member.display_name
    
    user = bot.get_user(seller_id)
    if user: return user.display_name
    
    try:
        with getDbSession() as session:
            p = session.query(Player).filter(Player.player_id == seller_id).first()
            if p and p.username: return p.username
    except: pass
    
    return "Nhẫn giả"

class MarketPaginationView(View):
    def __init__(self, bot, guild_id, listings, author, title="Chợ Đen"):
        super().__init__(timeout=300)
        self.bot = bot
        self.guild_id = guild_id
        self.listings = listings
        self.author = author
        self.current_page = 0
        self.title = title

    def get_total_pages(self):
        return math.ceil(len(self.listings) / ITEMS_PER_PAGE) if self.listings else 1

    async def build_embed(self, interaction: discord.Interaction):
        total_pages = self.get_total_pages()
        start = self.current_page * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE
        subset = self.listings[start:end]

        embed = discord.Embed(title=f"🏪 {self.title}", color=discord.Color.from_rgb(43, 45, 49))
        
        if not subset:
            embed.description = "Hiện không có tin đăng nào."
        else:
            description = []
            for item in subset:
                price_str = f"{item.unit_price:,} Ryo"
                seller_name = await resolve_seller_name(self.bot, interaction, item.seller_id)
                seller_display = f"<@{item.seller_id}>" if seller_name != "Nhẫn giả" else "Nhẫn giả"

                line = (
                    f"ID: # {item.id} | ✅ {item.template.name} (Lv {item.level})\n"
                    f"┣ 🏷️ Tier: {item.template.tier} | 📦 SL: {item.quantity}\n"
                    f"┣ 💵 Giá: {price_str} / thẻ\n"
                    f"┗ 👤 Người bán: {seller_display}\n"
                    f"━━━━━━━━━━━━━━━━━━"
                )
                description.append(line)
            embed.description = "\n".join(description)

        embed.set_footer(text=f"Trang {self.current_page + 1}/{total_pages} • Dùng /market buy [ID] để mua")
        return embed

    @discord.ui.button(label="Trước", style=discord.ButtonStyle.primary)
    async def prev_page(self, interaction: discord.Interaction, button: Button):
        if self.current_page > 0:
            self.current_page -= 1
            await interaction.response.edit_message(embed=await self.build_embed(interaction), view=self)

    @discord.ui.button(label="Sau", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: Button):
        if self.current_page < self.get_total_pages() - 1:
            self.current_page += 1
            await interaction.response.edit_message(embed=await self.build_embed(interaction), view=self)

class Market(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_market_expiry.start()

    def cog_unload(self):
        self.check_market_expiry.cancel()

    market_group = app_commands.Group(name="market", description="Hệ thống Chợ Đen")

    @market_group.command(name="sell", description="Đăng bán thẻ bài")
    async def market_sell(self, interaction: discord.Interaction, card_id: int, quantity: int, unit_price: int):
        await interaction.response.defer()
        try:
            with getDbSession() as session:
                service = MarketService(session)
                last_listing = service.listCard(interaction.user.id, card_id, quantity, unit_price)
                card_name = last_listing.template.name if last_listing.template else "Thẻ"
                session.commit()
                
                embed = discord.Embed(
                    title="✅ Đăng bán thành công!",
                    description=(
                        f"Đã đăng bán **{quantity}x {card_name}** lên chợ\n"
                        f"┣ 🏷️ ID tin: # {last_listing.id}\n"
                        f"┣ 💵 Giá bán: {unit_price:,} Ryo/thẻ\n"
                        f"┗ 💰 Tổng tiền: {unit_price * quantity:,} Ryo"
                    ),
                    color=discord.Color.green()
                )
                await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(f"❌ Lỗi: {e}")

    @market_sell.autocomplete('card_id')
    async def _market_sell_card_id_autocomplete(self, interaction: discord.Interaction, current: str):
        try:
            with getDbSession() as session:
                cards = session.query(PlayerCard).filter_by(player_id=interaction.user.id, status='INVENTORY').all()
                choices = []
                for pc in cards:
                    if pc.locked or pc.equipped: continue
                    label = f"{pc.template.name} (Lv {pc.level}) - ID: {pc.id}"
                    if not current or current.lower() in label.lower():
                        choices.append(app_commands.Choice(name=label[:100], value=pc.id))
                return choices[:25]
        except: return []

    @market_group.command(name="buy", description="Mua thẻ từ người chơi")
    @app_commands.describe(listing_id="Chọn tin đăng (#ID - Tên - Người bán)", quantity="Số lượng mua")
    async def market_buy(self, interaction: discord.Interaction, listing_id: int, quantity: int = None):
        await self._execute_buy(interaction, listing_id, quantity)

    @market_buy.autocomplete('listing_id')
    async def _market_buy_id_autocomplete(self, interaction: discord.Interaction, current: str):
        try:
            with getDbSession() as session:
                query = session.query(MarketListing).options(
                    joinedload(MarketListing.template),
                    joinedload(MarketListing.seller)
                ).filter(MarketListing.status == 'LISTED')
                
                al = query.order_by(MarketListing.created_at.desc()).limit(30).all()
                choices = []
                for item in al:
                    c_n = item.template.name if item.template else "Thẻ"
                    s_n = item.seller.username if item.seller else "Nhẫn giả"
                    label = f"#{item.id} | {c_n} - {item.unit_price:,} Ryo ({s_n})"
                    
                    if not current or current.lower() in label.lower():
                        choices.append(app_commands.Choice(name=label[:100], value=item.id))
                    if len(choices) >= 25: break
                return choices
        except: return []

    async def _execute_buy(self, interaction: discord.Interaction, listing_id: int, quantity: int = None):
        await interaction.response.defer()
        try:
            with getDbSession() as session:
                listing_check = session.query(MarketListing).filter_by(id=listing_id).first()
                if not listing_check:
                    return await interaction.followup.send("⚠️ Tin đăng không tồn tại.")
                
                final_q = quantity if quantity is not None else listing_check.quantity
                service = MarketService(session)
                listing_obj, total_p, tax, buy_c = service.buyListing(interaction.user.id, listing_id, final_q)
                session.commit()
                
                s_name = await resolve_seller_name(self.bot, interaction, listing_obj.seller_id)
                s_disp = f"<@{listing_obj.seller_id}>" if s_name != "Nhẫn giả" else "Nhẫn giả"

                embed = discord.Embed(
                    title="🎉 Giao dịch thành công!",
                    description=(
                        f"Bạn đã mua **{buy_c}x {listing_obj.template.name}**\n"
                        f"┣ 💵 Trả: {total_p:,} Ryo cho {s_disp}\n"
                        f"┗ 💰 Minh bạch: Tiền đã được gửi tới người bán."
                    ),
                    color=discord.Color.gold()
                )
                await interaction.followup.send(embed=embed)

                try:
                    s_user = self.bot.get_user(listing_obj.seller_id) or await self.bot.fetch_user(listing_obj.seller_id)
                    if s_user:
                        n_emb = discord.Embed(
                            title="💰 Đơn hàng thành công!",
                            description=(
                                f"**{interaction.user.display_name}** đã mua hàng của bạn:\n"
                                f"┣ 📦 Thẻ: **{buy_c}x {listing_obj.template.name}**\n"
                                f"┣ 💵 Doanh thu: {total_p:,} Ryo\n"
                                f"┗ 💰 Thực nhận: {total_p - int(total_p * 0.05):,} Ryo"
                            ),
                            color=discord.Color.green()
                        )
                        await s_user.send(embed=n_emb)
                except: pass
        except Exception as e:
            await interaction.followup.send(f"❌ Lỗi: {e}")

    @market_group.command(name="all", description="Sảnh giao dịch")
    async def market_all(self, interaction: discord.Interaction, tier: str = None, find: str = None):
        await interaction.response.defer()
        try:
            with getDbSession() as session:
                query = session.query(MarketListing).filter(MarketListing.status == 'LISTED')
                if tier: query = query.join(CardTemplate).filter(CardTemplate.tier == tier)
                if find: query = query.join(CardTemplate).filter(CardTemplate.name.like(f"%{find}%"))
                
                listings = query.order_by(MarketListing.created_at.desc()).all()
                view = MarketPaginationView(self.bot, interaction.guild_id, listings, interaction.user, title="Sảnh Chợ Đen")
                await interaction.followup.send(embed=await view.build_embed(interaction), view=view)
        except: await interaction.followup.send(f"❌ Lỗi hiển thị sảnh.")

    @market_group.command(name="my", description="Sạp hàng cá nhân")
    async def market_my(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            with getDbSession() as session:
                service = MarketService(session)
                listings = service.market_repo.getPlayerListings(interaction.user.id)
                view = MarketPaginationView(self.bot, interaction.guild_id, listings, interaction.user, title="Sạp Hàng Của Bạn")
                await interaction.followup.send(embed=await view.build_embed(interaction), view=view)
        except: await interaction.followup.send(f"❌ Lỗi xem sạp.")

    @market_group.command(name="cancel", description="Thu hồi thẻ đang bán")
    @app_commands.describe(listing_id="Chọn tin đăng muốn thu hồi")
    async def market_cancel(self, interaction: discord.Interaction, listing_id: int):
        await interaction.response.defer()
        try:
            with getDbSession() as session:
                service = MarketService(session)
                listing = service.market_repo.getById(listing_id)
                if not listing or listing.seller_id != interaction.user.id:
                    return await interaction.followup.send("⚠️ Bạn không sở hữu tin đăng này.")
                
                n = listing.template.name if listing.template else "Thẻ"
                service.cancelListing(interaction.user.id, listing_id)
                session.commit()
                
                embed = discord.Embed(
                    title="✅ Thu hồi thành công!",
                    description=f"Đã thu hồi **{listing.quantity}x {n}** về túi đồ\n┗ Tin đăng # {listing_id} đã đóng.",
                    color=discord.Color.blue()
                )
                await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(f"⚠️ {e}")

    @market_cancel.autocomplete('listing_id')
    async def _market_cancel_id_autocomplete(self, interaction: discord.Interaction, current: str):
        try:
            with getDbSession() as session:
                listings = session.query(MarketListing).options(joinedload(MarketListing.template)).filter_by(
                    seller_id=interaction.user.id, status='LISTED'
                ).all()
                choices = []
                for item in listings:
                    name = item.template.name if item.template else "Thẻ"
                    label = f"#{item.id} | {name} - {item.quantity}x"
                    if not current or current.lower() in label.lower():
                        choices.append(app_commands.Choice(name=label[:100], value=item.id))
                return choices[:25]
        except: return []

    @tasks.loop(hours=1)
    async def check_market_expiry(self):
        try:
            with getDbSession() as session:
                MarketService(session).processExpirations()
        except: pass

async def setup(bot):
    await bot.add_cog(Market(bot))
