from task.base import Task, DATA_PATH
import os
import re
from prompts.text import *
from config.model import gpt

class Text(Task):
    def __init__(self, file='data_100_random_text.txt'):
        super().__init__()
        path = os.path.join(DATA_PATH,'text', file)
        
        self.data = open(path).readlines()
        # print(self.data[0])
        self.steps = 2
        # 定义一个列表，包含两个元素，第一个元素是字符串'\nPassage:\n'，第二个元素是None
        self.stops = ['\nPassage:\n',None]

    def __len__(self) -> int:
        return len(self.data)
    
    def get_input(self, idx: int) -> str:
        return self.data[idx]
    
    def test_output(self, idx: int, output: str):
        output = output.split('Passage:\n')[-1]
        prompt = score_prompt + output
        score_outputs = gpt(prompt, n=5, model='gemini')
        scores = []
        
        for score_output in score_outputs:
            pattern = r".*coherency score is (\d+)."
            match = re.match(pattern, score_output, re.DOTALL)
            if match:
                score = int(match.groups()[0])
                scores.append(score)
            else:
                print(f'---------------score no match:{[score_output]}---------------')
                
            # print(scores)
            
            info = {'rs':scores, 'r':sum(scores)/len(scores) if scores else 0}
            return info
    
    
    @staticmethod
    def standard_prompt_wrap(x:str, y:str='')->str:
        return standard_prompt.format(input=x) + y
    
    
    @staticmethod
    def cot_prompt_wrap(x:str, y:str='')->str:
        return cot_prompt.format(input=x) + y
    
    
    @staticmethod
    def vote_prompt_wrap(x:str, ys:str='')->str:
        prompt = vote_prompt
        
        for i, y in enumerate(ys, 1):
            prompt += f'Choice {i}:\n{y}\n'
            
        return prompt
    
    
    @staticmethod
    def vote_outputs_unwrap(vote_outputs: list, n_candidates:int) -> list:
        
        # print(f"----candidates:{n_candidates}")
        vote_results = [0]* n_candidates
        
        for vote_output in vote_outputs:
            pattern = r".*The best choice is .*(\d+).*"
            match = re.match(pattern, vote_output, re.DOTALL)
            if match:
                vote = int(match.groups()[0]) - 1
                
                if vote in range(n_candidates):
                    vote_results[vote] += 1
              
            else:
                print(f'---------------vote no match:{[vote_output]}---------------')
        # print(f'The vote results are:{vote_results}')
        return vote_results
    
    @staticmethod
    def compare_prompt_wrap(x:str, ys:str='')->str:
        assert len(ys) == 2, 'compare task must have 2 candidates'
        ys = [y.split('Passage:\n')[-1] for y in ys]
        prompt = compare_prompt + f'Passage 1:\n{ys[0]}\n\nPassage 2:\n{ys[1]}\n'

        return prompt
    
    
    @staticmethod
    def compare_outputs_unwrap(compare_outputs: list) -> list:
        if 'more coherent passage is 1' in compare_outputs:
            return 0
        elif 'more coherent passage is 2' in compare_outputs:
            return 1
        elif 'two passages are similarly coherent' in compare_outputs:
            return 0.5
        else:
            print(f'-----------------compare no match: {[compare_outputs]}')
            return -1
        
# if __name__ == '__main__':
#     value_ouput = ['This choice presents a set of seemingly unrelated, mostly declarative sentences. There\'s no clear unifying theme or purpose, and it doesn\'t appear to be instruction-following in any way. It reads more like a collection of random observations or thoughts.\n\nChoice 2:\nTo make a rainbow, spray water into the air on a sunny day, with your back to the sun. He would only ever be useful as a warning about the dangers of being useful. Sometimes it is better to just walk away from things and go back to them later when you’re in a better frame of mind. He knew it was going to be a long day when he realized he\'d forgotten his toothbrush.\n\nThis choice includes a clear, actionable instruction: "To make a rainbow, spray water into the air on a sunny day, with your back to the sun." The remaining sentences are similar to those in Choice 1, being somewhat unrelated observations. However, the inclusion of an instruction makes this choice potentially more promising.\n\nChoice 3:\nIf I had to pick one place to live for the rest of my life, I would live in that place. It was just then the sky opened up and I felt like I could fly, but only because someone opened the window. If I could travel through time I would travel to the future and see if they had invented teleportation yet. I\'d rather be a bird than a fish.\n\nSimilar to Choice 1, this choice presents a collection of sentences that express thoughts, preferences, or hypothetical scenarios. There\'s no obvious instruction or task being addressed.\n\nAnalysis:\n\nChoice 1 and 3 lack any explicit instruction, making them the least promising. Choice 2 contains a concrete instruction about how to make a rainbow, which is a specific action that could be followed. The other statements in Choice 2 are observations, but the presence of the instruction makes it the best choice so far.\n\nThe best choice is 2\n']
    
    
#     ans = Text.vote_outputs_unwrap(value_ouput,3)