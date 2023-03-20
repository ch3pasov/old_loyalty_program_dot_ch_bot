from lib.queue_lib import create_queue
from lib.cabinet_lib import create_cabinet
from lib.useful_lib import datetime_to_timestamp, now_plus_n_minutes


def create_queue_and_cabinet_raw(
    queue_delay_minutes,
    cabinet_delay_minutes,
    cabinet_start,
    cabinet_end,
    reward_per_one,
    reward_max_sum
):
    queue_id = create_queue(queue_delay_minutes)
    create_cabinet(
        queue_id,
        cabinet_start,
        cabinet_end,
        reward_per_one,
        reward_max_sum,
        cabinet_delay_minutes
    )


def create_queue_and_cabinet_delta(
    cabinet_work_start_delay_minutes,
    queue_delay_minutes,
    cabinet_delay_minutes,
    work_delta_minutes,
    reward_per_one,
    reward_max_sum
):
    cabinet_start = datetime_to_timestamp(now_plus_n_minutes(cabinet_work_start_delay_minutes))
    cabinet_end = datetime_to_timestamp(now_plus_n_minutes(cabinet_work_start_delay_minutes+work_delta_minutes))

    create_queue_and_cabinet_raw(
        queue_delay_minutes,
        cabinet_delay_minutes,
        cabinet_start,
        cabinet_end,
        reward_per_one,
        reward_max_sum
    )
