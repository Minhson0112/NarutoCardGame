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


    #devinfo
    "devinfo.command_desc": "Show developer information",

    "devinfo.embed.title": "🌟 Developer Info 🌟",
    "devinfo.embed.description": (
        "This bot is developed by **{developerName}**.\n\n"
        "If you find a bug or have feedback, click [here]({contactUrl}) to contact.\n\n"
        "Thanks for using the bot!"
    ),
    "devinfo.embed.author_name": "{authorName}",



    # Command meta
    "fight.command_desc": "Challenge an opponent near your rank",

    # Guard / validate
    "fight.already_in_fight": "⚠️ You're already in a battle. Please wait until it ends before using /fight again!",
    "fight.not_registered": "⚠️ You haven't registered yet. Use /register first!",
    "fight.need_full_team": "⚠️ You must equip 3 cards (Tanker, Middle, Back) to join a fight!",
    "fight.no_opponent": "⚠️ No suitable opponent found right now.",
    "fight.top1_no_opponent": "⚠️ You're Top 1. No opponent available.",

    # Battle log
    "fight.team_attack": "Attack Team",
    "fight.team_defense": "Defense Team",
    "fight.battle.starting": "Starting the battle…",
    "fight.battle.title": "🔥 Battle Log {attacker} VS {defender}",
    "fight.battle.turn_header": "--- Turn {turn}: {cardName} ---",

    # Result labels
    "fight.result.win": "Victory",
    "fight.result.lose": "Defeat",
    "fight.result.draw": "🏳️ Draw",

    # Result texts
    "fight.result.draw_outcome": "⚔️ The fight reached 120 turns and ended in a draw. No rewards for either side.",
    "fight.result.rank_change_win": "**Rank Points:** {attacker} +10, {defender} -5",
    "fight.result.rank_change_lose": "**Rank Points:** {attacker} -10, {defender} +5",

    # Final embed
    "fight.result.title": "🏁 Battle Result: {attacker} VS {defender}",
    "fight.result.line_result": "🎖️ **Result:** {result}",
    "fight.result.line_reward": "💰**Reward:** {reward:,} Ryo",
    "fight.result.line_streak": "🏆**Win Streak:** {streak}",
    "fight.result.footer_rank": "Rank Points: {rankPoints}",

    # Error
    "fight.error": "❌ An error occurred:\n```{trace}```",



    # Command meta
    "fightwith.command_desc": "Friendly PK with a tagged player (no rank changes)",
    "fightwith.param.target": "Tag the player you want to PK",

    # Guard / validate
    "fightwith.already_in_fight": "⚠️ You're already in a battle. Please wait until it ends before using /fight again!",
    "fightwith.not_registered": "⚠️ You haven't registered yet. Use /register first!",
    "fightwith.cannot_self": "⚠️ You can't PK yourself.",
    "fightwith.target_not_registered": "⚠️ The tagged player hasn't registered yet.",
    "fightwith.target_not_ready": "⚠️ The tagged player isn't ready to PK (missing cards).",
    "fightwith.need_full_team": "⚠️ You must equip 3 cards (Tanker, Middle, Back) to join a fight!",

    # Battle log
    "fightwith.team_attack": "Attack Team",
    "fightwith.team_defense": "Defense Team",
    "fightwith.battle.starting": "Starting the battle…",
    "fightwith.battle.title": "🔥 Battle Log {attacker} VS {defender}",
    "fightwith.battle.turn_header": "--- Turn {turn}: {cardName} ---",

    # Result labels
    "fightwith.result.win": "Victory",
    "fightwith.result.lose": "Defeat",
    "fightwith.result.draw": "🏳️ Draw",

    # Result texts
    "fightwith.result.draw_outcome": "⚔️ The fight reached 120 turns and ended in a draw.",
    "fightwith.result.no_rank_note": "**Rank Points:** This is not a ranked match, so no one gets rewards or rank points.",
    "fightwith.result.streak_unchanged": "Unchanged",

    # Final embed
    "fightwith.result.title": "🏁 Battle Result: {attacker} VS {defender}",
    "fightwith.result.line_result": "🎖️ **Result:** {result}",
    "fightwith.result.line_reward": "💰**Reward:** {reward:,} Ryo",
    "fightwith.result.line_streak": "🏆**Win Streak:** {streak}",
    "fightwith.result.footer_rank": "Rank Points: {rankPoints}",

    # Error
    "fightwith.error_generic": "❌ Something went wrong. Please try again later.",



    # Command meta
    "giftcode.command_desc": "Use a GIFT code to claim rewards",
    "giftcode.param.code": "The GIFT code you want to use",

    # Validate
    "giftcode.not_registered": "⚠️ You haven't registered yet. Use /register first!",
    "giftcode.not_found": "⚠️ This GIFT code doesn't exist. Please double-check it.",
    "giftcode.expired": "⚠️ This GIFT code has expired.",
    "giftcode.already_used": "⚠️ You've already used this GIFT code and can't use it again.",

    # Reward item labels (parts)
    "giftcode.reward.ryo": "Bonus Ryo: {amount:,} Ryo",
    "giftcode.reward.card": "Card: {name}",
    "giftcode.reward.weapon": "Weapon: {name}",
    "giftcode.reward.weapon_default": "Weapon",
    "giftcode.reward.none": "No rewards.",

    # Success message
    "giftcode.success.title": "✅ GIFT code redeemed successfully!",
    "giftcode.success.detail": "Rewards received: {rewards}",

    # Error
    "giftcode.error_generic": "❌ Something went wrong. Please try again later.",



    # Command meta
    "give.command_desc": "Transfer money to another player",
    "give.param.target": "The recipient you want to tag",
    "give.param.amount": "Amount of Ryo to transfer",

    # Validate
    "give.amount_invalid": "⚠️ Transfer amount must be greater than 0.",
    "give.sender_not_registered": "⚠️ You haven't registered yet. Use /register first!",
    "give.receiver_not_registered": "⚠️ The recipient hasn't registered yet.",
    "give.insufficient_balance": "⚠️ You don't have enough balance for that transfer.",

    # Daily limit
    "give.limit_exceeded": (
        "⚠️ The recipient is level **{level}** and can receive at most **{limit:,} Ryo** per day.\n\n"
        "They have already received **{received:,} Ryo** today."
    ),

    # Success
    "give.success": "✅ You transferred **{amount:,} Ryo** to {mention}.",

    # Error
    "give.error_generic": "❌ Something went wrong. Please try again later.",



    # Command meta
    "giveawayryo.command_desc": "Give Ryo (admin only)",
    "giveawayryo.param.target": "The recipient you want to tag",
    "giveawayryo.param.amount": "Amount of Ryo to give",

    # Validate / permission
    "giveawayryo.no_permission": "⚠️ You don't have permission to use this command. Use /give to transfer money.",
    "giveawayryo.amount_invalid": "⚠️ Giveaway amount must be greater than 0.",
    "giveawayryo.receiver_not_registered": "⚠️ The recipient hasn't registered yet.",

    # Success
    "giveawayryo.success": "✅ Gave **{amount:,} Ryo** to {mention}.",

    # Error
    "giveawayryo.error_generic": "❌ Something went wrong. Please try again later.",



    # command meta
    "help.command_desc": "A quick guide for new players to use the bot",

    # embeds: overview
    "help.embed.overview.title": "📜 Game Overview",
    "help.embed.overview.desc": (
        "Our game is all about collecting **Naruto** character cards with different rarities.\n"
        "You will use these cards to **PK** other players, clear story stages, climb the leaderboard, and enjoy many other fun activities."
    ),

    # embeds: start
    "help.embed.start.title": "🚀 Getting Started",
    "help.embed.start.desc": "• Create your account with ``/register`` to begin your journey.",

    # embeds: earn
    "help.embed.earn.title": "💰 How to Earn Money",
    "help.embed.earn.desc": (
        "1. Claim your daily reward with ``/daily``.\n\n"
        "2. Complete daily missions with ``/dailytask`` to earn rewards.\n\n"
        "3. Clear story stages with ``/challenge`` — the more you clear, the more you earn.\n\n"
        "4. Try your luck with ``/fight`` to climb the ranking; longer win streaks give extra money.\n\n"
        "5. Play minigames like ``/slot``, ``/blackjack``, ``/coinflip``, ``/bingo`` to earn money.\n\n"
        "6. Buy cheaper card packs (with a chance to drop rare cards) and sell them using ``/sellcard`` or ``/sellweapon`` for profit.\n\n"
        "7. Go on an expedition with ``/adventure`` — winning gives you money.\n\n"
        "8. Fight the tailed beast boss with ``/tailedboss`` — earn money based on damage dealt; the last hit has a chance to drop cards and weapons.\n\n"
    ),

    # embeds: interact
    "help.embed.interact.title": "🃏 Cards & Weapons Guide",
    "help.embed.interact.desc": (
        "1. Open the card shop with ``/shop`` to see packs, drop rates, how to buy, and how many pulls are needed to guarantee rare cards (personalized per player).\n\n"
        "2. After buying, check your inventory with ``/inventory``.\n\n"
        "3. Similarly, you can visit the weapon shop via its related commands.\n\n"
        "4. Upgrade cards and weapons using ``/levelupcard`` and ``/levelupweapon`` (upgrades increase power if you have duplicates).\n\n"
        "5. Equip your best cards and weapons using ``/setcard`` and ``/setweapon`` to prepare for battles.\n\n"
        "6. See the full battle rules with ``/battlerule``.\n\n"
    ),

    # embeds: community
    "help.embed.community.title": "🌐 Community Server",
    "help.embed.community.desc": (
        "• Join our [community server]({community_link}) to get **giftcode** announcements and bot events.\n\n"
    ),



    "inventory.command_desc": "Show your inventory",

    "inventory.embed.cards.title": "🎴 Card Inventory",
    "inventory.embed.weapons.title": "🔪 Weapon Inventory",

    "inventory.embed.cards.empty": "You have no cards.",
    "inventory.embed.weapons.empty": "You have no weapons.",

    "inventory.footer.page": "Page {page}/{total}",

    "inventory.button.prev": "Previous",
    "inventory.button.next": "Next",
    "inventory.button.to_weapons": "Weapons",
    "inventory.button.to_cards": "Cards",

    "inventory.msg.first_page": "You are already on the first page.",
    "inventory.msg.last_page": "You are already on the last page.",

    "inventory.error.not_registered": "You are not registered yet. Please use `/register` first.",

    "inventory.field.id": "ID",
    "inventory.field.tier": "Tier",
    "inventory.field.grade": "Grade",
    "inventory.field.tanker": "Tanker",
    "inventory.field.quantity": "Quantity",
    "inventory.field.quantity_weapon": "Quantity",

    "inventory.card.locked_marker": " (Locked)",

    "inventory.buff.damage": "Damage",
    "inventory.buff.health": "HP",
    "inventory.buff.armor": "Armor",
    "inventory.buff.crit_rate": "Crit Rate",
    "inventory.buff.speed": "Evasion",
    "inventory.buff.chakra": "Chakra",



    "levelupweapon.command_desc": "Upgrade your weapon (increase by 1 level)",
    "levelupweapon.param.weapon_id": "Weapon ID you want to upgrade (check /inventory)",

    "levelupweapon.error.not_registered": "You are not registered yet. Please use /register first.",
    "levelupweapon.error.not_owner": "You do not own a weapon with ID `{weapon_id}`. Please check /inventory.",
    "levelupweapon.error.invalid_data": "Invalid weapon data. Please try again later.",

    "levelupweapon.error.not_highest_level": (
        "You can only upgrade from your highest-level weapon.\n"
        "Weapon ID `{weapon_id}` is level {current_level}, "
        "but your highest weapon level is {highest_level}."
    ),

    "levelupweapon.error.equipped": (
        "Weapon **{weapon_name}** (ID `{weapon_id}`) "
        "is currently equipped. Please unequip it using /unequipweapon before upgrading."
    ),

    "levelupweapon.error.not_enough_materials": (
        "You don't have enough level 1 copies of **{weapon_name}** to upgrade.\n"
        "Required: {required}, you have: {current}."
    ),

    "levelupweapon.success": (
        "Upgrade successful! Weapon **{weapon_name}** "
        "(ID `{new_weapon_id}`) has been upgraded from level {from_level} to level {to_level}."
    ),

    "levelupweapon.error.generic": "Something went wrong. Please try again later.",



    "levelupcard.command_desc": "Upgrade your card (increase by 1 level)",
    "levelupcard.param.card_id": "Card ID you want to upgrade (check /inventory)",

    "levelupcard.error.not_registered": "You are not registered yet. Please use /register first.",
    "levelupcard.error.not_owner": "You do not own a card with ID `{card_id}`. Please check /inventory.",

    "levelupcard.error.max_level": "The maximum card level is 50. This card is currently level {current_level}.",
    "levelupcard.error.invalid_data": "Invalid card data. Please try again later.",

    "levelupcard.error.not_highest_level": (
        "You can only upgrade from your highest-level card.\n"
        "Card ID `{card_id}` is level {current_level}, "
        "but your highest card level is {highest_level}."
    ),

    "levelupcard.error.equipped": (
        "Card **{card_name}** (ID `{card_id}`) is currently equipped as your main card. "
        "Please set another card using /setcard before upgrading."
    ),

    "levelupcard.error.not_enough_materials": (
        "You don't have enough level 1 copies of **{card_name}** to upgrade.\n"
        "Required: {required}, you have: {current}."
    ),

    "levelupcard.success": (
        "Upgrade successful! Card **{card_name}** "
        "(ID `{new_card_id}`) has been upgraded from level {from_level} to level {to_level}."
    ),

    "levelupcard.error.generic": "Something went wrong. Please try again later.",




    "lockcard.command_desc": "Lock all cards of the same type. Locked cards cannot be sold",
    "lockcard.param.card_id": "Card ID you want to lock (check /inventory)",

    "lockcard.error.not_registered": "You are not registered yet. Please use /register first.",
    "lockcard.error.not_owner": "You do not own a card with ID `{card_id}`.",
    "lockcard.error.not_found_same_type": "Cannot find other cards of the same type to lock.",

    "lockcard.success": (
        "Locked **all your `{card_name}` cards** "
        "(including all levels and materials)."
    ),

    "lockcard.error.generic": "Something went wrong while locking cards. Please try again later.",
}