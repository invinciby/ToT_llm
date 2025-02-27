import os
import json
import argparse
from email.policy import default
from sympy import false # type: ignore

from task.get_task import  get_task
from methods.bfs import solve, naive_solve
# solve : 主求解函数，执行生成、评估和选择步骤，最终返回最佳输出。
# naive_solve : 一个简单的求解函数，直接生成样本并返回
from config.model import gpt_usage

def run(args):
    # 获取任务
    task = get_task(args.task)
    # 初始化日志、平均准确率和任意准确率
    logs, cnt_avg, cnt_any = [], 0, 0
    # 判断是否为简单运行
    if args.naive_run:
        # 简单运行时，文件名为：./logs/{args.task}/{args.backend}_{args.temperature}_naive_{args.prompt_sample}_sample_{args.n_generate_sample}_start{args.task_start_index}_end{args.task_end_index}.json
        file = f'./logs/{args.task}/{args.backend}_{args.temperature}_naive_{args.prompt_sample}_sample_{args.n_generate_sample}_start{args.task_start_index}_end{args.task_end_index}.json'
    else:
        # 非简单运行时，文件名为：./logs/{args.task}/{args.backend}_{args.temperature}_{args.method_generate}{args.n_generate_sample}_{args.method_evaluate}{args.n_evaluate_sample}_{args.method_select}{args.n_select_sample}_start{args.task_start_index}_end{args.task_end_index}.json
        file = f'./logs/{args.task}/{args.backend}_{args.temperature}_{args.method_generate}{args.n_generate_sample}_{args.method_evaluate}{args.n_evaluate_sample}_{args.method_select}{args.n_select_sample}_start{args.task_start_index}_end{args.task_end_index}.json'
    # 创建文件目录
    os.makedirs(os.path.dirname(file), exist_ok=True)

    # 遍历任务索引
    for i in range(args.task_start_index, args.task_end_index):
        # solve
        if args.naive_run:
            ys, info = naive_solve(args, task, i) 
        else:
            ys, info = solve(args, task, i)

        # log
        infos = [task.test_output(i, y) for y in ys]
        info.update({'idx': i, 'ys': ys, 'infos': infos, 'usage_so_far': gpt_usage(args.backend)})
        logs.append(info)
        with open(file, 'w') as f:
            json.dump(logs, f, indent=4)
        
        # log main metric
        accs = [info['r'] for info in infos]
        cnt_avg += sum(accs) / len(accs)
        cnt_any += any(accs)
        print(i, 'sum(accs)', sum(accs), 'cnt_avg', cnt_avg, 'cnt_any', cnt_any, '\n')
    
    n = args.task_end_index - args.task_start_index
    print(cnt_avg / n, cnt_any / n)
    print('usage_so_far', gpt_usage(args.backend))

def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument('--backend', type=str, choices=['gemini'], default='gemini')
    args.add_argument('--temperature', type=float, default=0.7)
    args.add_argument('--task', type=str, required=false, choices=['game24', 'text'], default='text')

    args.add_argument('--task_start_index', type=int, default=0)
    args.add_argument('--task_end_index', type=int, default=1)
    args.add_argument('--naive_run', action='store_true')
    
    # 添加一个名为prompt_sample的参数，类型为字符串，可选值为standard和cot，默认值为standard
    args.add_argument('--prompt_sample', type=str, choices=['standard', 'cot'],default='standard')  # only used when method_generate = sample, or naive_run
    # 添加一个名为method_generate的参数，类型为字符串，可选值为sample和propose，默认值为sample
    args.add_argument('--method_generate', type=str, choices=['sample', 'propose'], default='sample')
    # 添加一个名为method_evaluate的参数，类型为字符串，可选值为value和vote，默认值为vote
    args.add_argument('--method_evaluate', type=str, choices=['value', 'vote'], default='vote')
    # 添加一个名为method_select的参数，类型为字符串，可选值为sample和greedy，默认值为greedy
    args.add_argument('--method_select', type=str, choices=['sample', 'greedy'], default='greedy')
    # 添加一个名为n_generate_sample的参数，类型为整数，默认值为2
    args.add_argument('--n_generate_sample', type=int, default=2)  # only thing needed if naive_run
    # 添加一个名为n_evaluate_sample的参数，类型为整数，默认值为3
    args.add_argument('--n_evaluate_sample', type=int, default=1)
    # 添加一个名为n_select_sample的参数，类型为整数，默认值为1
    args.add_argument('--n_select_sample', type=int, default=1)

    # 解析参数
    args = args.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    print(args)
    run(args)
    
    # python run.py --n_generate_sample 100 