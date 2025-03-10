from config.model import gpt
import itertools
import numpy as np
from functools import partial
import re

def get_value(task, x, y, n_eval_sample, cache_value = True):
    value_prompt = task.value_prompt_wrap(x, y)
    if cache_value and value_prompt in task.value_cache:
        return task.value_cache[value_prompt]
    value_outputs = gpt(value_prompt, n=n_eval_sample, stop=None)
    # print(f"----------------value_outputs: {value_outputs}")
    value = task.value_outputs_unwrap(x, y, value_outputs)
    if cache_value:
        task.value_cache[value_prompt] = value
    return value

def get_values(task, x, ys, n_evaluate_sample, cache_value=True):
    values = []
    local_value_cache = {}
    for y in ys:  # each partial output
        if y in local_value_cache:  # avoid duplicate candidates
            value = 0
        else:    
            value = get_value(task, x, y, n_evaluate_sample, cache_value=cache_value)
            local_value_cache[y] = value
        values.append(value)
    return values

def get_votes(task, x, ys, n_evaluate_sample):
    vote_prompt = task.vote_prompt_wrap(x, ys)
    vote_outputs = gpt(vote_prompt, n=n_evaluate_sample, stop=None)
    # print(f"----------------vote_outputs: {vote_outputs}")
    values = task.vote_outputs_unwrap(vote_outputs, len(ys))
    
    return values

def get_proposals(task, x, y): 
    propose_prompt = task.propose_prompt_wrap(x, y)
    proposals = gpt(propose_prompt, n=1, stop=None)[0].split('\n')
    return [y + _ + '\n' for _ in proposals]

def get_samples(task, x, y, n_generate_sample, prompt_sample, stop):
    # print(f"----------------get_samples: {y}")
    if prompt_sample == 'standard':
        prompt = task.standard_prompt_wrap(x,y)
    elif prompt_sample == 'cot':
        prompt = task.cot_prompt_wrap(x, y)
    else:
        raise ValueError(f'prompt_sample {prompt_sample} not recognized')
    samples = gpt(prompt, n=n_generate_sample, stop=stop)
    return [y + _ for _ in samples]

def detal_sentence(y, task):
    if y == ['']:
        return y
    # print(f"----------------detal_sentence: {y}")
    if task == 'text':
        return [s.strip() for s in y[0].split('\n\n') if s]
    else:
        return y

def solve(args, task, idx, to_print=True):
    # 定义一个全局变量gpt
    global gpt
    # 将gpt函数的model参数设置为args.backend，temperature参数设置为args.temperature
    gpt = partial(gpt, model=args.backend, temperature=args.temperature)
    # 打印gpt函数
    print(gpt)
    # 获取任务输入
    print(f"idx: {idx}")
    x = task.get_input(idx)  # input
    print(f"x get! is : {x}")
    # 初始化当前输出候选
    ys = ['']  # current output candidates
    # 初始化信息列表
    infos = []
    # 循环执行任务步骤
    for step in range(task.steps):
        ys = detal_sentence(ys, args.task)
        # generation
        if args.method_generate == 'sample':
            new_ys = [get_samples(task, x, y, args.n_generate_sample, prompt_sample=args.prompt_sample, stop=task.stops[step]) for y in ys]
        elif args.method_generate == 'propose':
            new_ys = [get_proposals(task, x, y) for y in ys]
        new_ys = list(itertools.chain(*new_ys))
        ids = list(range(len(new_ys)))
        new_ys =detal_sentence(new_ys,args.task)
        # print(f"----------------new_ys: {new_ys}")
        # evaluation
        if args.method_evaluate == 'vote':
            values = get_votes(task, x, new_ys, args.n_evaluate_sample)
        
        elif args.method_evaluate == 'value':
            values = get_values(task, x, new_ys, args.n_evaluate_sample)

        # print(f"----------------values: {values}")
        # selection
        # 如果选择的方法是sample
        if args.method_select == 'sample':
            # 将values转换为概率分布
            ps = np.array(values) / sum(values)
            # 根据概率分布选择n_select_sample个id
            select_ids = np.random.choice(ids, size=args.n_select_sample, p=ps).tolist()
        # 如果选择的方法是greedy
        elif args.method_select == 'greedy':
            # 根据values的值，从大到小排序id
            select_ids = sorted(ids, key=lambda x: values[x], reverse=True)[:args.n_select_sample]
            # print(f"select_ids: {select_ids}")
        # 根据选择的id，从new_ys中取出对应的值
        select_new_ys = [new_ys[select_id] for select_id in select_ids]
        
        # print(f"select_new_ys_id: {len(select_new_ys)}")
        # log
        # if to_print: 
            # sorted_new_ys, sorted_values = zip(*sorted(zip(new_ys, values), key=lambda x: x[1], reverse=True))
            # print(f'-- new_ys --: {sorted_new_ys}\n-- sol values --: {sorted_values}\n-- choices --: {select_new_ys}\n')
        
        infos.append({'step': step, 'x': x, 'ys': ys, 'new_ys': new_ys, 'values': values, 'select_new_ys': select_new_ys})
        ys = select_new_ys
    
    if to_print: 
        # print(ys)
        pass
    return ys, {'steps': infos}

def naive_solve(args, task, idx, to_print=True):
    # 定义一个全局变量gpt
    global gpt
    # 将gpt函数的model参数设置为args.backend，temperature参数设置为args.temperature
    gpt = partial(gpt, model=args.backend, temperature=args.temperature)
    # 打印gpt函数
    print(gpt)
    # 获取任务输入
    x = task.get_input(idx)  # input
    # 获取样本
    ys = get_samples(task, x, '', args.n_generate_sample, args.prompt_sample, stop=None)
    # 返回样本和空字典
    return ys, {}