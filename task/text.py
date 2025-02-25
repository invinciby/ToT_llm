
from task.base import Task

class Text(Task):
    def __init__(self, text):
        self.text = text

    def run(self):
        print(self.text)