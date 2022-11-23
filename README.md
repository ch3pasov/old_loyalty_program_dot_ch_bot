# dot_ch_bot

Мой бот 🤡

Чтобы его завести, надо:

1. Установить зависимости.
```
pip3 install pyrogram
pip3 install -U tgcrypto
```

2. Получить Telegarm API key из https://my.telegram.org/apps. Вписать опции в server/secret.py:
   - Вписать App api_id в app_id
   - Вписать App api_hash в app_api_hash

3. Завести папку server, если её нет:
```
cp -r server_default server
```

3. Вписать опции в server/server_vars.py:
   - Завести суперсекретный чат для создания денежных чеков. Вписать его число-id (или строчку-username) в money_chat_id
   - Завести канал, на который нужно всем подписаться. Вписать его число-id (или строчку-username) в dot_ch_id
   - Вписать в money_animation id анимации при выдаче денег (это нетривиальная задача)
   — Вписать money_drop_message_id id сообщения поста с манидропом, куда робот будет сбрасывать деньги
   - (опционально) поменять сетку уровней и бонусов за них. Напомню, что минимально возможная сумма для создания чека в @wallet — 0,0001
   — (опционально) поменять правила манидропа.

4. Завести аккаунт человека с подключенным @wallet-кошельком, который будет денежной прослойкой.

5. Завести аккаунт робота, который будет главным интерфейсом, через @botfather. Робота нужно подписать на канал и на группу с минимальными правами админа.

6. Запустить main.py. Для первого логина pyrogram попросит два раза авторизоваться.
   - Сначала нужно залогиниться в робота: необходимо вписать token робота, выданный @botfather
   - Затем нужно залогиниться в человека: необходимо ввести телефон\код\пароль\всё_что_pyrogram_попросит

7. ???

8. PROFIT!!!
