def get_task(name):
    if name == 'game24':
        from task.game24 import Game24
        return Game24()
    elif name == 'text':
        from task.text import Text
        return Text()
    else:
        raise NotImplementedError