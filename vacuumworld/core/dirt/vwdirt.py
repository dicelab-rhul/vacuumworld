
from pystarworlds.Identifiable import Identifiable

from .dirt_interface import Dirt as Drt



class Dirt(Identifiable):
    def __init__(self, dirt: Drt) -> None:        
        super(Dirt, self).__init__()
        self._Identifiable__ID: str = dirt.name #hack...
        self.dirt: Drt = dirt
