class ViewModelBase:
    def __init__(self):
        self.errors = []

    @property
    def error_msg(self):
        msg = 'There are errors with your request: \n' + \
              '\n'.join(self.errors)

        return msg
