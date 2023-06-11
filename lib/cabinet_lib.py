from global_vars import active_queues
from lib.queue_lib import update_queue
import server.server_vars
from queue_program.queue_schedule import set_cabinet_state_scheduler_job


async def create_cabinet(
    queue_id,
    start,  # timestamp начала работы кабинета
    end,  # timestamp конца работы кабинета
    lock,  # timestamp лока очереди (нельзя зайти)
    delete,  # timestamp удаления очереди (архив)
    reward_per_one=0.0001,
    reward_max_sum=0.01,
    cabinet_delay_minutes=5
):
    queue = active_queues[queue_id]

    queue['cabinet'] = {
        "rules": {
            "work": {
                "start": start,
                "finish": end,
                "lock": lock,
                "delete": delete,
                "delay_minutes": cabinet_delay_minutes
            },
            "reward": {
                "per_one": reward_per_one,
                "max_sum": reward_max_sum
            }
        },
        "state": {
            "cabinet_status": -1,
            "inside": None,
            "winners": {
                "players": {},
                "sum": 0
            }
        }
    }

    cabinet = queue['cabinet']
    await set_cabinet_state_scheduler_job(queue_id, cabinet, verbose=True)

    await update_queue(queue_id)

    return f"Очередь {queue_id} создана! https://t.me/c/{(-server.server_vars.dot_ch_id)%10**10}/{queue_id}"
