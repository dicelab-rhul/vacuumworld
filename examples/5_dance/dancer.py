#!/usr/bin/env python3

from random import randint, choice
from typing import Iterable, cast
from pyoptional.pyoptional import PyOptional

from pystarworldsturbo.common.content_type import MessageContentType

from vacuumworld import run
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.model.actions.vwidle_action import VWIdleAction
from vacuumworld.model.actions.vwmove_action import VWMoveAction
from vacuumworld.model.actions.vwturn_action import VWTurnAction
from vacuumworld.model.actions.vwbroadcast_action import VWBroadcastAction
from vacuumworld.common.vworientation import VWOrientation
from vacuumworld.common.vwdirection import VWDirection
from vacuumworld.common.vwcolour import VWColour
from vacuumworld.common.vwcoordinates import VWCoord

from dance_mind import DanceMind


class ColourMind(DanceMind):
    '''
    This mind is build on top of the basic mind. It adds additional behaviours which address
    the task at hand.
    '''
    def __init__(self) -> None:
        super(ColourMind, self).__init__()

        self.__target_loc: PyOptional[VWCoord] = PyOptional.empty()  # The location to move to.
        self.__dance_time: list[int] = []  # Time interval where the agent should be dancing.

    def sub_revise(self) -> None:
        '''
        This function gets called after all of the basic state updates happen in DanceMind.
        The behaviour is quite simple, we just listen for messages and set attributes in
        response to specific messages.
        '''

        self.__leader: bool = self.get_own_colour() == VWColour.orange  # Am I the orange agent? Orange is the leader.

        for message in map(lambda m: m.get_content(), self.get_latest_received_messages()):
            self.__parse_message(message=message)

    def __parse_message(self, message: MessageContentType) -> None:
        '''
        This function is used to parse messages when pattern matching is not available.
        '''

        error_message: str = f"{'#'*30}\nWARNING: Bad message: {str(message)}\n{'#'*30}"

        if ColourMind.__well_formed(message=message):
            assert isinstance(message, list)
            assert len(message) == 2
            assert isinstance(message[0], str)
            assert isinstance(message[1], list)
            assert len(message[1]) == 2
            assert all(isinstance(x, int) for x in message[1])

            if message[0] == "goto" and isinstance(message[1][0], int) and isinstance(message[1][1], int):
                self.__target_loc = PyOptional.of(VWCoord(x=message[1][0], y=message[1][1]))
            elif message[0] == "dance" and isinstance(message[1][0], int) and isinstance(message[1][1], int):
                self.__dance_time = [time for time in message[1] if isinstance(time, int)]
            else:
                print(error_message)
        else:
            print(error_message)

    @staticmethod
    def __well_formed(message: MessageContentType) -> bool:
        ''' Is the message well formed? '''
        if not isinstance(message, list):
            return False
        elif len(message) != 2:
            return False
        elif not isinstance(message[0], str):
            return False
        elif not isinstance(message[1], list):
            return False
        elif len(message[1]) != 2:
            return False
        elif any(not isinstance(x, int) for x in message[1]):
            return False
        else:
            return True

    def decide(self) -> Iterable[VWAction]:
        '''
        This is a slightly more complex function which implements some teleo-reactive
        behaviour but is essentially just a big if statement. Each "production rule"
        maps a condition (or set of conditions) to an action or a subgoal.
        For example in the first part of the if statement, we check if we should be dancing
        (the condition) and if so we do some dancing behaviour (the action). Or if we aren't
        at the meeting point, our subgoal is to move to the meeting point. A subgoal is
        different from an action in that it does not explicitly define an action but is instead
        used to derive an action based on context.

            shouldDance -> dance
            notAtMeetingPoint -> moveToMeetingPoint
            etc...

        In the teleo-reactive model the ordering of the rules IS important. The first
        condition to be checked corresponds to the highest priority action. In order to
        replicate this in Python we need to ensure that the conditions are checked in
        order of priority (from highest to lowest, so here dancing is the highest priority
        action) and that after a condition succeeds we choose an action and do not check
        further ones. For this reason it's important that we use if/elif structure, since
        only one case can "fire".
        '''

        # Rule 1:
        # should dance -> dance
        if self.__update_dancing_status():
            return [self.__dance()]
        # Rule 2:
        # no meeting point agreed and leader -> choose and broadcast meeting point
        elif self.__target_loc.is_empty() and self.__leader:
            loc1, loc2 = ColourMind.__gen_meeting_locs()
            self.__target_loc = PyOptional.of(loc1)

            return [VWBroadcastAction(message=["goto", [loc2.get_x(), loc2.get_y()]], sender_id=self.get_own_id())]
        # Rule 3:
        # no meeting point and not leader -> do nothing (wait for a meeting point)
        elif self.__target_loc.is_empty() and not self.__leader:
            return [VWIdleAction()]
        # Rule 4:
        # not at target location -> move to target location (subgoal)
        elif not self.__at_target_loc():
            return [self.__move_to_target()]
        # Rule 5:
        # at target location but not facing friend -> turn
        elif self.__at_target_loc() and not self.__can_see_friend():
            return [VWTurnAction(VWDirection.left)]
        # Rule 6:
        # at target location and can see friend and no agreed dancing time -> choose and
        #   broadcast dance time
        elif self.__at_target_loc() and self.__can_see_friend() and not self.__dance_time and self.__leader:
            dance_start: int = self.get_tick() + randint(2, 5)
            dance_end: int = dance_start + randint(5, 10)

            self.__dance_time = [dance_start, dance_end]

            return [VWBroadcastAction(message=["dance", cast(MessageContentType, self.__dance_time)], sender_id=self.get_own_id())]
        else:
            # otherwise do nothing
            return [VWIdleAction()]

    @staticmethod
    def __gen_meeting_locs(max_n: int=8) -> list[VWCoord]:
        '''
        A function to generate a meeting point, a default grid size of 8 is assumed.
        Picks a random point that isn't on the grid perimeter (adjacent to a wall).
        Randomly chooses a second point directly adjacent to the first.
        '''
        x1: int = randint(1, max_n-2)
        y1: int = randint(1, max_n-2)
        offset: list[int] = choice([[1, 0], [-1, 0], [0, 1], [0, -1]])
        x2: int = x1 + offset[0]
        y2: int = y1 + offset[1]

        return [VWCoord(x=x1, y=y1), VWCoord(x=x2, y=y2)]

    def __move_to_target(self) -> VWAction:
        '''
        A simple (although sub-optimal) function for infering which action to take in order
        to reach the target location.

        If you're facing the right way move forward otherwise turn
        '''

        # Starts by finding the x and y deltas
        diff: VWCoord = VWCoord(x=self.get_own_position().get_x() - self.__target_loc.or_else_raise().get_x(), y=self.get_own_position().get_y() - self.__target_loc.or_else_raise().get_y())

        # infer desired orientation based on x and y deltas
        if diff.get_y() > 0:
            desired_ori: VWOrientation = VWOrientation.north
        elif diff.get_y() < 0:
            desired_ori: VWOrientation = VWOrientation.south
        elif diff.get_x() > 0:
            desired_ori: VWOrientation = VWOrientation.west
        elif diff.get_x() < 0:
            desired_ori: VWOrientation = VWOrientation.east
        else:
            return VWIdleAction()

        assert isinstance(desired_ori, VWOrientation)

        # if orientation is correct go forward, otherwise turn
        return VWMoveAction() if desired_ori == self.get_own_orientation() else VWTurnAction(VWDirection.left)

    def __at_target_loc(self) -> bool:
        ''' Am I at the target location? '''
        return self.get_own_position() == self.__target_loc.or_else_raise()

    def __can_see_friend(self) -> bool:
        ''' Can I see an agent directly ahead? '''
        return not self.get_latest_observation().is_wall_immediately_ahead() and self.get_latest_observation().get_forward().or_else_raise().has_cleaning_agent()

    def __update_dancing_status(self) -> bool:
        ''' Is it time to dance? '''
        if not self.__dance_time:
            return False
        elif self.get_tick() < self.__dance_time[0]:
            print(f"I can't wait to dance in {self.__dance_time[0]-self.get_tick()} cycles!")

            return False
        elif self.get_tick() > self.__dance_time[0] and self.get_tick() < self.__dance_time[1]:
            print(ColourMind.__dance_enjoyment_declaration())

            return True
        elif self.get_tick() == self.__dance_time[1]:
            # Once the dancing window ends, reset the dance time and target location, now
            # the behaviour will start "from the beginning" choosing a new meeting location
            # and doing another dance.
            self.__dance_time = []
            self.__target_loc = PyOptional.empty()

            print("Okay enough dancing let's be serious... :-|")

            return False
        else:
            return False

    def __dance(self) -> VWAction:
        '''
        A small bit of maths to coordinate the dancing.

        We want the agent to turn all the way right and then all the way left. Say the
        left action is 0 and the right is 1 we want a function, f, s.t:

        f(0) = 0
        f(1) = 1
        f(2) = 1
        f(3) = 0
        f(4) = 0
        .
        .
        .
        '''
        phase: int = ((self.get_tick() - self.__dance_time[0]) // 2) % 2

        assert phase in [0, 1]

        # phase != leader is equivalent to xor, this way the follower will turn the opposite
        #   way to the leader so they mirror the "dance moves".
        return VWTurnAction(direction=VWDirection.right if phase != self.__leader else VWDirection.left)

    @staticmethod
    def __dance_enjoyment_declaration() -> str:
        ''' Superfluous '''

        strs: list[str] = [
            "I love dancing!",
            "Boogy time!",
            "This song is great!",
            "We're doing the Vacuum Shuffle!",
            "Nice moves!"
        ]

        return choice(strs)


if __name__ == "__main__":
    run(default_mind=ColourMind(), skip=True, speed=0.4)
