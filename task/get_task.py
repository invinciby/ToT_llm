def get_task(name):
    if name == 'text':
        from task.text import Text
        return Text()
    else:
        raise NotImplementedError