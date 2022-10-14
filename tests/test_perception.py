#!/usr/bin/env python3

from unittest import main, TestCase
from typing import Dict

from pystarworldsturbo.common.message import BccMessage
from pystarworldsturbo.common.action_outcome import ActionOutcome
from pystarworldsturbo.common.action_result import ActionResult

from vacuumworld.common.position_names import PositionNames
from vacuumworld.model.actions.idle_action import VWIdleAction
from vacuumworld.model.dirt.dirt_appearance import VWDirtAppearance
from vacuumworld.common.orientation import Orientation
from vacuumworld.common.colour import Colour
from vacuumworld.model.actor.vwactor_appearance import VWActorAppearance
from vacuumworld.common.coordinates import Coord
from vacuumworld.model.environment.vwlocation import VWLocation
from vacuumworld.common.observation import Observation



class TestPerception(TestCase):
    def test_observation(self) -> None:
        a1: VWActorAppearance = VWActorAppearance(actor_id="foo", progressive_id="1", colour=Colour.green, orientation=Orientation.east)
        a2: VWActorAppearance = VWActorAppearance(actor_id="bar", progressive_id="2", colour=Colour.orange, orientation=Orientation.north)
        u1: VWActorAppearance = VWActorAppearance(actor_id="foobar", progressive_id="3", colour=Colour.user, orientation=Orientation.west)
        u2: VWActorAppearance = VWActorAppearance(actor_id="barfoo", progressive_id="4", colour=Colour.user, orientation=Orientation.south)
        d1: VWDirtAppearance = VWDirtAppearance(dirt_id="running", progressive_id="5", colour=Colour.green)
        d2: VWDirtAppearance = VWDirtAppearance(dirt_id="out_of", progressive_id="6", colour=Colour.orange)
        d3: VWDirtAppearance = VWDirtAppearance(dirt_id="ideas", progressive_id="7", colour=Colour.orange)
        c: Coord = Coord(4,4)
        f: Coord = c.forward(orientation=a1.get_orientation())
        l: Coord = c.left(orientation=a1.get_orientation())
        r: Coord = c.right(orientation=a1.get_orientation())
        fl: Coord = c.forwardleft(orientation=a1.get_orientation())
        fr: Coord = c.forwardright(orientation=a1.get_orientation())
        
        # TODO: use non-trivial walls.
        sample_wall: Dict[Orientation, bool] = {Orientation.north: False, Orientation.south: False, Orientation.west: False, Orientation.east: False}

        # TODO: customise the wall depending on the coordinates.

        center: VWLocation = VWLocation(coord=c, actor_appearance=a1, dirt_appearance=None, wall=sample_wall)
        left: VWLocation = VWLocation(coord=l, actor_appearance=None, dirt_appearance=None, wall=sample_wall)
        right: VWLocation = VWLocation(coord=r, actor_appearance=a2, dirt_appearance=d1, wall=sample_wall)
        forward: VWLocation = VWLocation(coord=f, actor_appearance=None, dirt_appearance=d2, wall=sample_wall)
        forwardleft: VWLocation = VWLocation(coord=fl, actor_appearance=u1, dirt_appearance=None, wall=sample_wall)
        forwardright: VWLocation = VWLocation(coord=fr, actor_appearance=u2, dirt_appearance=d3, wall=sample_wall)

        perceived_locations: Dict[PositionNames, VWLocation] = {
            PositionNames.center: center.deep_copy(),
            PositionNames.left: left.deep_copy(),
            PositionNames.right: right.deep_copy(),
            PositionNames.forward: forward.deep_copy(),
            PositionNames.forwardleft: forwardleft.deep_copy(),
            PositionNames.forwardright: forwardright.deep_copy()
        }

        for action_outcome in (ActionOutcome.impossible, ActionOutcome.success, ActionOutcome.failure):
            result: ActionResult = ActionResult(outcome=action_outcome)
            o: Observation = Observation(action_type=VWIdleAction, action_result=result, locations_dict=perceived_locations)

            self.assertEqual(o.get_center().get_coord(), c)
            self.assertEqual(o.get_center().get_actor_appearance(), a1)
            self.assertIsNone(o.get_center().get_dirt_appearance())

            self.assertEqual(o.get_left().get_coord(), l)
            self.assertIsNone(o.get_left().get_actor_appearance())
            self.assertIsNone(o.get_left().get_dirt_appearance())

            self.assertEqual(o.get_right().get_coord(), r)
            self.assertEqual(o.get_right().get_actor_appearance(), a2)
            self.assertEqual(o.get_right().get_dirt_appearance(), d1)

            self.assertEqual(o.get_forward().get_coord(), f)
            self.assertIsNone(o.get_forward().get_actor_appearance())
            self.assertEqual(o.get_forward().get_dirt_appearance(), d2)

            self.assertEqual(o.get_forwardleft().get_coord(), fl)
            self.assertEqual(o.get_forwardleft().get_actor_appearance(), u1)
            self.assertIsNone(o.get_forwardleft().get_dirt_appearance())

            self.assertEqual(o.get_forwardright().get_coord(), fr)
            self.assertEqual(o.get_forwardright().get_actor_appearance(), u2)
            self.assertEqual(o.get_forwardright().get_dirt_appearance(), d3)
            
            # TODO: check for walls.


    def test_message(self) -> None:
        for content in (1, 1.32343, "foo", ["foo", 1, 1.234, [], (), {}], ("foo", 1, 1.234, [], (), {}), {1: ["", None], 1.2343: (3, 4.5)}):
            for sender in ("U", "N", "OWEN"):
                for recipient in ("Cloud", "Barret", "Red XIII", "Cid", "Vincent", "Tifa", "Yuffie", "Cait Sith", "Aerith"):
                    message: BccMessage = BccMessage(content=content, sender_id=sender, recipient_id=recipient)

                    self.assertEqual(content, message.get_content())
                    self.assertEqual(sender, message.get_sender_id())
                    self.assertEqual(len(message.get_recipients_ids()), 1)
                    self.assertIn(recipient, message.get_recipients_ids())


if __name__ == "__main__":
    main()
