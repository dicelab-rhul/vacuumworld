#!/usr/bin/env python3

from typing import Iterable, override

from vacuumworld import run
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.model.actions.vwidle_action import VWIdleAction
from vacuumworld.model.actions.vwmove_action import VWMoveAction
from vacuumworld.model.actor.mind.surrogate.vwactor_mind_surrogate import VWActorMindSurrogate
from vacuumworld.common.vworientation import VWOrientation
from vacuumworld.common.vwcoordinates import VWCoord
from vacuumworld.model.actions.vwturn_action import VWTurnAction
from vacuumworld.common.vwdirection import VWDirection


class MyMind(VWActorMindSurrogate):
    def __init__(self) -> None:
        super(MyMind, self).__init__()

        # Add here all the attributes you need/want.

        # Example of a target location set in advance.
        self.__target_coords: VWCoord = VWCoord(2, 6)

    @override
    def revise(self) -> None:
        self.__temporal_distance_to_target_if_move: int = self.__compute_minimum_temporal_distance_from_target(hypotetical_orientation=self.get_own_orientation())
        self.__temporal_distance_to_target_if_turn_left: int = self.__compute_minimum_temporal_distance_from_target(hypotetical_orientation=self.get_own_orientation().get_left())
        self.__temporal_distance_to_target_if_turn_right: int = self.__compute_minimum_temporal_distance_from_target(hypotetical_orientation=self.get_own_orientation().get_right())
        self.__minimum_temporal_distance: int = min(self.__temporal_distance_to_target_if_move, self.__temporal_distance_to_target_if_turn_left, self.__temporal_distance_to_target_if_turn_right)

    @override
    def decide(self) -> Iterable[VWAction]:
        if self.__target_coords == self.get_own_position():
            return [VWIdleAction()]
        elif self.__minimum_temporal_distance == self.__temporal_distance_to_target_if_move:
            return [VWMoveAction()]
        elif self.__minimum_temporal_distance == self.__temporal_distance_to_target_if_turn_left:
            return [VWTurnAction(VWDirection.left)]
        elif self.__minimum_temporal_distance == self.__temporal_distance_to_target_if_turn_right:
            return [VWTurnAction(VWDirection.right)]
        else:
            raise ValueError("This is impossible: one of the temporal distances should be the minimum.")

    def __compute_minimum_temporal_distance_from_target(self, hypotetical_orientation: VWOrientation) -> int:
        return self.__count_minimum_number_of_turns_to_face_target(hypotetical_orientation=hypotetical_orientation) + self.__count_minimum_number_of_moves_to_target()

    def __count_minimum_number_of_turns_to_face_target(self, hypotetical_orientation: VWOrientation) -> int:
        # Positive if the target is to the east, negative if the target is to the west, zero if the target is vertically aligned with the agent.
        horizontal_delta_to_target: int = self.__target_coords.get_x() - self.get_own_position().get_x()
        # Positive if the target is to the south, negative if the target is to the north, zero if the target is horizontally aligned with the agent.
        vertical_delta_to_target: int = self.__target_coords.get_y() - self.get_own_position().get_y()

        # If the target location is in front of the agent (not necessarily aligned)...
        if self.__is_target_in_front(hypotetical_orientation=hypotetical_orientation, horizontal_delta=horizontal_delta_to_target, vertical_delta=vertical_delta_to_target):
            # ... and the agent is already aligned with the target, then no turn actions are needed, else just 1 turn action.
            return 0 if self.__is_target_aligned(horizontal_delta=horizontal_delta_to_target, vertical_delta=vertical_delta_to_target) else 1
        # If the target location is behind the agent...
        elif self.__is_target_behind(hypotetical_orientation=hypotetical_orientation, horizontal_delta=horizontal_delta_to_target, vertical_delta=vertical_delta_to_target):
            # ... then 2 turn actions are needed.
            return 2
        # Otherwise, the target location is on the side of the agent...
        else:
            # ... and 1 turn is needed.
            return 1

    # The target is in front of the agent depending on the agent's orientation, and the horizontal/vertical delta between target and agent.
    def __is_target_in_front(self, hypotetical_orientation: VWOrientation, horizontal_delta: int, vertical_delta: int) -> bool:
        if hypotetical_orientation == VWOrientation.north:
            return vertical_delta < 0
        elif hypotetical_orientation == VWOrientation.south:
            return vertical_delta > 0
        elif hypotetical_orientation == VWOrientation.west:
            return horizontal_delta < 0
        elif hypotetical_orientation == VWOrientation.east:
            return horizontal_delta > 0
        else:
            raise ValueError(f"Invalid hypotetical orientation: {hypotetical_orientation}.")

    # The target is behind the agent depending on the agent's orientation, and the horizontal/vertical delta between target and agent.
    def __is_target_behind(self, hypotetical_orientation: VWOrientation, horizontal_delta: int, vertical_delta: int) -> bool:
        if hypotetical_orientation == VWOrientation.north:
            return vertical_delta > 0
        elif hypotetical_orientation == VWOrientation.south:
            return vertical_delta < 0
        elif hypotetical_orientation == VWOrientation.west:
            return horizontal_delta > 0
        elif hypotetical_orientation == VWOrientation.east:
            return horizontal_delta < 0
        else:
            raise ValueError(f"Invalid hypotetical orientation: {hypotetical_orientation}.")

    # The target is aligned with the agent if at least one of the deltas is zero.
    def __is_target_aligned(self, horizontal_delta: int, vertical_delta: int) -> bool:
        return horizontal_delta == 0 or vertical_delta == 0

    def __count_minimum_number_of_moves_to_target(self) -> int:
        # |target_x - agent_x| + |target_y - agent_y|, otherwise known as the Manhattan distance.
        return abs(self.get_own_position().get_x() - self.__target_coords.get_x()) + abs(self.get_own_position().get_y() - self.__target_coords.get_y())


if __name__ == "__main__":
    run(default_mind=MyMind())
