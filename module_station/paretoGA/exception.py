class BuildFactoryException(Exception):
    def __init__(self):
        # def build_factory in factory.py
        pass


class EmptyGenerationException(Exception):
    def __init__(self):
        msg = 'When first_generation is False value, you have to enter generation value'
        super().__init__(msg)


class InfiniteLoopException(Exception):
    def __init__(self, func):
        self.func = func
        msg = 'infinite loop is occurred during new generation'
        super().__init__(msg)

    def __call__(self):
        self.func()