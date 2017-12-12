class Node:
    def __init__(self, name, dependencies=None):
        if dependencies is None:
            dependencies = []
        self.dependencies = dependencies
        self.name = name
    
    def clear_dependency(self, value):
        try:
            self.dependencies.remove(value.name)
        except ValueError:
            pass