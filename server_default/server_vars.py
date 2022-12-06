from lib.dataclasses import LoyaltyLevel

money_chat_id = -0  # id чата, куда Человек будет кидать деньги
dot_ch_id = -0  # id канала, на который нужно быть подписанным
dot_ch_chat_id = -0  # id чата канала

bot_username = "a"  # юзернейм бота
creator_username = "a"  # юзернейм меня, чтобы призывать в случае экстренного выключения
bot_debug_message_id = 0  # id сообщения, куда робот пишет, что начал\закончил свою работу
money_drop_message_id = 0  # id сообщения для манидропов. Это id внутри чата канала
# то есть # t.me/c/{dot_ch_chat_id}/{chat_message_id}

# Ой вот тут вы умрёте доставать этот id, для каждого робота он разный. Удачи!
money_animation = "a"
unsubscribed_animation = "a"

# программа лояльности
loyalty_program = [
    LoyaltyLevel(level=0, days=0, reward=0.0001, congrats_text='🦍🦍🦍', congrats_link='https://youtu.be/-Kg9i0Pt_oA'),
    LoyaltyLevel(level=1, days=1, reward=0.0002, congrats_text='🥳😺🪩', congrats_link='https://youtu.be/uITwtd92r6Y?t=47'),
    LoyaltyLevel(level=2, days=2, reward=0.0004, congrats_text='🛁🧽💧', congrats_link='https://youtu.be/3K-aggRMR8I'),
    LoyaltyLevel(level=3, days=3, reward=0.0008, congrats_text='😳🪿😳', congrats_link='https://youtu.be/d_8bl-RxRyY'),
    LoyaltyLevel(level=4, days=4, reward=0.0016, congrats_text='🔄🐀🛳', congrats_link='https://youtu.be/PEUIqiBAaQw?t=21'),
    LoyaltyLevel(level=5, days=5, reward=0.0032, congrats_text='🔂🐟🔂', congrats_link='https://youtu.be/poa_QBvtIBA'),
    LoyaltyLevel(level=6, days=6, reward=0.0064, congrats_text='🥋🦆🔁', congrats_link='https://youtu.be/Bat09kKAle4'),
    LoyaltyLevel(level=7, days=7, reward=0.01, congrats_text='🦀🦀🦀', congrats_link='https://youtu.be/LDU_Txk06tM?t=73'),
    LoyaltyLevel(level=8, days=14, reward=0.01, congrats_text='😳🧌😳', congrats_link='https://youtu.be/WPywfWMPgt4?t=28'),
    LoyaltyLevel(level=9, days=21, reward=0.01, congrats_text='🧌🧌🧌🧌', congrats_link='https://youtu.be/xNoSi7acNgc'),
    LoyaltyLevel(level=10, days=28, reward=0.05, congrats_text='🧌🧌🧌🧌🧌🧌🧌🧌', congrats_link='https://youtu.be/0PiqqbyQRoo?t=14'),
    LoyaltyLevel(level=11, days=35, reward=0.01, congrats_text='🤪🤪', congrats_link='https://youtu.be/kGGoeDrjL5g'),
    LoyaltyLevel(level=12, days=42, reward=0.01, congrats_text='🚬🤡', congrats_link='https://youtu.be/o3bxfyq1wrk'),
    LoyaltyLevel(level=13, days=49, reward=0.01, congrats_text='👨‍🎨🤡', congrats_link='https://youtu.be/eMbNihx1BNk'),
    LoyaltyLevel(level=14, days=50, reward=0.0128, congrats_text='🐶✂️', congrats_link='https://youtu.be/z2xgSgAVQ-E'),
    LoyaltyLevel(level=15, days=60, reward=0.0256, congrats_text='🐹🍼', congrats_link='https://youtu.be/UlM-DiHbJXE'),
    LoyaltyLevel(level=16, days=75, reward=0.0256, congrats_text='🐷', congrats_link='https://youtu.be/taOw0intSWk'),
    LoyaltyLevel(level=17, days=90, reward=0.0512, congrats_text='👠⚽️', congrats_link='https://youtu.be/eHe3WUdRnaE?t=126'),
    LoyaltyLevel(level=18, days=100, reward=0.0512, congrats_text='#🇷🇺', congrats_link='https://youtu.be/XWaN_geKpj4?t=2'),
    LoyaltyLevel(level=19, days=200, reward=0.1024, congrats_text='2️⃣0️⃣1️⃣8️⃣', congrats_link='https://youtu.be/TIjb8yR8f9Q'),
    LoyaltyLevel(level=20, days=365, reward=0.2048, congrats_text='👶🏻👦🏻👨🏻🧔🏻‍♂️👴🏻💀', congrats_link='https://youtu.be/EFL4rgxYsJE'),
]

money_drop_period_minutes = 1440
money_drop_drops = 5
money_drop_amount = 0.00777
