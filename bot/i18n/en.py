EN = {
    # battlerule
    "battlerule.title": "📜 Battle Rules",
    "battlerule.desc": (
        "🔹 Each team has 3 cards (Tanker, Middle, Back) (weapons are already included if equipped)\n"
        "🏎️ The team with the higher total **Speed** gets to attack **first**\n"
        "🎯 Basic attacks prioritize targets in this order: **Tanker → Middle → Back**\n"
        "💧 When a card's **Chakra** reaches **100**, on its next turn it will use its **Special Skill**\n"
        "💧 A card's **Chakra** increases by 20 after each attack or when it finishes an enemy, and also increases when taking damage based on the % of max HP lost\n"
        "💀 The battle ends when one side has all **3 cards defeated**\n"
        "⏳ If there is no winner after **120 turns**, the match ends in a **draw**\n"
        "⚔️ View a card's special skill with the `/showcard` command"
    ),


    # Command: /adventure
    "adventure.not_registered": "⚠️ You haven't registered yet. Please use /register first!",
    "adventure.need_full_team": "⚠️ You must equip all 3 cards (Tanker, Middle, Back) to join the battle!",

    # Battle log
    "adventure.battle.starting": "Starting the battle…",
    "adventure.battle.title": "🔎 {username} went exploring and got ambushed by {teamName}",
    "adventure.battle.turn_header": "--- Turn {turn}: {cardName} ---",

    # Result (final embed)
    "adventure.result.title": "🏁 Battle Result: {username} VS {teamName}",
    "adventure.result.line_result": "🎖️ **Result:** {result}",
    "adventure.result.reward_draw": "💰**Reward:** {reward:,} Ryo",
    "adventure.result.outcome_draw": "⚔️ Both teams retreated, so it's a draw! No reward. Come back in 5 minutes.",
    "adventure.result.result_win": "Victory",
    "adventure.result.result_lose": "Defeat",
    "adventure.result.result_draw": "🏳️ Draw",

    "adventure.result.reward_win": "💰**Reward:** Looted {reward:,} Ryo from {teamName}'s bodies",
    "adventure.result.outcome_win": "You defeated {teamName} and claimed your reward. Come back in 5 minutes.",

    "adventure.result.reward_lose": "💰**Reward:** {teamName} said you're too green and didn't even bother taking your money",
    "adventure.result.outcome_lose": "You lost to {teamName} and got nothing. Come back in 5 minutes.",

    "adventure.result.footer_rank": "Rank Points: {rankPoints}",

    # Cooldown error
    "adventure.cooldown": "⏱️ You must wait **{seconds:.1f}** more seconds before going on another adventure.",

    # Generic error
    "adventure.error": "❌ An error occurred:\n```{trace}```",
    "adventure.team_names": [
        "The Tryhard Squad",
        "Loud Lungs Crew",
        "Village Wreckers",
        "Keyboard Yakuza",
        "Scorpio Gang",
        "Do You Know My Dad?",
        "Wrench-in-the-Gears Team",
        "Gambling Addicts United",
        "The Perfect Kids Club",
        "So You Chose Death",
        "1vEveryone Enjoyers",
        "Patience? Never Heard Of It",
        "Budget Hackers",
        "Zero-Slip Legends",
        "Too Young Too Wild",
        "Headbutt & Run",
        "Hot Goods Dealers",
        "Teddy Bears With Fangs",
        "Blood-Rush Brigade",
        "Weeb Nation",
        "Red Devils Fanclub",
        "Bottom of Society",
        "Construction Kings",
        "K-Pop Main Characters",
        "Fireflies Crew",
        "Peter Fans Association",
    ],


    # /bingo command
    "bingo.not_registered": "⚠️ You haven't registered yet. Please use /register first!",
    "bingo.bet_invalid": "⚠️ Your bet must be greater than 0.",
    "bingo.bet_too_large": "⚠️ Your bet cannot exceed 1,000,000.",
    "bingo.not_enough_balance": "⚠️ You don't have enough balance.",

    # Intro / instruction message (content)
    "bingo.intro": (
        "🌟 **Bingo Time!** 🌟\n\n"
        "Pick a lucky number from **1️⃣** to **5️⃣**!\n"
        "Bet: **{bet} Ryo**\n"
        "❗ Guess right on the 1st try: get **x4** 🎉\n"
        "❗ Guess right on the 2nd try: get **x2** 😄\n"
        "❗ Miss both tries: lose your bet 😢"
    ),

    # Outcome texts (used inside embed description)
    "bingo.win_first_try": (
        "🥳 Congrats! The lucky number was {numberEmoji}.\n"
        "You got it on the first try and won **{reward} Ryo**! 🎉"
    ),
    "bingo.win_second_try": (
        "😊 Nice! The lucky number was {numberEmoji}.\n"
        "You got it on the second try and won **{reward} Ryo**! 👍"
    ),
    "bingo.lose": (
        "😢 Unlucky! The lucky number was {numberEmoji}.\n"
        "Wrong pick. You lost your bet (**{bet} Ryo**)."
    ),

    # Result embed
    "bingo.result_embed.title": "🎲 Bingo Result 🎲",
    "bingo.result_embed.desc": (
        "Lucky number: {numberEmoji}\n\n"
        "{outcomeText}\n\n"
        "💰 Current balance: **{balance} Ryo**"
    ),

    # Error
    "bingo.error": "❌ Something went wrong. Please try again later.",


    #blackjack
    "blackjack.not_registered": "⚠️ You haven’t registered yet. Please use /register first!",
    "blackjack.bet_invalid": "⚠️ Your bet must be greater than 0.",
    "blackjack.bet_too_large": "⚠️ Your bet cannot exceed 1,000,000.",
    "blackjack.not_enough_balance": "⚠️ You don’t have enough balance.",
    "blackjack.error": "❌ Something went wrong. Please try again later.",

    "blackjack.embed.title": "♠️ Blackjack Game ♣️",
    "blackjack.embed.player_hand": "**Your hand:** {cards} (Total: {total})",
    "blackjack.embed.dealer_hand": "**Dealer’s hand:** {cards} (Total: {total})",
    "blackjack.embed.dealer_hidden": "**Dealer’s hand:** {cards}",
    "blackjack.embed.actions": "🟢: Hit | 🔴: Stand",
    "blackjack.embed.bet": "Bet: {bet}",
    "blackjack.embed.dealer_drawing": "Dealer is drawing cards...",
    "blackjack.embed.dealer_start_drawing": "Dealer starts drawing...",
    "blackjack.embed.dealer_draw": "Dealer draws a card...",
    "blackjack.embed.balance": "Current balance: **{balance}**",

    "blackjack.outcome.double_ace_win": "🎉 Double Aces! You win 4x!",
    "blackjack.outcome.double_ace_lose": "😢 Dealer has Double Aces! You lose 4x!",
    "blackjack.outcome.double_ace_draw": "🤝 Both have Double Aces! It’s a draw!",

    "blackjack.outcome.blackjack_win": "🎉 Blackjack! You win 3x!",
    "blackjack.outcome.blackjack_both": "😢 Both have blackjack! Dealer wins!",
    "blackjack.outcome.blackjack_lose": "😢 Dealer has blackjack! You lose!",

    "blackjack.outcome.five_card_win": "🎉 Five-card trick (<= 21)! You win instantly!",
    "blackjack.outcome.player_bust_lose": "😢 You busted. You lose!",
    "blackjack.outcome.both_bust_draw": "🤝 Dealer also busted. It’s a draw — you don’t lose money!",
    "blackjack.outcome.dealer_after_draw_lose": "😢 After drawing, the dealer has {dealerTotal}. You lose!",

    "blackjack.outcome.dealer_five_card_lose": "😢 Dealer got 5 cards without busting (<= 21). You lose!",
    "blackjack.outcome.dealer_bust_win": "🎉 Dealer busted! You win!",

    "blackjack.outcome.win": "🎉 You win!",
    "blackjack.outcome.lose": "😢 You lose!",
    "blackjack.outcome.draw": "🤝 Draw!",


    #buy card
    "buycard.not_registered": "⚠️ You are not registered yet. Please use `/register` first!",

    "buycard.invalid_pack": "❌ Pack '{pack}' is invalid. Please choose: {validPacks}",
    "buycard.not_enough_balance": "❌ Not enough balance. Need {cost:,} Ryo, you have {balance:,} Ryo.",
    "buycard.open_pack_not_found": "❌ Failed to open the pack. No suitable card was found.",

    "buycard.result.title": "🎉 You bought {pack} and pulled: {cardName}",
    "buycard.result.stats.damage": "**Damage:** {value}",
    "buycard.result.stats.hp": "**HP:** {value}",
    "buycard.result.stats.armor": "**Armor:** {value}",
    "buycard.result.stats.crit_rate": "**Crit Rate:** {value}",
    "buycard.result.stats.dodge": "**Dodge:** {value}",
    "buycard.result.stats.base_chakra": "**Base Chakra:** {value}",
    "buycard.result.stats.tanker": "**Tanker:** {value}",
    "buycard.result.stats.tier": "**Tier:** {value}",
    "buycard.result.stats.element": "**Chakra Element:** {value}",
    "buycard.result.stats.sell_price": "**Sell Price:** {value:,} Ryo",

    "buycard.common.yes": "✅",
    "buycard.common.no": "❌",

    "buycard.result.added_to_inventory": "The card has been added to your inventory. Check it with `/inventory`.",
    "buycard.result.skill_title": "📜 **Special Skill:**",
    "buycard.skill_missing": "No special skill yet.",

    "buycard.cooldown": "⏱️ Please wait **{seconds:.1f}** more seconds before opening another pack.",
    "buycard.error": "❌ Something went wrong. Please try again later.",


    # buymulticard
    "buymulticard.cooldown": "⏱️ Still on cooldown. Please wait **{remaining}**s.",
    "buymulticard.not_registered": "⚠️ You are not registered yet. Use `/register` first!",
    "buymulticard.count_invalid": "⚠️ Count must be greater than 0.",
    "buymulticard.level_required": "⚠️ This feature is only available for players level 2 or higher.",
    "buymulticard.count_limit": "⚠️ You are level {level}, so you can buy up to {maxPack} packs per request.",
    "buymulticard.pack_invalid": "⚠️ Invalid pack.",
    "buymulticard.not_enough_balance": "❌ You need {totalCost:,} Ryo, but you only have {balance:,}.",
    "buymulticard.success_header": "✅ Successfully bought **{count} {pack}** and received:",
    "buymulticard.item_line": "🥷 {name} ({tier}) x {qty}",
    "buymulticard.error": "❌ Something went wrong. Please try again later.",


    # buyweapon
    "buyweapon.not_registered": "⚠️ You are not registered yet. Use `/register` first!",
    "buyweapon.pack_invalid": "❌ Invalid pack '{pack}'. Please choose: {validPacks}",
    "buyweapon.not_enough_balance": "❌ Not enough balance. Need {cost:,} Ryo, you have {balance:,} Ryo.",
    "buyweapon.no_weapon_found": "❌ Failed to open the pack: no suitable weapon found.",
    "buyweapon.error": "❌ Something went wrong. Please try again later.",

    "buyweapon.embed.title": "🎉 You bought {pack} and pulled a weapon: {weaponName}",
    "buyweapon.embed.line_bonus_damage": "**Bonus Damage:** {value}",
    "buyweapon.embed.line_bonus_health": "**Bonus HP:** {value}",
    "buyweapon.embed.line_bonus_armor": "**Bonus Armor:** {value}",
    "buyweapon.embed.line_bonus_crit_rate": "**Bonus Crit Rate:** {value}",
    "buyweapon.embed.line_bonus_speed": "**Bonus Evasion:** {value}",
    "buyweapon.embed.line_bonus_chakra": "**Bonus Chakra:** {value}",
    "buyweapon.embed.line_grade": "**Grade:** {grade}",
    "buyweapon.embed.line_sell_price": "**Sell price:** {price:,} Ryo",
    "buyweapon.embed.added_to_inventory": "The weapon has been added to your inventory. Check it with `/inventory`.",
    "buyweapon.embed.passive_title": "📜 **Weapon Passive:**",
    "buyweapon.embed.skill_missing": "No passive available yet.",


    # checkmoney
    "checkmoney.not_registered": "⚠️ You are not registered yet. Use `/register` first!",
    "checkmoney.balance": "💰 Your current balance is **{coin:,} Ryo**",
    "checkmoney.error": "❌ Something went wrong. Please try again later.",



    # coinflip
    "coinflip.invalid_guess": "⚠️ Please enter a valid guess: **u** or **n**.",
    "coinflip.not_registered": "⚠️ You are not registered yet. Use /register first!",
    "coinflip.bet_must_be_positive": "⚠️ Bet amount must be greater than 0.",
    "coinflip.bet_too_large": "⚠️ Bet amount cannot be greater than 1,000,000.",
    "coinflip.not_enough_money": "⚠️ You don't have enough balance.",

    "coinflip.result.title": "Coin Flip Result",
    "coinflip.result.line_result": "**Result:** {result}",
    "coinflip.result.win": (
        "🥳 Congrats! The result is **{result}**.\n"
        "You guessed correctly and won **{reward:,} Ryo**!"
    ),
    "coinflip.result.lose": (
        "😢 Unlucky! The result is **{result}**.\n"
        "You guessed wrong and lost your bet (**{bet:,} Ryo**)."
    ),
    "coinflip.result.balance": "💰 Current balance: **{coin:,} Ryo**",

    "coinflip.error": "❌ Something went wrong. Please try again later.",



    # daily
    "daily.already_claimed": "❗ You already claimed today's reward. Come back tomorrow!",
    "daily.not_registered": "⚠️ You are not registered yet. Use `/register` first!",
    "daily.success": "💰 You received **{reward:,} ryo** (Streak: {streak} days)! See you tomorrow 😄",
    "daily.error": "❌ Something went wrong. Please try again later.",



    # dailytask
    "dailytask.not_registered": "⚠️ You are not registered yet. Use /register first!",
    "dailytask.title": "Daily tasks for {username}",
    "dailytask.claimed": "Claimed",
    "dailytask.not_enough": "Not enough",
    "dailytask.reward_line": "• 💰 Reward: {reward:,} Ryo",
    "dailytask.field_reward_name": "Rewards",
    "dailytask.field_reward_value": "You received {totalReward:,} Ryo from this check.",
    "dailytask.field_info_name": "Info",
    "dailytask.field_info_value": "Complete tasks to claim rewards.",
    "dailytask.error": "❌ Failed to check daily tasks. Please try again later.",

    # per-task description
    "dailytask.task.fight_win": "Win 10 times using `/fight`",
    "dailytask.task.minigame": "Play minigames 10 times",
    "dailytask.task.fightwith": "Challenge friends 5 times using `/fightwith`",
    "dailytask.task.shop_buy": "Buy from the shop 3 times",
    "dailytask.task.shop_sell": "Sell to the shop 3 times",
    "dailytask.task.stage_clear": "Clear at least 1 stage using `/challenge`",
}