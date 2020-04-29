class BuildFactoryException(Exception):
    def __init__(self):
        msg = 'The factory cannot make last station'
        super().__init__(msg)
