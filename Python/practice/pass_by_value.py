# https://stackoverflow.com/questions/986006/how-do-i-pass-a-variable-by-reference

class PassByReference:
    def __init__(self):
        self.variable = 'Original'
        self.change(self.variable)
        print(self.variable)

    def change(self, var):
        var = 'Changed'

test = PassByReference()