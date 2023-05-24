from typing import Dict, Type

from .vwrunner import VWRunner
from ..common.vwcolour import VWColour
from ..model.actor.mind.surrogate.vwactor_mind_surrogate import VWActorMindSurrogate


class VWUnityRunner(VWRunner):
    def __init__(self, config: dict, minds: Dict[VWColour, VWActorMindSurrogate], allowed_args: Dict[str, Type], **kwargs) -> None:
        '''
        The VWUnityRunner is a VWRunner that runs VacuumWorld in with a Unity GUI.

        Args:

            config (dict): The configuration for the VWEnvironment.

            minds (Dict[VWColour, VWActorMindSurrogate]): The minds for the VWEnvironment, one for each VWColour.

            allowed_args (Dict[str, Type]): The allowed arguments for the VWEnvironment (names and types).

            **kwargs: keyword arguments.
        '''
        super(VWUnityRunner, self).__init__(config=config, minds=minds, allowed_args=allowed_args, **kwargs)

        raise NotImplementedError("Not yet implemented.")

    def run(self) -> None:
        '''
            1) Create a new empty `VWEnvironment` named `env` via `VWEnvironment.generate_empty_env(config, forced_line_dim)`.
            2) Create the Unity GUI, allowing for:
                - The user to modify the `VWEnvironment` via drag/drop on the GUI.
                - The user to load a `VWEnvironment` from a JSON file, (which then needs to be validated and replace the current `env`).
                - The user to save the current `VWEnvironment` to a JSON file.
            3) Loop:
                - Call `env.evolve()`.
                - Update the Unity GUI fetching the data with the VWEnvironment and VWAmbient API.
        '''
        raise NotImplementedError("Not yet implemented.")
