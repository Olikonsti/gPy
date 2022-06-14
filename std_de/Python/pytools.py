
class Pytools:
    def __init__(self, interpreter):
        self.interpreter = interpreter

    def declare_variable(self, variable_name, variable_value):
        self.interpreter.stack[variable_name] = variable_value

    def get_variable(self, variable_name):
        return self.interpreter.stack[variable_name]

module_class = Pytools