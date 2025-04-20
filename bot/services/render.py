from io import BytesIO
from PIL import Image
from PIL.Image import Resampling

def CardResize(image):
    target_width = 150
    w, h = image.size
    return image.resize((target_width, int(target_width * (h/w))), Resampling.LANCZOS)

def WeaponResize(image):
    target_width = 70
    w, h = image.size
    return image.resize((target_width, int(target_width * (h/w))), Resampling.LANCZOS)

def renderImage(card1Path, card2Path, card3Path,
                weapon1Path, weapon2Path, weapon3Path,
                bgPath):
    # 1) Load và resize
    bg      = Image.open(bgPath).convert("RGBA")
    card1   = CardResize(Image.open(card1Path).convert("RGBA"))
    card2   = CardResize(Image.open(card2Path).convert("RGBA"))
    card3   = CardResize(Image.open(card3Path).convert("RGBA"))
    weapon1 = WeaponResize(Image.open(weapon1Path).convert("RGBA"))
    weapon2 = WeaponResize(Image.open(weapon2Path).convert("RGBA"))
    weapon3 = WeaponResize(Image.open(weapon3Path).convert("RGBA"))

    # 2) Tính vị trí
    bw, bh     = bg.size
    cw, ch     = card1.size
    n_cards    = 3
    total_space= bw - n_cards * cw
    spacing    = total_space // (n_cards + 1)

    card_positions = [
        (spacing, 100),
        (spacing*2 + cw, 100),
        (spacing*3 + cw*2, 100),
    ]
    weapon_positions = [
        (x + 40, 10) for (x, y) in card_positions
    ]

    # 3) Paste lên background
    for img, pos in zip((card1, card2, card3), card_positions):
        bg.paste(img, pos, img)
    for img, pos in zip((weapon1, weapon2, weapon3), weapon_positions):
        bg.paste(img, pos, img)

    # 4) Save ra file <playerId>.png trong bộ nhớ tạm
    buffer = BytesIO()
    bg.save(buffer, format="PNG")
    buffer.seek(0)  # Reset con trỏ về đầu

    return buffer
