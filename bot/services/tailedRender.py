from PIL import Image
from PIL.Image import Resampling
from io import BytesIO

def CardResize(image):
    target_width = 200
    w, h = image.size
    return image.resize((target_width, int(target_width * (h/w))), Resampling.LANCZOS)

def renderImageFight(card1Path, card2Path, card3Path, card5Path, bgPath):
    bg = Image.open(bgPath).convert("RGBA")
    card1 = CardResize(Image.open(card1Path)).convert("RGBA")
    card2 = CardResize(Image.open(card2Path)).convert("RGBA")
    card3 = CardResize(Image.open(card3Path)).convert("RGBA")

    card5 = CardResize(Image.open(card5Path)).convert("RGBA")


    bw, bh = bg.size
    cw, ch     = card1.size
    n_cards    = 3
    total_space= bw - n_cards * cw
    spacing    = total_space // (n_cards + 1)

    pos1 = (spacing, 100)
    pos2 = (spacing * 2 + cw, 20)
    pos3 = (spacing * 3 + cw * 2, 100)

    pos5 = (spacing * 2 + cw, 450)

    bg.paste(card1, pos1, card1)
    bg.paste(card2, pos2, card2)
    bg.paste(card3, pos3, card3)


    bg.paste(card5, pos5, card5)


    buffer = BytesIO()
    bg.save(buffer, format="PNG")
    buffer.seek(0)  # Reset con trỏ về đầu

    return buffer