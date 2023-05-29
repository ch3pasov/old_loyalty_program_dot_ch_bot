# from lib.queue_lib import create_queue
from random import choice, random, randrange
from lib.queue_cabinet_generate_lib import create_queue_and_cabinet_delta
from global_vars import print, queue_md_params


def choice_queue_md_type(queue_md=queue_md_params):
    types = queue_md['types']
    return choice(sum([[key]*types[key]['freq'] for key in types], []))


def tricky_random_range(param_range, degree):
    return param_range['min']+(((param_range['max']-param_range['min'])**(1/degree))*random())**degree


def trim_to_ten_thousandths(number):
    return int(number*10000)/10000


def generate_queue_params_by_type(queue_md_type, queue_md=queue_md_params):
    queue_lock_delta_minutes = queue_md['queue_lock_delta_minutes']
    queue_delete_delta_minutes = queue_md['queue_delete_delta_minutes']

    queue_md_type_params = queue_md['types'][queue_md_type]

    cabinet_work_start_delay_minutes = queue_md_type_params['cabinet']['cabinet_work_start_delay_minutes']
    reward_max_sum = queue_md_type_params['cabinet']['cabinet_reward_max_sum']
    queue_delay_minutes_range = queue_md_type_params['queue']['delay_minutes']
    queue_delay_minutes = randrange(queue_delay_minutes_range['min'], queue_delay_minutes_range['max']+1)

    cabinet_params = queue_md_type_params['cabinet']
    cabinet_delay_minutes_range = cabinet_params['delay_minutes']
    cabinet_delay_minutes = randrange(cabinet_delay_minutes_range['min'], cabinet_delay_minutes_range['max']+1)

    work_delta_minutes_range = cabinet_params['work_delta_minutes']
    work_delta_minutes = randrange(work_delta_minutes_range['min'], work_delta_minutes_range['max']+1)

    reward_per_one_range = cabinet_params['reward_per_one']
    reward_per_one = trim_to_ten_thousandths(tricky_random_range(reward_per_one_range, 4))
    return {
        'cabinet_work_start_delay_minutes': cabinet_work_start_delay_minutes,
        'reward_max_sum': reward_max_sum,
        'queue_delay_minutes': queue_delay_minutes,
        'cabinet_delay_minutes': cabinet_delay_minutes,
        'work_delta_minutes': work_delta_minutes,
        'queue_lock_delta_minutes': queue_lock_delta_minutes,
        'queue_delete_delta_minutes': queue_delete_delta_minutes,
        'reward_per_one': reward_per_one
    }


def generate_queue_params(queue_md=queue_md_params):
    return generate_queue_params_by_type(choice_queue_md_type(queue_md), queue_md)


def queue_money_drop():
    print("QUEUE MONEY DROP")
    q_md_params = generate_queue_params(queue_md_params)
    return create_queue_and_cabinet_delta(**q_md_params)
