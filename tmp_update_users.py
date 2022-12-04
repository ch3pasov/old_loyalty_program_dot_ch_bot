import json

with open('server/users.json') as f:
    old_users = json.load(f)


import copy


new_users = copy.deepcopy(old_users)
for user in new_users:
    if "loyality_programm" in new_users[user]:
        new_users[user]['loyalty_program'] = new_users[user].pop('loyality_programm')
for user in new_users:
    new_users[user]['loyalty_program'].setdefault('referer_id', None)
    # new_users[user].setdefault('context', None)

print('''
with open('server/users.json', 'w', encoding='utf-8') as f:
    json.dump(users, f, ensure_ascii=False, indent=4)
''')
