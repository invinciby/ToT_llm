import re
import os
import sympy
import pandas as pd
from prompts.game24 import *
from task.base import Task, DATA_PATH

# 定义一个函数，用于获取字符串y中的left留下的数字
# eg. 13 - 10 = 3 (left: 3 4 9)
# ans =  3 4 9
def get_current_numbers(y: str) -> str:
    # 去除字符串y中的空格，并按行分割
    last_line = y.strip().split('\n')[-1]
    # 将最后一行按'left: '分割，并取最后一个元素
    return last_line.split('left: ')[-1].split(')')[0]

class Game24(Task):
    # 初始化Game24类，读取24.csv文件中的数据
    def __init__(self, file='24.csv'):
        super().__init__()
        # 获取文件路径
        path = os.path.join(DATA_PATH, '24', file)
        # 读取csv文件中的数据
        self.data = list(pd.read_csv(path)['Puzzles'])
        # 初始化value_cache
        self.value_cache = {}
        # 初始化steps
        self.steps = 4
        # 初始化stops
        self.stops = ['\n'] * 4

    # 返回数据长度
    def __len__(self) -> int:
        return len(self.data)
    
    # 获取输入数据
    def get_input(self, idx: int) -> str:
        return self.data[idx]
    
    # 测试输出数据
    def test_output(self, idx: int, output: str):
        # 获取表达式
        expression = output.strip().split('\n')[-1].lower().replace('answer: ', '').split('=')[0]
        # 获取数字
        numbers = re.findall(r'\d+', expression)
        problem_numbers = re.findall(r'\d+', self.data[idx])
        # 如果数字不匹配，返回0
        if sorted(numbers) != sorted(problem_numbers):
            return {'r': 0}
        try:
            # 简化表达式
            # print(sympy.simplify(expression))
            # 如果表达式等于24，返回1，否则返回0
            return {'r': int(sympy.simplify(expression) == 24)}
        except Exception as e:
            # 打印异常
            # print(e)
            return {'r': 0}
        
    # 标准提示包装
    @staticmethod
    def standard_prompt_wrap(x: str, y:str='') -> str:
        return standard_prompt.format(input=x) + y

    # cot提示包装
    @staticmethod
    def cot_prompt_wrap(x: str, y:str='') -> str:
        return cot_prompt.format(input=x) + y
    
    # 提议提示包装
    @staticmethod
    def propose_prompt_wrap(x: str, y: str='') -> str:
        # 获取当前数字
        current_numbers = get_current_numbers(y if y else x)
        # 如果当前数字等于24，返回cot提示
        if current_numbers == '24':
            prompt = cot_prompt.format(input=x) + 'Steps:' + y
            # print([prompt])
        else:
            prompt = propose_prompt.format(input=current_numbers)
        return prompt
    
    # value提示包装
    @staticmethod
    def value_prompt_wrap(x: str, y: str) -> str:
        # 获取最后一行
        last_line = y.strip().split('\n')[-1]
        if 'left: ' not in last_line:  # last step
            ans = last_line.lower().replace('answer: ', '')
            # print([value_last_step_prompt.format(input=x, answer=ans)])
            return value_last_step_prompt.format(input=x, answer=ans)
        current_numbers = get_current_numbers(y)
        return value_prompt.format(input=current_numbers)
    
    @staticmethod
    def value_outputs_unwrap(x: str, y: str, value_outputs: list) -> float:
        if len(y.strip().split('\n')) == 4 and 'answer' not in y.lower():
            return 0
        value_names = [_.split('\n')[-1] for _ in value_outputs]
        value_map = {'impossible': 0.001, 'likely': 1, 'sure': 20}  # TODO: ad hoc
        value = sum(value * value_names.count(name) for name, value in value_map.items())
        return value