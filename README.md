

# Tree of Thoughts (ToT) 文本任务复现

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)

本仓库复现了ICLR 2023论文《Tree of Thoughts: Deliberate Problem Solving with Large Language Models》的文本生成任务，实现了基于思维树的推理框架。

## 📌 核心特性
- 支持文本生成任务：
  - 创意写作（Creative Writing）
  - 文本补全（Text Completion）
  - 诗歌生成（Poetry Generation）
- 实现搜索算法：
  - 广度优先搜索（BFS）



## 🚀 快速开始

### 环境要求
```bash
Python >= 3.9
```

### 安装依赖
```bash
git clone https://github.com/invinciby/ToT_llm.git
cd ToT_llm
conda create -n tot python=3.9
conda activate tot
pip install -r requirements.txt
```

### 基础使用示例
1. 修改config/model.py 这里使用的是gemini api 目前免费，在这个👈文档里将api替换上即可。
2. 修改run.py中的配置

    ```python
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
    ```

3. 运行run.py即可，【注意：用gemini api时，需要科学上网，否则会报错】

## 📊 复现结果
### 性能指标（在测试集上的表现）

待测中...


