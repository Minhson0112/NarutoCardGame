import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ADMIN_OVERRIDE_ID = 995730123166851102
NONE_CARD_IMAGE_URL = "https://cdn.discordapp.com/attachments/1357740352878022736/1358406569129410711/noncard.png?ex=67f3ba34&is=67f268b4&hm=848208f7d1eb860c6749cfd4f8e17c0ceb35f8a1326e90738d9f9b393be26734&"
NONE_WEAPON_IMAGE_URL = "https://cdn.discordapp.com/attachments/1358315431257182288/1358406505124331620/Nonweapon.png?ex=67f3ba24&is=67f268a4&hm=6a7c28b848905d8d0bf457aae4e60f701e8f7ba715d874c6f9681faf8ae227c2&"
VS_IMAGE = "https://cdn.discordapp.com/attachments/1358825326360264756/1358825477023994109/vs.gif?ex=67f54057&is=67f3eed7&hm=f5eff06c7b9d7e70f8e1c4e37baeac7fc7622c67035e5ba93f568156acfa18d0&"
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}
