import google.generativeai as genai

genai.configure(api_key='Yor API Key',transport="rest") 

gemini_model = genai.GenerativeModel(model_name="gemini-2.0-flash")


completion_tokens = prompt_tokens = 0
# 使用backoff库实现指数退避重试机制
import backoff

@backoff.on_exception(backoff.expo, Exception, max_tries=5)
def completions_with_backoff(prompt,stop):
  
    ans = gemini_model.generate_content(prompt,stream=False)
    
    return ans

def gpt(prompt, model="gemini", temperature=0.7, max_tokens=1000, n=1, stop=None)->list:

    return gemini(prompt, model, temperature, max_tokens, n, stop)

def gemini(prompt, model="gemini", temperature=0.7, max_tokens=1000, n=1, stop=None)->list:
    global completion_tokens, prompt_tokens
    
    outputs = []
    
    while n>0:
        cnt = min(20, n)
        n -= cnt
        
        res = completions_with_backoff(prompt,stop)
        
        outputs.append(res.text)
        
        # print(res)
        completion_tokens += res.usage_metadata.total_token_count
        prompt_tokens += res.usage_metadata.prompt_token_count
        
    return outputs

def gpt_usage(backend="gemini"):
    global completion_tokens, prompt_tokens
    cost = 0.0000002 * prompt_tokens + 0.0000001 * completion_tokens
    return {"completion_tokens": completion_tokens, "prompt_tokens": prompt_tokens, "cost": cost}

    

# cot_prompt = '''Use numbers and basic arithmetic operations (+ - * /) to obtain 24. Each step, you are only allowed to choose two of the remaining numbers to obtain a new number.
# Input: 4 4 6 8
# Steps:
# 4 + 8 = 12 (left: 4 6 12)
# 6 - 4 = 2 (left: 2 12)
# 2 * 12 = 24 (left: 24)
# Answer: (6 - 4) * (4 + 8) = 24
# Input: 2 9 10 12
# Steps:
# 12 * 2 = 24 (left: 9 10 24)
# 10 - 9 = 1 (left: 1 24)
# 24 * 1 = 24 (left: 24)
# Answer: (12 * 2) * (10 - 9) = 24
# Input: 4 9 10 13
# Steps:
# 13 - 10 = 3 (left: 3 4 9)
# 9 - 3 = 6 (left: 4 6)
# 4 * 6 = 24 (left: 24)
# Answer: 4 * (9 - (13 - 10)) = 24
# Input: 1 4 8 8
# Steps:
# 8 / 4 = 2 (left: 1 2 8)
# 1 + 2 = 3 (left: 3 8)
# 3 * 8 = 24 (left: 24)
# Answer: (1 + 8 / 4) * 8 = 24
# Input: 5 5 5 9
# Steps:
# 5 + 5 = 10 (left: 5 9 10)
# 10 + 5 = 15 (left: 9 15)
# 15 + 9 = 24 (left: 24)
# Answer: ((5 + 5) + 5) + 9 = 24
# Input: 2 5 4 10
# '''

# out = gpt(prompt=cot_prompt,n=1, stop=False)

# print(out)