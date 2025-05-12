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
from bot.services.character.yakushiKabuto import YakushiKabuto
from bot.services.character.yamato import Yamato
from bot.services.character.deidara import Deidara
from bot.services.character.gaara import Gaara
from bot.services.character.chuninKakashi import ChuninKakashi
from bot.services.character.kakuzu import Kakuzu
from bot.services.character.kushina import Kushina
from bot.services.character.konan import Konan
from bot.services.character.kisame import Kisame
from bot.services.character.uchihaObito import UchihaObito
from bot.services.character.gengetsu import Gengetsu
from bot.services.character.killerBee import KillerBee
from bot.services.character.raikageIII import RaikageIII
from bot.services.character.uchihaItachi import UchihaItachi
from bot.services.character.pain import Pain
from bot.services.character.uchihaSasuke import UchihaSasuke
from bot.services.character.kyuubiNaruto import KyuubiNaruto
from bot.services.character.hokageKakashi import HokageKakashi
from bot.services.character.mightGuy import MightGuy
from bot.services.character.uzumakiNagato import UzumakiNagato
from bot.services.character.onoki import Onoki
from bot.services.character.terumiMei import TerumiMei
from bot.services.character.tsunade import Tsunade
from bot.services.character.orochimaru import Orochimaru
from bot.services.character.jiraiya import Jiraiya
from bot.services.character.minato import Minato
from bot.services.character.sarutobiHiruzen import SarutobiHiruzen
from bot.services.character.senjuTobirama import SenjuTobirama
from bot.services.character.uchihaMadara import UchihaMadara
from bot.services.character.senjuHashirama import SenjuHashirama
from bot.services.character.shimuraDanzo import ShimuraDanzo
from bot.services.character.haku import Haku
from bot.services.character.hatakeKakashi import HatakeKakashi
from bot.services.character.uzumakiNaruto import UzumakiNaruto
from bot.services.character.susanooSasuke import SusanooSasuke
from bot.services.character.sixPathsPain import SixPathsPain
from bot.services.character.akatsukiItachi import AkatsukiItachi
from bot.services.character.nhatVi import NhatVi
from bot.services.character.nhiVi import NhiVi
from bot.services.character.tamVi import TamVi
from bot.services.character.tuVi import TuVi
from bot.services.character.NguVi import NguVi
from bot.services.character.lucVi import LucVi
from bot.services.character.thatVi import ThatVi
from bot.services.character.batVi import BatVi
from bot.services.character.cuuVi import CuuVi


from bot.services.weaponEffect.kunai import kunai
from bot.services.weaponEffect.knife import knife
from bot.services.weaponEffect.chakraKnife import ChakraKnife
from bot.services.weaponEffect.guandao import Guandao
from bot.services.weaponEffect.katana import Katana
from bot.services.weaponEffect.shuriken import Shuriken
from bot.services.weaponEffect.bow import Bow
from bot.services.weaponEffect.flail import Flail
from bot.services.weaponEffect.kibaku import Kibaku
from bot.services.weaponEffect.tansa import Tansa
from bot.services.weaponEffect.tessen import Tessen
from bot.services.weaponEffect.sansaju import Sansaju
from bot.services.weaponEffect.suna import Suna
from bot.services.weaponEffect.enma import Enma
from bot.services.weaponEffect.samehada import Samehada
from bot.services.weaponEffect.rinnegan import Rinnegan
from bot.services.weaponEffect.gudodama import Gudodama

SPECIAL_CARD_CLASS_MAP = {
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
    "Rock Lee": RockLee,
    "Yuhi Kurenai": YuhiKurenai,
    "Sarutobi Asuma": SarutobiAsuma,
    "Hidan": Hidan,
    "Kimimaro": Kimimaro,
    "Sasori": Sasori,
    "Yamanaka Sai": YamanakaSai,
    "Yakushi Kabuto": YakushiKabuto,
    "Yamato": Yamato,
    "Deidara": Deidara,
    "Gaara": Gaara,
    "Chunin Kakashi": ChuninKakashi,
    "Kakuzu": Kakuzu,
    "Kushina": Kushina,
    "Konan": Konan,
    "Kisame": Kisame,
    "Uchiha Obito": UchihaObito,
    "Gengetsu": Gengetsu,
    "Killer Bee": KillerBee,
    "RaikageIII": RaikageIII,
    "Uchiha Itachi": UchihaItachi,
    "Pain": Pain,
    "Uchiha Sasuke": UchihaSasuke,
    "Kyuubi Naruto": KyuubiNaruto,
    "Hokage Kakashi": HokageKakashi,
    "Might Guy": MightGuy,
    "Uzumaki Nagato": UzumakiNagato,
    "Onoki": Onoki,
    "Terumi Mei": TerumiMei,
    "Tsunade": Tsunade,
    "Orochimaru": Orochimaru,
    "Jiraiya": Jiraiya,
    "Minato": Minato,
    "Sarutobi Hiruzen": SarutobiHiruzen,
    "Senju Tobirama": SenjuTobirama,
    "Uchiha Madara": UchihaMadara,
    "Senju Hashirama": SenjuHashirama,
    "Shimura Danzo": ShimuraDanzo,
    "Haku": Haku,
    "Hatake Kakashi": HatakeKakashi,
    "Uzumaki Naruto": UzumakiNaruto,
    "Susanoo Sasuke": SusanooSasuke,
    "Six Paths Pain": SixPathsPain,
    "Akatsuki Itachi": AkatsukiItachi,
    "Nhất Vĩ": NhatVi,
    "Nhị Vĩ": NhiVi,
    "Tam Vĩ": TamVi,
    "Tứ Vĩ": TuVi,
    "Ngũ Vĩ": NguVi,
    "Lục Vĩ": LucVi,
    "Thất Vĩ": ThatVi,
    "Bát Vĩ": BatVi,
    "Cửu Vĩ": CuuVi,
}

WEAPON_NAME_MAP = {
    "Kunai": kunai,
    "Knife": knife,
    "ChakraKnife": ChakraKnife,
    "Guandao": Guandao,
    "Katana": Katana,
    "Shuriken": Shuriken,
    "Bow": Bow,
    "Flail": Flail,
    "Kibaku": Kibaku,
    "Tansa": Tansa,
    "Tessen": Tessen,
    "Sansaju": Sansaju,
    "Suna": Suna,
    "Enma": Enma,
    "Samehada": Samehada,
    "Rinnegan": Rinnegan,
    "Gudodama": Gudodama,
}

def create_card(name, health, armor, base_damage, crit_rate, speed, chakra, element, tier, weapon_name = None):

    weapon_passive = None

    if weapon_name:
        weapon_class = WEAPON_NAME_MAP.get(weapon_name)
        weapon_passive = weapon_class()

    card_class = SPECIAL_CARD_CLASS_MAP.get(name, Card)
    return card_class(name, health, armor, base_damage, crit_rate, speed, chakra, element, tier, weapon_passive)
