#!/usr/bin/env python3

from unittest import main, TestCase

from vacuumworld import run
from vacuumworld.gui.gui import VWGUI
from vacuumworld.model.actor.hystereticmindsurrogate import VWHystereticMindSurrogate


class TestIllegalRunInputs(TestCase):
    '''
    All the arguments of `run()` that are not tested are simply ignored if they are not valid.
    '''

    def test_illegal_speed_value(self) -> None:      
        for value in [-1, -0.3, 1.1, 2, 3, 100, 1000]:
            self.assertRaises(ValueError, VWGUI._VWGUI__validate_arguments, play=False, file_to_load="", scale=1, speed=value)

    def test_illegal_scale_value(self) -> None:
        for value in [-1, -0.3, 2.6, 3, 100, 1000]:
            self.assertRaises(ValueError, VWGUI._VWGUI__validate_arguments, play=False, file_to_load="", scale=value, speed=0)

    def test_play_without_load(self) -> None:
        self.assertRaises(ValueError, VWGUI._VWGUI__validate_arguments, play=True, file_to_load="", scale=1, speed=0)

    def test_illegal_minds_combination(self) -> None:
        self.assertRaises(AssertionError, run)
        self.assertRaises(AssertionError, run, green_mind=VWHystereticMindSurrogate())
        self.assertRaises(AssertionError, run, orange_mind=VWHystereticMindSurrogate())
        self.assertRaises(AssertionError, run, white_mind=VWHystereticMindSurrogate())
        self.assertRaises(AssertionError, run, green_mind=VWHystereticMindSurrogate(), orange_mind=VWHystereticMindSurrogate())
        self.assertRaises(AssertionError, run, green_mind=VWHystereticMindSurrogate(), white_mind=VWHystereticMindSurrogate())
        self.assertRaises(AssertionError, run, orange_mind=VWHystereticMindSurrogate(), white_mind=VWHystereticMindSurrogate())


if __name__ == "__main__":
    main()
