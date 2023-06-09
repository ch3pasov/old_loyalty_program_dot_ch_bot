import server.server_vars
from global_vars import active_queues
from lib.queue_lib import kick_user_from_queue, update_queue
from lib.cabinet_actions_lib import kick_user_from_cabinet


def queue_delete(queue_id: str):
    """Удалить очередь — пост останется в архиве, но просчитываться не будет."""
    # для админки
    queue_id = str(queue_id)
    # kick all users
    queue = active_queues[queue_id]
    for user_id in queue['queue_order']:
        kick_user_from_queue(user_id)
    cabinet = queue['cabinet']
    if cabinet:
        inside_user_id = cabinet['state']['inside']
        if inside_user_id:
            kick_user_from_cabinet(inside_user_id, queue_id)
    # update queue
    queue_comments = queue['show']['comments']
    queue_comments['cnt'] = str(queue_comments['cnt'])+'?'
    queue_comments['fingerprint'] = '❓'
    update_queue(queue_id, archive=True)
    # del queue
    active_queues.pop(queue_id)
    return f"Очередь https://t.me/c/{(-server.server_vars.dot_ch_id)%10**10}/{queue_id} удалена!"
