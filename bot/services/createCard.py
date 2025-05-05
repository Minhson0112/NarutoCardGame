from bot.services.cardBase import Card
from bot.services.tailedCard import TailedBeastCard
from bot.services.character.yamanakaIno import YamanakaIno
from bot.services.character.tenTen import TenTen
from bot.services.character.kankuro import Kankuro
from bot.services.character.aburameShino import AburameShino
from bot.services.character.harunoSakura import HarunoSakura
from bot.services.character.hyugaHinata import HyugaHinata
from bot.services.character.temari import Temari
from bot.services.character.inuzukaKiba import InuzukaKiba
from bot.services.character.akimichiChoji import AkimichiChoji
from bot.services.character.uminoIruka import UminoIruka
from bot.services.character.momochiZabuza import MomochiZabuza
from bot.services.character.konohamaru import Konohamaru
from bot.services.character.hyugaNeji import HyugaNeji
from bot.services.character.naraShikamaru import NaraShikamaru
from bot.services.character.noharaRin import NoharaRin
from bot.services.character.yagura import Yagura
from bot.services.character.rockLee import RockLee
from bot.services.character.yuhiKurenai import YuhiKurenai
from bot.services.character.sarutobiAsuma import SarutobiAsuma
from bot.services.character.hidan import Hidan
from bot.services.character.kimimaro import Kimimaro
from bot.services.character.sasori import Sasori
from bot.services.character.yamanakaSai import YamanakaSai

from bot.services.character.uchihaMadara import UchihaMadara

SPECIAL_CARD_CLASS_MAP = {
    "Uchiha Madara": UchihaMadara,
    "Yamanaka Ino": YamanakaIno,
    "TenTen": TenTen,
    "Kankuro" : Kankuro,
    "Aburame Shino" : AburameShino,
    "Haruno Sakura": HarunoSakura,
    "Hyuga Hinata": HyugaHinata,
    "Temari": Temari,
    "Inuzuka Kiba": InuzukaKiba,
    "Akimichi Choji": AkimichiChoji,
    "Umino Iruka": UminoIruka,
    "Momochi Zabuza": MomochiZabuza,
    "Konohamaru": Konohamaru,
    "Hyuga Neji": HyugaNeji,
    "Nara Shikamaru": NaraShikamaru,
    "Nohara Rin": NoharaRin,
    "Yagura": Yagura,
    "Rock_Lee": RockLee,
    "Yuhi Kurenai": YuhiKurenai,
    "Sarutobi Asuma": SarutobiAsuma,
    "Hidan": Hidan,
    "Kimimaro": Kimimaro,
    "Sasori": Sasori,
    "Yamanaka Sai": YamanakaSai,





    # ... thêm các tướng khác
}

def create_card(name, health, armor, base_damage, crit_rate, speed, chakra, element, tier):
    # Nếu là vĩ thú thì dùng class riêng cho vĩ thú
    if element == "vi":
        card_class = TailedBeastCard
    else:
        # Ưu tiên tìm theo tên trong map tướng đặc biệt
        card_class = SPECIAL_CARD_CLASS_MAP.get(name, Card)
    return card_class(name, health, armor, base_damage, crit_rate, speed, chakra, element, tier)
