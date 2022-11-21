#!/usr/bin/env python3

from unittest import main, TestCase

from vacuumworld.common.vwcolour import VWColour
from vacuumworld.model.dirt.vwdirt import VWDirt
from vacuumworld.model.dirt.vwdirt_appearance import VWDirtAppearance


class TestDirt(TestCase):
    def test_dirt(self) -> None:
        for colour in [VWColour.green, VWColour.orange]:
            dirt: VWDirt = VWDirt(colour=colour)
            dirt_appearance: VWDirtAppearance = VWDirtAppearance(dirt_id=dirt.get_id(), progressive_id=dirt.get_progressive_id(), colour=colour)

            self.assertEqual(dirt.get_id(), dirt_appearance.get_id())
            self.assertEqual(dirt.get_progressive_id(), dirt_appearance.get_progressive_id())
            self.assertEqual(dirt.get_colour(), colour)
            self.assertEqual(dirt_appearance.get_colour(), colour)


if __name__ == "__main__":
    main()
