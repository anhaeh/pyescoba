class ImplementationError(Exception):
    def __init__(self, method, class_name):
        super(ImplementationError, self).__init__()
        self.method = method
        self.class_name = class_name

    def __str__(self):
        return "not implemented method '{0}' in class {1}".format(self.method, self.class_name)
