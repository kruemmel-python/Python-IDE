class PluginInterface:
    def __init__(self, ide):
        self.ide = ide

    def initialize(self):
        raise NotImplementedError("Plugins must implement the initialize method")

    def deinitialize(self):
        raise NotImplementedError("Plugins must implement the deinitialize method")
