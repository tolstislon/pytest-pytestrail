class MissingRequiredParameter(Exception):

    def __init__(self, param):
        super().__init__(f'Missing Required Parameter "{param}"')
