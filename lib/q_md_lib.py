# from lib.queue_lib import create_queue
from random import choice, random, randrange
from server.server_vars import queue_md


def choice_queue_md_type(queue_md=queue_md):
    types = queue_md['types']
    return choice(sum([[key]*types[key]['freq'] for key in types], []))


def tricky_random_range(param_range, degree):
    return param_range['min']+(((param_range['max']-param_range['min'])**(1/degree))*random())**degree


def trim_to_ten_thousandths(number):
    return int(number*10000)/10000


def generate_queue_params_by_type(queue_md_type, queue_md=queue_md):
    period_minutes = queue_md['period_minutes']
    cabinet_work_start_delay_minutes = queue_md['cabinet_work_start_delay_minutes']
    cabinet_reward_max_sum = queue_md['cabinet_reward_max_sum']

    queue_md_type_params = queue_md['types'][queue_md_type]

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
        'period_minutes': period_minutes,
        'cabinet_work_start_delay_minutes': cabinet_work_start_delay_minutes,
        'cabinet_reward_max_sum': cabinet_reward_max_sum,
        'queue_delay_minutes': queue_delay_minutes,
        'cabinet_delay_minutes': cabinet_delay_minutes,
        'work_delta_minutes': work_delta_minutes,
        'reward_per_one': reward_per_one
    }


def generate_queue_params(queue_md=queue_md):
    return generate_queue_params_by_type(choice_queue_md_type(queue_md), queue_md)


print(generate_queue_params())
