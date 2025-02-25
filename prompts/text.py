standard_prompt = '''
Write a coherent passage of 4 short paragraphs. The end sentence of each paragraph must be: {input}
'''

# 写一段连贯的文字，共 4 小段。 每段的结尾句必须是

cot_prompt = '''
Write a coherent passage of 4 short paragraphs. The end sentence of each paragraph must be: {input}

Make a plan then write. Your output should be of the following format:

Plan:
Your plan here.

Passage:
Your passage here.
'''
# 写一段连贯的文字，共 4 小段。 每段的结尾句必须是 {输入｝
# 制定计划，然后写作。 您的输出应采用以下格式：
# 计划：
# 您的计划在此。
# 段落：
# 此处为您的段落。

vote_prompt = '''Given an instruction and several choices, decide which choice is most promising. Analyze each choice in detail, then conclude in the last line "The best choice is {s}", where s the integer id of the choice.
'''
# 给你一条指令和几个选择，请判断哪个选择最有前途。 详细分析每个选择，然后在最后一行得出结论 "最佳选择是 {s}"，其中 s 是选择的整数 ID。


compare_prompt = '''Briefly analyze the coherency of the following two passages. Conclude in the last line "The more coherent passage is 1", "The more coherent passage is 2", or "The two passages are similarly coherent".
'''
# 简要分析下面两个段落的连贯性。 在最后一行得出结论："更连贯的段落是 1"、"更连贯的段落是 2 "或 "这两个段落同样连贯"。



score_prompt = '''Analyze the following passage, then at the last line conclude "Thus the coherency score is {s}", where s is an integer from 1 to 10.
'''

# 分析下面的段落，然后在最后一行得出结论："因此一致性得分是 {s}"，其中 s 是 1 到 10 之间的整数。
