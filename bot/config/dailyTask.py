# config/dailyTask.py

"""
Cấu hình nhiệm vụ hằng ngày cho hệ thống.
Mỗi nhiệm vụ được định nghĩa gồm:
- Số lần cần hoàn thành để được nhận thưởng (requirement)
- Số ryo thưởng khi hoàn thành nhiệm vụ (reward)

Ví dụ:
- Dùng lệnh fight và chiến thắng 5 lần nhận được 20000 ryo.
- Chơi minigame 10 lần nhận được 10000 ryo.
"""

# Nhiệm vụ "fight_win"
FIGHT_WIN_REQUIREMENT = 10       # Số lần chiến thắng cần hoàn thành để nhận thưởng
FIGHT_WIN_REWARD = 100000        # Số ryo thưởng cho nhiệm vụ fight win

# Nhiệm vụ "minigame"
MINIGAME_REQUIREMENT = 10       # Số lần chơi minigame cần hoàn thành để nhận thưởng
MINIGAME_REWARD = 30000         # Số ryo thưởng cho nhiệm vụ minigame

# Các nhiệm vụ khác (bạn có thể thay đổi theo ý muốn)
FIGHTWITH_REQUIREMENT = 5       # Ví dụ: số lần dùng lệnh fightwith cần thiết
FIGHTWITH_REWARD = 20000        # Ví dụ: số ryo thưởng cho nhiệm vụ fightwith

SHOP_BUY_REQUIREMENT = 3        # Số lần mua trong cửa hàng cần hoàn thành
SHOP_BUY_REWARD = 50000          # Số ryo thưởng cho nhiệm vụ mua trong cửa hàng

SHOP_SELL_REQUIREMENT = 3       # Số lần bán trong cửa hàng cần hoàn thành
SHOP_SELL_REWARD = 30000         # Số ryo thưởng cho nhiệm vụ bán trong cửa hàng

STAGE_CLEAR_REQUIREMENT = 1     # Số lần vượt ải cần hoàn thành (ví dụ chỉ cần vượt qua 1 lần)
STAGE_CLEAR_REWARD = 50000      # Số ryo thưởng cho nhiệm vụ vượt ải

# Cấu hình tập trung cho các nhiệm vụ hằng ngày
DAILY_TASK_CONFIG = {
    "fight_win": {
        "requirement": FIGHT_WIN_REQUIREMENT,
        "reward": FIGHT_WIN_REWARD,
    },
    "minigame": {
        "requirement": MINIGAME_REQUIREMENT,
        "reward": MINIGAME_REWARD,
    },
    "fightwith": {
        "requirement": FIGHTWITH_REQUIREMENT,
        "reward": FIGHTWITH_REWARD,
    },
    "shop_buy": {
        "requirement": SHOP_BUY_REQUIREMENT,
        "reward": SHOP_BUY_REWARD,
    },
    "shop_sell": {
        "requirement": SHOP_SELL_REQUIREMENT,
        "reward": SHOP_SELL_REWARD,
    },
    "stage_clear": {
        "requirement": STAGE_CLEAR_REQUIREMENT,
        "reward": STAGE_CLEAR_REWARD,
    },
}
