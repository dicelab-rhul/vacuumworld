#!/usr/bin/env python3

from typing import Iterable, override
from pyoptional.pyoptional import PyOptional

from vacuumworld import run
from vacuumworld.model.actor.mind.surrogate.vwactor_mind_surrogate import VWActorMindSurrogate
from vacuumworld.model.actions.vwidle_action import VWIdleAction
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.model.actions.vwmove_action import VWMoveAction
from vacuumworld.model.actions.vwturn_action import VWTurnAction
from vacuumworld.common.vwdirection import VWDirection
from vacuumworld.common.vwcoordinates import VWCoord


class MyMind(VWActorMindSurrogate):
    '''
    The goal of this surrogate mind is to find any corner of the grid.

    This surrogate mind takes advantage of the Wall API and the 3x2 `VWObservation` size in order to find a corner.
    '''

    def __init__(self) -> None:
        super(MyMind, self).__init__()

        self.__corner_found: bool = False

    @override
    def revise(self) -> None:
        if not self.__corner_found and self.__can_see_corner():
            coord: PyOptional[VWCoord] = self.__get_visible_corner_coordinates()

            assert coord.is_present()

            print(f"I found a corner at {coord.or_else_raise()}. I'm staying idle from now on.")

            self.__corner_found = True

    @override
    def decide(self) -> Iterable[VWAction]:
        # If we've found a corner, don't do anything else.
        if self.__corner_found:
            return [VWIdleAction()]
        # If we can see a wall one step ahead, but no wall to the left, turn right.
        elif self.get_latest_observation().is_wall_one_step_ahead() and not self.get_latest_observation().is_wall_immediately_to_the_left():
            return [VWTurnAction(VWDirection.right)]
        # If we can see a wall one step ahead, but no wall to the right, turn left.
        elif self.get_latest_observation().is_wall_one_step_ahead() and not self.get_latest_observation().is_wall_immediately_to_the_right():
            return [VWTurnAction(VWDirection.left)]
        # If we can see a wall directly ahead, but no wall to the left, turn right.
        elif self.get_latest_observation().is_wall_immediately_ahead() and not self.get_latest_observation().is_wall_immediately_to_the_left():
            return [VWTurnAction(VWDirection.right)]
        # If we can see a wall directly ahead, but no wall to the right, turn left.
        elif self.get_latest_observation().is_wall_immediately_ahead() and not self.get_latest_observation().is_wall_immediately_to_the_right():
            return [VWTurnAction(VWDirection.left)]
        # Otherwise move forward.
        else:
            return [VWMoveAction()]

    def __can_see_corner(self) -> bool:
        # We can see a corner if we can see a corner `VWLocation` in the current `VWObservation`.
        return any(loc.is_corner() for loc in self.get_latest_observation().get_locations().values())

    def __get_visible_corner_coordinates(self) -> PyOptional[VWCoord]:
        # We return a `PyOptional` wrapping the coordinates of the first corner `VWLocation` we can see.
        # We always check the current `VWObservation` in the same order of `VWPositionNames` (`center`, `forward`, `left`, `right`, `forwardleft`, `forwardright`).
        # We return an empty `PyOptional` if we can't see any corner.
        return PyOptional[VWCoord].of_nullable(next((loc.or_else_raise().get_coord() for loc in self.get_latest_observation().get_locations_in_order() if loc.is_present() and loc.or_else_raise().is_corner()), None))


if __name__ == "__main__":
    run(default_mind=MyMind(), skip=True)
