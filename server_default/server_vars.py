from lib.dataclasses import LoyaltyLevel

money_chat_id = -0  # id чата, куда Человек будет кидать деньги
dot_ch_id = -0  # id канала, на который нужно быть подписанным
dot_ch_chat_id = -0  # id чата канала

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
]

money_drop_period_minutes = 1440
money_drop_drops = 5
money_drop_amount = 0.00777
