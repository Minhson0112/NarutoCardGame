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


    #devinfo
    "devinfo.command_desc": "Hiển thị thông tin nhà phát triển",

    "devinfo.embed.title": "🌟 Thông tin Nhà Phát Triển 🌟",
    "devinfo.embed.description": (
        "Bot được phát triển bởi **{developerName}**.\n\n"
        "Nếu bạn gặp lỗi hoặc có góp ý, hãy nhấn vào [đây]({contactUrl}) để liên hệ.\n\n"
        "Cảm ơn bạn đã sử dụng bot!"
    ),
    "devinfo.embed.author_name": "{authorName}",



    # Command meta
    "fight.command_desc": "Thách đấu người chơi cùng trình độ",

    # Guard / validate
    "fight.already_in_fight": "⚠️ Bạn đang trong trận đấu, vui lòng chờ cho trận trước kết thúc rồi mới /fight tiếp!",
    "fight.not_registered": "⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!",
    "fight.need_full_team": "⚠️ Bạn phải lắp đủ 3 thẻ (Tanker, Middle, Back) mới có thể tham gia đấu!",
    "fight.no_opponent": "⚠️ Hiện không tìm thấy đối thủ phù hợp.",
    "fight.top1_no_opponent": "⚠️ Bạn đang ở Top 1, không có đối thủ.",

    # Battle log
    "fight.team_attack": "Team Tấn Công",
    "fight.team_defense": "Team Phòng Thủ",
    "fight.battle.starting": "Đang khởi đầu trận đấu…",
    "fight.battle.title": "🔥 Battle Log {attacker} VS {defender}",
    "fight.battle.turn_header": "--- Lượt {turn}: {cardName} ---",

    # Result labels
    "fight.result.win": "Chiến Thắng",
    "fight.result.lose": "Thất Bại",
    "fight.result.draw": "🏳️ Hoà",

    # Result texts
    "fight.result.draw_outcome": "⚔️ Hai đội quá cân sức (120 vòng) nên hoà! không bên nào được thưởng.",
    "fight.result.rank_change_win": "**Điểm Rank:** {attacker} +10 điểm, {defender} -5 điểm",
    "fight.result.rank_change_lose": "**Điểm Rank:** {attacker} -10 điểm, {defender} +5 điểm",

    # Final embed
    "fight.result.title": "🏁 Kết quả trận chiến của {attacker} VS {defender}",
    "fight.result.line_result": "🎖️ **Kết quả:** {result}",
    "fight.result.line_reward": "💰**Thưởng:** {reward:,} Ryo",
    "fight.result.line_streak": "🏆**Chuỗi thắng:** {streak}",
    "fight.result.footer_rank": "Điểm Rank: {rankPoints}",

    # Error
    "fight.error": "❌ Có lỗi xảy ra:\n```{trace}```",



    # Command meta
    "fightwith.command_desc": "Pk vui với người chơi đã tag (không cập nhật rank)",
    "fightwith.param.target": "Tag của người chơi bạn muốn pk",

    # Guard / validate
    "fightwith.already_in_fight": "⚠️ Bạn đang trong trận đấu, vui lòng chờ cho trận trước kết thúc rồi mới /fight tiếp!",
    "fightwith.not_registered": "⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!",
    "fightwith.cannot_self": "⚠️ Bạn không thể pk với chính mình.",
    "fightwith.target_not_registered": "⚠️ Người chơi được tag chưa tạo tài khoản.",
    "fightwith.target_not_ready": "⚠️ Người chơi được tag chưa sẵn sàng pk (thiếu thẻ).",
    "fightwith.need_full_team": "⚠️ Bạn phải lắp đủ 3 thẻ (Tanker, Middle, Back) mới có thể tham gia đấu!",

    # Battle log
    "fightwith.team_attack": "Team Tấn Công",
    "fightwith.team_defense": "Team Phòng Thủ",
    "fightwith.battle.starting": "Đang khởi đầu trận đấu…",
    "fightwith.battle.title": "🔥 Battle Log {attacker} VS {defender}",
    "fightwith.battle.turn_header": "--- Lượt {turn}: {cardName} ---",

    # Result labels
    "fightwith.result.win": "Chiến Thắng",
    "fightwith.result.lose": "Thất Bại",
    "fightwith.result.draw": "🏳️ Hoà",

    # Result texts
    "fightwith.result.draw_outcome": "⚔️ Hai đội quá cân sức (120 vòng) nên hoà!.",
    "fightwith.result.no_rank_note": "**Điểm Rank:** vì không phải đánh rank nên không ai nhận được thưởng hay điểm rank.",
    "fightwith.result.streak_unchanged": "Không bị thay đổi",

    # Final embed
    "fightwith.result.title": "🏁 Kết quả trận chiến của {attacker} VS {defender}",
    "fightwith.result.line_result": "🎖️ **Kết quả:** {result}",
    "fightwith.result.line_reward": "💰**Thưởng:** {reward:,} Ryo",
    "fightwith.result.line_streak": "🏆**Chuỗi thắng:** {streak}",
    "fightwith.result.footer_rank": "Điểm Rank: {rankPoints}",

    # Error
    "fightwith.error_generic": "❌ Có lỗi xảy ra. Vui lòng thử lại sau.",



    # Command meta
    "giftcode.command_desc": "Sử dụng mã GIFT để nhận quà",
    "giftcode.param.code": "Mã GIFT bạn muốn sử dụng",

    # Validate
    "giftcode.not_registered": "⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!",
    "giftcode.not_found": "⚠️ Mã GIFT không tồn tại. Vui lòng kiểm tra lại.",
    "giftcode.expired": "⚠️ Mã GIFT này đã hết hạn sử dụng.",
    "giftcode.already_used": "⚠️ Bạn đã sử dụng mã GIFT này trước đó và không thể sử dụng lại.",

    # Reward item labels (parts)
    "giftcode.reward.ryo": "Bonus Ryo: {amount:,} Ryo",
    "giftcode.reward.card": "Thẻ: {name}",
    "giftcode.reward.weapon": "Vũ khí: {name}",
    "giftcode.reward.weapon_default": "Vũ khí",
    "giftcode.reward.none": "Không có phần thưởng nào.",

    # Success message
    "giftcode.success.title": "✅ Bạn đã sử dụng thành công mã GIFT!",
    "giftcode.success.detail": "Phần quà nhận được: {rewards}",

    # Error
    "giftcode.error_generic": "❌ Có lỗi xảy ra. Vui lòng thử lại sau.",



    # Command meta
    "give.command_desc": "Chuyển tiền cho người khác",
    "give.param.target": "Tag của người nhận",
    "give.param.amount": "Số Ryo cần chuyển",

    # Validate
    "give.amount_invalid": "⚠️ Số tiền chuyển phải lớn hơn 0.",
    "give.sender_not_registered": "⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!",
    "give.receiver_not_registered": "⚠️ Người nhận chưa đăng ký tài khoản.",
    "give.insufficient_balance": "⚠️ Số tiền chuyển vượt quá số dư của bạn.",

    # Daily limit
    "give.limit_exceeded": (
        "⚠️ Người nhận đang ở cấp **{level}**, chỉ được nhận tối đa **{limit:,} Ryo** mỗi ngày.\n\n"
        "Hiện đã nhận **{received:,} Ryo** hôm nay."
    ),

    # Success
    "give.success": "✅ Bạn đã chuyển **{amount:,} Ryo** cho {mention}.",

    # Error
    "give.error_generic": "❌ Có lỗi xảy ra. Vui lòng thử lại sau.",



    # Command meta
    "giveawayryo.command_desc": "Tặng Ryo (chỉ admin)",
    "giveawayryo.param.target": "Tag của người nhận",
    "giveawayryo.param.amount": "Số Ryo muốn tặng",

    # Validate / permission
    "giveawayryo.no_permission": "⚠️ Bạn không có quyền sử dụng lệnh này. Hãy dùng /give để chuyển tiền.",
    "giveawayryo.amount_invalid": "⚠️ Số Ryo tặng phải lớn hơn 0.",
    "giveawayryo.receiver_not_registered": "⚠️ Người nhận chưa đăng ký tài khoản.",

    # Success
    "giveawayryo.success": "✅ Đã giveaway **{amount:,} Ryo** cho {mention}.",

    # Error
    "giveawayryo.error_generic": "❌ Có lỗi xảy ra. Vui lòng thử lại sau.",



    # command meta
    "help.command_desc": "Hướng dẫn cho người mới bắt đầu sử dụng bot",

    # embeds: overview
    "help.embed.overview.title": "📜 Giới thiệu game",
    "help.embed.overview.desc": (
        "Game của chúng ta xoay quanh việc thu thập các thẻ nhân vật từ anime **Naruto** với độ hiếm khác nhau. \n"
        "Bạn sẽ sử dụng các thẻ này để **PK** với nhau, tham gia đánh ải cốt truyện, leo bảng xếp hạng và trải nghiệm nhiều trò chơi thú vị khác."
    ),

    # embeds: start
    "help.embed.start.title": "🚀 Xuất phát nào",
    "help.embed.start.desc": "• Tạo tài khoản ngay bằng lệnh ``/register`` để bắt đầu hành trình của bạn.",

    # embeds: earn
    "help.embed.earn.title": "💰 Cách kiếm tiền",
    "help.embed.earn.desc": (
        "1. Điểm danh mỗi ngày bằng lệnh ``/daily`` để nhận tiền điểm danh.\n\n"
        "2. Hoàn thành các nhiệm vụ hằng ngày bằng lệnh ``/dailytask`` để nhận thưởng.\n\n"
        "3. Tham gia đánh ải cốt truyện bằng lệnh ``/challenge`` – càng đánh càng được thưởng nhiều.\n\n"
        "4. Thử vận may với lệnh ``/fight`` để leo bảng xếp hạng; chuỗi thắng cao sẽ nhận thêm tiền.\n\n"
        "5. Chơi minigame với bot qua các lệnh ``/slot``, ``/blackjack``, ``/coinflip``, ``/bingo`` để kiếm tiền.\n\n"
        "6. Mua gói thẻ rẻ (với tỷ lệ rơi thẻ hiếm) và bán chúng bằng lệnh ``/sellcard`` hoặc ``/sellweapon`` để kiếm lời.\n\n"
        "7. Đi viễn chinh bằng ``/adventure``, thắng sẽ nhận được tiền.\n\n"
        "8. Đánh boss vĩ thú bằng ``/tailedboss``, nhận được tiền theo sát thương gây ra; hạ gục vĩ thú sẽ có tỉ lệ nhận được thẻ và vũ khí.\n\n"
    ),

    # embeds: interact
    "help.embed.interact.title": "🃏 Cách tương tác với thẻ và vũ khí",
    "help.embed.interact.desc": (
        "1. Ghé shop thẻ bằng lệnh ``/shop`` để xem các gói thẻ, tỷ lệ rơi và cách mua, cũng như số lần cần mua để đảm bảo nhận được thẻ hiếm (được cá nhân hóa cho từng người chơi).\n\n"
        "2. Sau khi mua, kiểm tra kho của bạn bằng lệnh ``/inventory``.\n\n"
        "3. Tương tự, bạn có thể vào shop vũ khí để mua vũ khí qua các lệnh tương tự.\n\n"
        "4. Nâng cấp thẻ và vũ khí bằng lệnh ``/levelupcard`` và ``/levelupweapon`` (nâng cấp sẽ tăng sức mạnh nếu bạn có các thẻ hoặc vũ khí giống nhau).\n\n"
        "5. Lắp thẻ mạnh nhất và vũ khí mạnh nhất vào hồ sơ của bạn bằng lệnh ``/setcard`` và ``/setweapon`` để chuẩn bị chiến đấu với các người chơi khác.\n\n"
        "6. Chi tiết luật chiến đấu ở ``/battlerule``.\n\n"
    ),

    # embeds: community
    "help.embed.community.title": "🌐 Máy chủ cộng đồng",
    "help.embed.community.desc": (
        "• Tham gia [máy chủ cộng đồng]({community_link}) của chúng ta để nhận thông báo về **giftcode** và các event hấp dẫn của bot.\n\n"
    ),



    "inventory.command_desc": "Hiển thị kho đồ của bạn",

    "inventory.embed.cards.title": "🎴 Kho Thẻ Bài",
    "inventory.embed.weapons.title": "🔪 Kho Vũ Khí",

    "inventory.embed.cards.empty": "Không có thẻ nào.",
    "inventory.embed.weapons.empty": "Không có vũ khí nào.",

    "inventory.footer.page": "Trang {page}/{total}",

    "inventory.button.prev": "Trước",
    "inventory.button.next": "Tiếp",
    "inventory.button.to_weapons": "Kho vũ khí",
    "inventory.button.to_cards": "Kho thẻ",

    "inventory.msg.first_page": "Bạn đang ở trang đầu!",
    "inventory.msg.last_page": "Bạn đang ở trang cuối!",

    "inventory.error.not_registered": "Bạn chưa đăng ký tài khoản. Hãy dùng `/register` trước nhé!",

    "inventory.field.id": "ID",
    "inventory.field.tier": "Bậc",
    "inventory.field.grade": "Bậc",
    "inventory.field.tanker": "Tanker",
    "inventory.field.quantity": "Số Lượng",
    "inventory.field.quantity_weapon": "Số Lượng",

    "inventory.card.locked_marker": " (🔒)",

    "inventory.buff.damage": "Damage",
    "inventory.buff.health": "Hp",
    "inventory.buff.armor": "Armor",
    "inventory.buff.crit_rate": "Crit Rate",
    "inventory.buff.speed": "Speed",
    "inventory.buff.chakra": "Chakra",



    "levelupweapon.command_desc": "Nâng cấp vũ khí của bạn (tăng 1 cấp)",
    "levelupweapon.param.weapon_id": "ID vũ khí bạn muốn nâng cấp (xem trong /inventory)",

    "levelupweapon.error.not_registered": "Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!",
    "levelupweapon.error.not_owner": "Bạn không sở hữu vũ khí với ID `{weapon_id}`. Kiểm tra lại trong /inventory.",
    "levelupweapon.error.invalid_data": "Dữ liệu vũ khí không hợp lệ. Vui lòng thử lại sau.",

    "levelupweapon.error.not_highest_level": (
        "Bạn chỉ có thể nâng cấp từ vũ khí cấp cao nhất.\n"
        "Vũ khí với ID `{weapon_id}` đang ở cấp {current_level}, "
        "nhưng vũ khí cao nhất của bạn là cấp {highest_level}."
    ),

    "levelupweapon.error.equipped": (
        "Vũ khí **{weapon_name}** (ID `{weapon_id}`) "
        "đang được trang bị, hãy tháo nó ra bằng lệnh /unequipweapon trước khi nâng cấp."
    ),

    "levelupweapon.error.not_enough_materials": (
        "Bạn không có đủ vũ khí **{weapon_name}** cấp 1 để nâng cấp.\n"
        "Yêu cầu: {required}, hiện có: {current}."
    ),

    "levelupweapon.success": (
        "Nâng cấp thành công! Vũ khí **{weapon_name}** "
        "(ID `{new_weapon_id}`) đã được nâng từ cấp {from_level} lên cấp {to_level}."
    ),

    "levelupweapon.error.generic": "Có lỗi xảy ra. Vui lòng thử lại sau.",



    "levelupcard.command_desc": "Nâng cấp thẻ của bạn (tăng 1 cấp)",
    "levelupcard.param.card_id": "ID thẻ bạn muốn nâng cấp (xem trong /inventory)",

    "levelupcard.error.not_registered": "Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!",
    "levelupcard.error.not_owner": "Bạn không sở hữu thẻ với ID `{card_id}`. Kiểm tra lại trong /inventory.",

    "levelupcard.error.max_level": "Cấp thẻ lớn nhất có thể nâng cấp là 50. Thẻ này đang ở cấp {current_level}.",
    "levelupcard.error.invalid_data": "Dữ liệu thẻ không hợp lệ. Vui lòng thử lại sau.",

    "levelupcard.error.not_highest_level": (
        "Bạn chỉ có thể nâng cấp từ thẻ cấp cao nhất.\n"
        "Thẻ với ID `{card_id}` đang ở cấp {current_level}, "
        "nhưng thẻ cao nhất của bạn là cấp {highest_level}."
    ),

    "levelupcard.error.equipped": (
        "Thẻ **{card_name}** (ID `{card_id}`) đang được dùng làm thẻ chính, "
        "hãy tháo thẻ đó ra bằng lệnh /setcard một thẻ khác trước khi nâng cấp."
    ),

    "levelupcard.error.not_enough_materials": (
        "Bạn không có đủ thẻ **{card_name}** cấp 1 để nâng cấp.\n"
        "Yêu cầu: {required}, hiện có: {current}."
    ),

    "levelupcard.success": (
        "Nâng cấp thành công! Thẻ **{card_name}** "
        "(ID `{new_card_id}`) đã được nâng từ cấp {from_level} lên cấp {to_level}."
    ),

    "levelupcard.error.generic": "Có lỗi xảy ra. Vui lòng thử lại sau.",



    "lockcard.command_desc": "Khoá toàn bộ thẻ cùng loại, thẻ bị khoá sẽ không thể bán",
    "lockcard.param.card_id": "ID thẻ bạn muốn khoá (xem trong /inventory)",

    "lockcard.error.not_registered": "Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!",
    "lockcard.error.not_owner": "Bạn không sở hữu thẻ với ID `{card_id}`.",
    "lockcard.error.not_found_same_type": "Không tìm thấy các bản thẻ cùng loại để khoá.",

    "lockcard.success": (
        "Đã khoá **toàn bộ thẻ `{card_name}`** của bạn "
        "(bao gồm mọi cấp độ & phôi)."
    ),

    "lockcard.error.generic": "Có lỗi xảy ra khi khoá thẻ. Vui lòng thử lại sau.",
}