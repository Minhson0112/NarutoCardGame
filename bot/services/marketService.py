from datetime import datetime, timedelta
from bot.entity.marketListing import MarketListing
from bot.entity.player import Player
from bot.entity.playerCards import PlayerCard
from bot.repository.marketRepository import MarketRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.playerRepository import PlayerRepository

LISTING_FEE = 50
TRANSACTION_TAX = 0.05

class MarketService:
    def __init__(self, session):
        self.session = session
        self.market_repo = MarketRepository(session)
        self.player_card_repo = PlayerCardRepository(session)
        self.player_repo = PlayerRepository(session)

    def listCard(self, seller_id: int, card_id: int, quantity: int, unit_price: int):
        """
        Đăng bán thẻ bài - Hệ thống Unique ID
        - Trừ phí niêm yết (50 Ryo).
        - Chuyển thẻ sang trạng thái ON_MARKET.
        """
        player = self.player_repo.getById(seller_id)
        if not player: raise ValueError("Người chơi không tồn tại.")
        if player.coin_balance < LISTING_FEE:
            raise ValueError(f"Không đủ tiền để trả phí niêm yết ({LISTING_FEE} Ryo).")
        
        # Thẻ cụ thể (Unique ID)
        player_card = self.player_card_repo.getById(card_id)
        if not player_card or player_card.player_id != seller_id:
            raise ValueError("Thẻ không tồn tại hoặc không thuộc về bạn.")
        if player_card.status != 'INVENTORY':
            raise ValueError("Thẻ này đang được giao dịch hoặc trang bị.")
        if player_card.locked: raise ValueError("Thẻ đang bị khóa.")
        if player_card.equipped: raise ValueError("Thẻ đang được trang bị.")

        # 1. Thu phí niêm yết ngay
        player.coin_balance -= LISTING_FEE
        
        # 2. Xử lý Listing (Đăng mới)
        expires_at = datetime.now() + timedelta(days=7)
        listing = MarketListing(
            seller_id=seller_id,
            card_key=player_card.card_key,
            level=player_card.level,
            quantity=quantity,
            unit_price=unit_price,
            status='LISTED',
            expires_at=expires_at
        )
        self.market_repo.create(listing)
        self.session.flush() # Lấy ID của listing mới tạo

        # 3. Tách thẻ ra để bán
        if player_card.quantity > quantity:
            player_card.quantity -= quantity
            market_card = PlayerCard(
                player_id=seller_id,
                card_key=player_card.card_key,
                level=player_card.level,
                quantity=quantity,
                status='ON_MARKET',
                listing_id=listing.id
            )
            self.session.add(market_card)
        else:
            player_card.status = 'ON_MARKET'
            player_card.listing_id = listing.id
            
        return listing

    def buyListing(self, buyer_id: int, listing_id: int, requested_quantity: int = 1):
        """
        Mua hàng trên chợ - Đảm bảo tính minh bạch 100%
        - Trừ tiền người mua (đã có check số dư).
        - Cộng tiền cho người bán (sau thuế).
        - Chuyển thẻ cho người mua.
        """
        buyer = self.player_repo.getById(buyer_id)
        if not buyer: raise ValueError("Người chơi không tồn tại.")
            
        listing = self.market_repo.getById(listing_id)
        if not listing or listing.status != 'LISTED':
            raise ValueError("Mặt hàng này không còn sẵn sàng trên chợ.")
            
        if listing.seller_id == buyer_id:
            raise ValueError("Bạn không thể tự mua sạp hàng của chính mình.")

        if requested_quantity <= 0 or requested_quantity > listing.quantity:
            raise ValueError(f"Số lượng mua không hợp lệ (Tối đa: {listing.quantity}).")
            
        total_price = listing.unit_price * requested_quantity
        if buyer.coin_balance < total_price:
            raise ValueError(f"Bạn không đủ tiền (Cần {total_price:,} Ryo, hiện có {buyer.coin_balance:,} Ryo).")
            
        # Lấy người bán - CHẮC CHẮN RẰNG NGƯỜI BÁN CÒN TỒN TẠI
        seller = self.player_repo.getById(listing.seller_id)
        if not seller:
            raise ValueError("Không tìm thấy sạp hàng của người bán này.")

        # 🛡️ 1. CHUYỂN TIỀN (NGUYÊN TỬ)
        tax = int(total_price * TRANSACTION_TAX)
        seller_receive = total_price - tax
        
        buyer.coin_balance -= total_price   # Trừ người mua
        seller.coin_balance += seller_receive # Cộng người bán (MINH BẠCH - ĐÃ CỘNG!)

        # 💎 2. CHUYỂN THẺ (Dùng Repository để gộp xập cho gọn kho)
        cards_on_market = (
            self.session.query(PlayerCard)
            .filter_by(listing_id=listing.id, status='ON_MARKET')
            .all()
        )
        
        remaining = requested_quantity
        for card in cards_on_market:
            if remaining <= 0: break
            take = min(card.quantity, remaining)
            
            if card.quantity == take:
                self.session.delete(card)
            else:
                card.quantity -= take
            
            remaining -= take
            # Tăng số lượng thẻ cho người mua (Tăng đúng CARD_KEY và LEVEL)
            self.player_card_repo.incrementQuantity(buyer_id, listing.card_key, listing.level, take)
            
        # 3. Cập nhật trạng thái tin đăng
        if requested_quantity == listing.quantity:
            listing.status = 'SOLD'
        else:
            listing.quantity -= requested_quantity
            
        return listing, total_price, tax, requested_quantity

    def cancelListing(self, player_id: int, listing_id: int):
        """
        Hủy tin đăng và hoàn trả thẻ về túi đồ.
        """
        listing = self.market_repo.getById(listing_id)
        if not listing or listing.status != 'LISTED':
            raise ValueError("Tin đăng này không thể hủy.")
            
        if listing.seller_id != player_id:
            raise ValueError("Bạn không có quyền hủy tin của người khác.")
            
        # Hoàn trả toàn bộ thẻ về kho (ID đại diện trong listing_id)
        cards_to_return = (
            self.session.query(PlayerCard)
            .filter_by(listing_id=listing.id, status='ON_MARKET')
            .all()
        )
        for card in cards_to_return:
            card.status = 'INVENTORY'
            card.listing_id = None
            
        listing.status = 'CANCELLED'
        return listing

    def processExpirations(self):
        """Tự động xử lý tin đăng hết hạn"""
        expired = self.market_repo.getExpiredListings()
        count = 0
        for l in expired:
            try:
                cards = self.session.query(PlayerCard).filter_by(listing_id=l.id, status='ON_MARKET').all()
                for c in cards:
                    c.status = 'INVENTORY'
                    c.listing_id = None
                l.status = 'EXPIRED'
                count += 1
            except: continue
        return count
