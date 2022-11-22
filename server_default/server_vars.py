from lib.dataclasses import LoyalityLevel

money_chat_id = -0  # id чата, куда Человек будет кидать деньги
dot_ch_id = -0  # id канала, на который нужно быть подписанным
# dot_ch_chat_id = -1  # id чата канала

# Ой вот тут вы умрёте доставать этот id, для каждого робота он разный. Удачи!
money_animation = "a"
unsubscribed_animation = "a"

# программа лояльности
loyality_programm = [
    LoyalityLevel(level=0, days=0, reward=0.0001, congrats_text='🦍🦍🦍', congrats_link='https://youtu.be/-Kg9i0Pt_oA'),
    LoyalityLevel(level=1, days=1, reward=0.0002, congrats_text='🥳😺🪩', congrats_link='https://youtu.be/uITwtd92r6Y?t=47'),
    LoyalityLevel(level=2, days=2, reward=0.0004, congrats_text='🛁🧽💧', congrats_link='https://youtu.be/3K-aggRMR8I'),
    LoyalityLevel(level=3, days=3, reward=0.0008, congrats_text='😳🪿😳', congrats_link='https://youtu.be/d_8bl-RxRyY'),
    LoyalityLevel(level=4, days=4, reward=0.0016, congrats_text='🔄🐀🛳', congrats_link='https://youtu.be/PEUIqiBAaQw?t=21'),
    LoyalityLevel(level=5, days=5, reward=0.0032, congrats_text='🔂🐟🔂', congrats_link='https://youtu.be/poa_QBvtIBA'),
    LoyalityLevel(level=6, days=6, reward=0.0064, congrats_text='🥋🦆🔁', congrats_link='https://youtu.be/Bat09kKAle4'),
    LoyalityLevel(level=7, days=7, reward=0.01, congrats_text='🦀🦀🦀', congrats_link='https://youtu.be/LDU_Txk06tM?t=73'),
    LoyalityLevel(level=8, days=14, reward=0.01, congrats_text='😳🧌😳', congrats_link='https://youtu.be/WPywfWMPgt4?t=28'),
    LoyalityLevel(level=9, days=21, reward=0.01, congrats_text='🧌🧌🧌🧌', congrats_link='https://youtu.be/xNoSi7acNgc'),
    LoyalityLevel(level=10, days=28, reward=0.05, congrats_text='🧌🧌🧌🧌🧌🧌🧌🧌', congrats_link='https://youtu.be/0PiqqbyQRoo?t=14'),
]