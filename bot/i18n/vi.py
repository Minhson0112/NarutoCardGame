VI = {
    # battlerule
    "battlerule.title": "📜 Luật Battle",
    "battlerule.desc": (
        "🔹 **Mỗi đội** có 3 thẻ (Tanker, Middle, Back) (đã tích hợp sẵn vũ khí nếu lắp)\n"
        "🏎️ Team nào có tổng **Tốc độ** lớn hơn sẽ được quyền đánh **trước**\n"
        "🎯 Đòn tấn công cơ bản ưu tiên mục tiêu: **Tanker → Middle → Back**\n"
        "💧 Nếu **Chakra** của thẻ lên **100**, lượt kế nó sẽ dùng **Skill Đặc Biệt**\n"
        "💧 **Chakra** của thẻ sẽ tăng 20 sau mỗi lần ra đòn hoặc kết liễu tướng đối phương, tăng khi nhận sát thương theo % máu tối đa bị mất\n"
        "💀 Trận đấu kết thúc khi một bên có cả **3 thẻ đều chết**\n"
        "⏳ Nếu quá **120 lượt** mà chưa phân thắng bại thì **hòa**\n"
        "⚔️ Xem kĩ năng đặc biệt tướng bằng lệnh `/showcard`"
    ),


    # Command: /adventure
    "adventure.not_registered": "⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!",
    "adventure.need_full_team": "⚠️ Bạn phải lắp đủ 3 thẻ (Tanker, Middle, Back) mới có thể tham gia đấu!",

    # Battle log
    "adventure.battle.starting": "Đang khởi đầu trận đấu…",
    "adventure.battle.title": "🔎 {username} đi khám phá và bị {teamName} phục kích",
    "adventure.battle.turn_header": "--- Lượt {turn}: {cardName} ---",

    # Result (final embed)
    "adventure.result.title": "🏁 Kết quả trận chiến của {username} VS {teamName}",
    "adventure.result.line_result": "🎖️ **Kết quả:** {result}",
    "adventure.result.reward_draw": "💰**Thưởng:** {reward:,} Ryo",
    "adventure.result.outcome_draw": "⚔️ Hai đội đều rút lui nên hoà! không nhận được thưởng, hãy quay lại sau 5 phút.",
    "adventure.result.result_win": "Chiến Thắng",
    "adventure.result.result_lose": "Thất Bại",
    "adventure.result.result_draw": "🏳️ Hoà",

    "adventure.result.reward_win": "💰**Thưởng:** nhặt được {reward:,} Ryo từ xác của {teamName}",
    "adventure.result.outcome_win": "bạn đã chiến thắng {teamName} và đã nhận thưởng, hãy quay lại sau 5 phút.",

    "adventure.result.reward_lose": "💰**Thưởng:** bọn {teamName} nói bạn quá non và không thèm lấy tiền của bạn",
    "adventure.result.outcome_lose": "bạn đã thất bại trước {teamName} và không nhận được gì, hãy quay lại sau 5 phút.",

    "adventure.result.footer_rank": "Điểm Rank: {rankPoints}",

    # Cooldown error
    "adventure.cooldown": "⏱️ Bạn phải chờ **{seconds:.1f}** giây nữa mới đi khám phá được.",

    # Generic error
    "adventure.error": "❌ Có lỗi xảy ra:\n```{trace}```",
    "adventure.team_names": [
        "Team thích thể hiện",
        "Team phổi to",
        "Team phá làng phá xóm",
        "Team giang hồ mõm",
        "Team cung bọ cạp",
        "Team biết bố mày là ai không",
        "Team chọc gậy bánh xe",
        "Team nghiện cờ bạc",
        "Team con nhà người ta",
        "Team thì ra mày chọn cái chết",
        "Team mình tao chấp hết",
        "Team tao có kiên",
        "Team hacker lỏ",
        "Team Không trượt phát lào",
        "Team tuổi l sánh vai",
        "Team đầu chộm đuôi cướp",
        "Team buôn hàng nóng",
        "Team gấu tró",
        "Team máu dồn lên não",
        "Team wibu",
        "Team fan mu",
        "Team đáy xã hội",
        "Team phụ hồ",
        "Team Ca sĩ hàn quốc",
        "Team đom đóm",
        "Team hội mê peter",
    ],


    # /bingo command
    "bingo.not_registered": "⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!",
    "bingo.bet_invalid": "⚠️ Số tiền cược phải lớn hơn 0.",
    "bingo.bet_too_large": "⚠️ Số tiền cược không được quá 1m.",
    "bingo.not_enough_balance": "⚠️ Số dư của bạn không đủ.",

    # Intro / instruction message (content)
    "bingo.intro": (
        "🌟 **Bingo Time!** 🌟\n\n"
        "Chọn số may mắn từ **1️⃣** đến **5️⃣**!\n"
        "Cược: **{bet} Ryo**\n"
        "❗ Nếu chọn đúng ngay từ lần đầu: nhận **x4** 🎉\n"
        "❗ Nếu chọn đúng ở lần thứ 2: nhận **x2** 😄\n"
        "❗ Nếu không đúng sau 2 lần: mất hết số tiền cược 😢"
    ),

    # Outcome texts (used inside embed description)
    "bingo.win_first_try": (
        "🥳 Chúc mừng! Con số may mắn của bạn là {numberEmoji}.\n"
        "Bạn đã chọn đúng ngay từ lần đầu, nhận thưởng là **{reward} Ryo**! 🎉"
    ),
    "bingo.win_second_try": (
        "😊 Chúc mừng! Con số may mắn của bạn là {numberEmoji}.\n"
        "Bạn đã chọn đúng ở lần thứ 2, nhận thưởng là **{reward} Ryo**! 👍"
    ),
    "bingo.lose": (
        "😢 Rất tiếc! Con số may mắn của bạn là {numberEmoji}.\n"
        "Bạn chọn sai. Bạn mất hết số tiền cược (**{bet} Ryo**)."
    ),

    # Result embed
    "bingo.result_embed.title": "🎲 Kết quả Bingo 🎲",
    "bingo.result_embed.desc": (
        "Số may mắn: {numberEmoji}\n\n"
        "{outcomeText}\n\n"
        "💰 Số dư hiện tại: **{balance} Ryo**"
    ),

    # Error
    "bingo.error": "❌ Có lỗi xảy ra. Vui lòng thử lại sau.",


    #blackjack
    "blackjack.not_registered": "⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!",
    "blackjack.bet_invalid": "⚠️ Số tiền cược phải lớn hơn 0.",
    "blackjack.bet_too_large": "⚠️ Số tiền cược không được quá 1m.",
    "blackjack.not_enough_balance": "⚠️ Số dư của bạn không đủ.",
    "blackjack.error": "❌ Có lỗi xảy ra. Vui lòng thử lại sau.",

    "blackjack.embed.title": "♠️ Blackjack Game ♣️",
    "blackjack.embed.player_hand": "**Bài của bạn:** {cards} (Tổng: {total})",
    "blackjack.embed.dealer_hand": "**Bài của Nhà Cái:** {cards} (Tổng: {total})",
    "blackjack.embed.dealer_hidden": "**Bài của Nhà Cái:** {cards}",
    "blackjack.embed.actions": "🟢: Rút bài (Hit) | 🔴: Dừng (Stand)",
    "blackjack.embed.bet": "Bet: {bet}",
    "blackjack.embed.dealer_drawing": "Nhà Cái đang bốc bài...",
    "blackjack.embed.dealer_start_drawing": "Nhà Cái bắt đầu rút bài...",
    "blackjack.embed.dealer_draw": "Nhà Cái rút bài...",
    "blackjack.embed.balance": "Số dư hiện tại: **{balance}**",

    "blackjack.outcome.double_ace_win": "🎉 Bạn có 2 con A (xi bàn)! Bạn thắng x4 tiền!",
    "blackjack.outcome.double_ace_lose": "😢 Nhà Cái có 2 con A (xi bàn)! Bạn thua x4 tiền!",
    "blackjack.outcome.double_ace_draw": "🤝 Cả hai đều có 2 con A (xi bàn)! Hòa!",

    "blackjack.outcome.blackjack_win": "🎉 Blackjack! Bạn thắng x3 tiền!",
    "blackjack.outcome.blackjack_both": "😢 Cả hai cùng blackjack! Nhà Cái thắng!",
    "blackjack.outcome.blackjack_lose": "😢 Nhà Cái có blackjack! Bạn thua!",

    "blackjack.outcome.five_card_win": "🎉 Bạn đạt 5 lá không quá 21 (Ngũ linh)! Bạn thắng ngay!",
    "blackjack.outcome.player_bust_lose": "😢 Bạn bị quắc, bạn thua!",
    "blackjack.outcome.both_bust_draw": "🤝 Cả Nhà Cái cũng quắc, kết quả hòa, bạn không mất tiền!",
    "blackjack.outcome.dealer_after_draw_lose": "😢 Sau khi bốc, Nhà Cái có {dealerTotal} điểm, bạn thua!",

    "blackjack.outcome.dealer_five_card_lose": "😢 Nhà Cái đạt 5 lá không quá 21 (Ngũ linh)! Bạn thua!",
    "blackjack.outcome.dealer_bust_win": "🎉 Nhà Cái bị quắc! Bạn thắng!",

    "blackjack.outcome.win": "🎉 Bạn thắng!",
    "blackjack.outcome.lose": "😢 Bạn thua!",
    "blackjack.outcome.draw": "🤝 Hòa!",



    #buycard
    "buycard.not_registered": "⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng `/register` trước nhé!",

    "buycard.invalid_pack": "❌ Gói '{pack}' không hợp lệ. Vui lòng chọn: {validPacks}",
    "buycard.not_enough_balance": "❌ Số dư không đủ. Cần {cost:,} Ryo, hiện có {balance:,} Ryo.",
    "buycard.open_pack_not_found": "❌ Lỗi khi mở hộp, không tìm thấy thẻ phù hợp.",

    "buycard.result.title": "🎉 Bạn đã mua gói {pack} và mở được thẻ: {cardName}",
    "buycard.result.stats.damage": "**Damage:** {value}",
    "buycard.result.stats.hp": "**Hp:** {value}",
    "buycard.result.stats.armor": "**Giáp:** {value}",
    "buycard.result.stats.crit_rate": "**Tỉ lệ chí mạng:** {value}",
    "buycard.result.stats.dodge": "**Né:** {value}",
    "buycard.result.stats.base_chakra": "**Chakra gốc:** {value}",
    "buycard.result.stats.tanker": "**Tanker:** {value}",
    "buycard.result.stats.tier": "**Bậc:** {value}",
    "buycard.result.stats.element": "**Hệ chakra:** {value}",
    "buycard.result.stats.sell_price": "**Giá bán:** {value:,} Ryo",

    "buycard.common.yes": "✅",
    "buycard.common.no": "❌",

    "buycard.result.added_to_inventory": "Thẻ đã được thêm vào kho của bạn. Kiểm tra kho bằng lệnh `/inventory`.",
    "buycard.result.skill_title": "📜 **Skill đặc biệt:**",
    "buycard.skill_missing": "Chưa có skill đặc biệt.",

    "buycard.cooldown": "⏱️ Bạn phải chờ **{seconds:.1f}** giây nữa mới mở gói tiếp được.",
    "buycard.error": "❌ Có lỗi xảy ra. Vui lòng thử lại sau.",


    # buymulticard
    "buymulticard.cooldown": "⏱️ Chưa hết cooldown, hãy đợi **{remaining}**s nữa.",
    "buymulticard.not_registered": "⚠️ Bạn chưa đăng ký. Dùng `/register` trước nhé!",
    "buymulticard.count_invalid": "⚠️ Số lượng phải lớn hơn 0.",
    "buymulticard.level_required": "⚠️ Chức năng này chỉ dành cho người chơi từ level 2 trở lên.",
    "buymulticard.count_limit": "⚠️ Bạn ở level {level} chỉ được mua tối đa {maxPack} pack mỗi lần.",
    "buymulticard.pack_invalid": "⚠️ Gói không hợp lệ.",
    "buymulticard.not_enough_balance": "❌ Cần {totalCost:,} Ryo, bạn chỉ có {balance:,}.",
    "buymulticard.success_header": "✅ Bạn đã mua thành công **{count} {pack}** và nhận được:",
    "buymulticard.item_line": "🥷 {name} ({tier}) x {qty}",
    "buymulticard.error": "❌ Có lỗi xảy ra. Vui lòng thử lại sau.",



    # buyweapon
    "buyweapon.not_registered": "⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng `/register` trước nhé!",
    "buyweapon.pack_invalid": "❌ Gói '{pack}' không hợp lệ. Vui lòng chọn: {validPacks}",
    "buyweapon.not_enough_balance": "❌ Số dư không đủ. Cần {cost:,} Ryo, hiện có {balance:,} Ryo.",
    "buyweapon.no_weapon_found": "❌ Lỗi khi mở hộp, không tìm thấy vũ khí phù hợp.",
    "buyweapon.error": "❌ Có lỗi xảy ra. Vui lòng thử lại sau.",

    "buyweapon.embed.title": "🎉 Bạn đã mua gói {pack} và mở được vũ khí: {weaponName}",
    "buyweapon.embed.line_bonus_damage": "**Damage cộng thêm:** {value}",
    "buyweapon.embed.line_bonus_health": "**Hp cộng thêm:** {value}",
    "buyweapon.embed.line_bonus_armor": "**Giáp cộng thêm:** {value}",
    "buyweapon.embed.line_bonus_crit_rate": "**Tỉ lệ chí mạng cộng thêm:** {value}",
    "buyweapon.embed.line_bonus_speed": "**Né cộng thêm:** {value}",
    "buyweapon.embed.line_bonus_chakra": "**Chakra cộng thêm:** {value}",
    "buyweapon.embed.line_grade": "**Bậc:** {grade}",
    "buyweapon.embed.line_sell_price": "**Giá bán:** {price:,} Ryo",
    "buyweapon.embed.added_to_inventory": "Vũ khí đã được thêm vào kho của bạn. Kiểm tra kho bằng lệnh `/inventory`.",
    "buyweapon.embed.passive_title": "📜 **Nội Tại Vũ khí:**",
    "buyweapon.embed.skill_missing": "Chưa có nội tại.",


    # checkmoney
    "checkmoney.not_registered": "⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng `/register` trước nhé!",
    "checkmoney.balance": "💰 Số dư hiện tại của bạn là **{coin:,} Ryo**",
    "checkmoney.error": "❌ Đã xảy ra lỗi. Vui lòng thử lại sau.",



    # coinflip
    "coinflip.invalid_guess": "⚠️ Vui lòng nhập đúng dự đoán: **u** hoặc **n**.",
    "coinflip.not_registered": "⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!",
    "coinflip.bet_must_be_positive": "⚠️ Số tiền cược phải lớn hơn 0.",
    "coinflip.bet_too_large": "⚠️ Số tiền cược không được quá 1m.",
    "coinflip.not_enough_money": "⚠️ Số dư của bạn không đủ.",

    "coinflip.result.title": "Kết quả Lật Đồng Xu",
    "coinflip.result.line_result": "**Kết quả:** {result}",
    "coinflip.result.win": (
        "🥳 Chúc mừng! Kết quả là **{result}**.\n"
        "Bạn đã dự đoán đúng và nhận thưởng **{reward:,} Ryo**!"
    ),
    "coinflip.result.lose": (
        "😢 Rất tiếc! Kết quả là **{result}**.\n"
        "Bạn đã dự đoán sai và mất hết số tiền cược (**{bet:,} Ryo**)."
    ),
    "coinflip.result.balance": "💰 Số dư hiện tại: **{coin:,} Ryo**",

    "coinflip.error": "❌ Có lỗi xảy ra. Vui lòng thử lại sau.",



    # daily
    "daily.already_claimed": "❗ Bạn đã nhận thưởng hôm nay rồi. Quay lại vào ngày mai nhé!",
    "daily.not_registered": "⚠️ Bạn chưa đăng ký tài khoản. Dùng `/register` trước nhé!",
    "daily.success": "💰 Bạn đã nhận **{reward:,} ryo** (Chuỗi {streak} ngày)! Hẹn gặp lại mai nhé 😄",
    "daily.error": "❌ Có lỗi xảy ra. Vui lòng thử lại sau.",


    # dailytask
    "dailytask.not_registered": "⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!",
    "dailytask.title": "Nhiệm vụ hằng ngày của {username}",
    "dailytask.claimed": "Đã nhận",
    "dailytask.not_enough": "Chưa đủ",
    "dailytask.reward_line": "• 💰 Thưởng: {reward:,} Ryo",
    "dailytask.field_reward_name": "Phần thưởng",
    "dailytask.field_reward_value": "Bạn nhận được {totalReward:,} Ryo từ lần check này.",
    "dailytask.field_info_name": "Thông tin",
    "dailytask.field_info_value": "Hãy nỗ lực hoàn thành các nhiệm vụ để nhận thưởng.",
    "dailytask.error": "❌ Có lỗi xảy ra khi kiểm tra nhiệm vụ hằng ngày. Vui lòng thử lại sau.",

    # per-task description (text only; emoji lấy riêng)
    "dailytask.task.fight_win": "Thắng 10 lần bằng lệnh `/fight`",
    "dailytask.task.minigame": "Chơi 10 lần minigame với bot",
    "dailytask.task.fightwith": "Khiêu chiến 5 lần với bạn bè bằng `/fightwith`",
    "dailytask.task.shop_buy": "Mua đồ trong shop 3 lần",
    "dailytask.task.shop_sell": "Bán đồ cho shop 3 lần",
    "dailytask.task.stage_clear": "Đánh ải ít nhất 1 lần bằng lệnh `/challenge`",
}