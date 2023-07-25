# from lib.queue_lib import create_queue
from random import choice, random, randrange
from lib.queue_cabinet_generate_lib import create_queue_and_cabinet_delta
from global_vars import print, queue_md_params
import json


def choice_queue_md_type(queue_md=queue_md_params):
    types = queue_md['types']
    return choice(sum([[key]*types[key]['freq'] for key in types], []))


def tricky_random_range(param_range_list, degree):
    return [
        param_range_list['min'][i] +
        (((param_range_list['max'][i]-param_range_list['min'][i])**(1/degree))*random())**degree
        for i in range(len(param_range_list['min']))
    ]


def trim_to_ten_thousandths(numbers_list):
    return [int(number*10000)/10000 for number in numbers_list]


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
    reward_per_one = trim_to_ten_thousandths(tricky_random_range(reward_per_one_range, 1))
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


def queue_money_drop_by_type(type_name: str):
    '''Создать очередь-манидроп определённого типа'''
    # для админки
    type_name = str(type_name)
    q_md_params = generate_queue_params_by_type(type_name, queue_md_params)
    print("QUEUE MONEY DROP")
    return create_queue_and_cabinet_delta(**q_md_params)


def queue_money_drop():
    '''Создать очередь-манидроп случайного типа'''
    type_name = choice_queue_md_type(queue_md_params)
    return queue_money_drop_by_type(type_name, queue_md=queue_md_params)


def get_qmd_params_type_keys():
    '''показать ключи queue_md_params'''
    return '\n'.join([f"`{key}`" for key in queue_md_params['types'].keys()])


def get_qmd_params_type(qmd_type):
    '''показать настройки queue_md_params по типу'''
    return f"```{json.dumps(queue_md_params['types'][qmd_type], indent=4)}```"
