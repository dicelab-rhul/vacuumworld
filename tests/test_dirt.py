#!/usr/bin/env python3

from vacuumworld.common.colour import Colour
from vacuumworld.model.dirt.dirt import Dirt
from vacuumworld.model.dirt.dirt_appearance import VWDirtAppearance



def test() -> None:
    for colour in [Colour.green, Colour.orange]:
        dirt: Dirt = Dirt(colour=colour)
        dirt_appearance: VWDirtAppearance = VWDirtAppearance(dirt_id=dirt.get_id(), progressive_id=dirt.get_progressive_id(), colour=colour)
        
        assert dirt.get_id() == dirt_appearance.get_id()
        assert dirt.get_progressive_id() == dirt_appearance.get_progressive_id()
        assert dirt.get_colour() == colour
        assert dirt_appearance.get_colour() == colour


if __name__ == "__main__":
    test()
