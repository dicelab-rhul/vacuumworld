
from pystarworlds.Identifiable import Identifiable



class Dirt(Identifiable):
    def __init__(self, dirt):        
        super(Dirt, self).__init__()
        self._Identifiable__ID = dirt.name #hack...
        self.dirt = dirt
