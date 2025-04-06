from bot.entity.player import Player
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerActiveSetupRepository import PlayerActiveSetupRepository
from bot.repository.gachaPityCounterRepository import GachaPityCounterRepository

from bot.config.gachaConfig import GACHA_PACKS

class PlayerService:
    def __init__(self, repo: PlayerRepository, setupRepo: PlayerActiveSetupRepository = None, gachaPityRepo: GachaPityCounterRepository = None):
        self.repo = repo
        self.setupRepo = setupRepo
        self.gachaPityRepo = gachaPityRepo

    def registerPlayer(self, playerId: int, username: str) -> bool:
        existing = self.repo.getById(playerId)
        if existing:
            return False  # đã tồn tại

        newPlayer = Player(player_id=playerId, username=username)
        self.repo.create(newPlayer)

        if self.setupRepo:
            # ✅ Gọi repo để tạo bản ghi player_active_setup
            self.setupRepo.createEmptySetup(playerId)

        if self.gachaPityRepo:
            self.initializeAccount(playerId)

        return True
    
    def initializeAccount(self, playerId: int):
        for pack in GACHA_PACKS:
            self.gachaPityRepo.initializeCounter(playerId, pack)
    
    def addCoin(self, playerId: int, amount: int) -> bool:
        player = self.repo.getById(playerId)
        if not player:
            return False
        player.coin_balance += amount
        self.repo.session.commit()
        return True
