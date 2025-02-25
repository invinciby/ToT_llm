# -*- coding = utf-8 -*-
# @Time : 2024/9/25 15:26
# @Author : Vinci
# @File : Test_openai_kay.py
# @Software: PyCharm

from openai import OpenAI

client = OpenAI(
    api_key = "sk-B9wonBTcGeUhTY3Rn3N0raK7jR8DQeKuJzxmhtOAdQXAnK2o",  # 此处的key需要自己通过官方购买 或者通过其他渠道获取
    base_url = "https://api.chatanywhere.tech" # 中转地址
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "讲个笑话",
        }
    ],
    model="gpt-3.5-turbo", #此处可更换其它模型
)
print(chat_completion.choices[0].message.content)

