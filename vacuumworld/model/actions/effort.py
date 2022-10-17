from typing import Dict


class ActionEffort():
    __DEFAULT_EFFORTS: Dict[str, int] = {
        "VWBroadcastAction": 1,
        "VWCleanAction": 1,
        "VWDropAction": 1,
        "VWIdleAction": 1,
        "VWMoveAction": 1,
        "VWSpeakAction": 1,
        "VWTurnAction": 1
    }

    REASONABLE_EFFORTS: Dict[str, int] = {
        "VWBroadcastAction": 5,  # Broadcasting is a costly operation, and needs to be used strategically.
        "VWCleanAction": 1,  # Not 0, because we want to discourage any unnecessary attempt.
        "VWDropAction": 1,  # Does not really matter for cleaning agents.
        "VWIdleAction": 1,  # Not 0, because we want to discourage any unnecessary loss of time.
        "VWMoveAction": 3,  # Moving is a somewhat costly operation, and needs to be used strategically.
        "VWSpeakAction": 2,  # Speaking is a mildly costly operation, and must not be abused. If the speech is broadcasted, the effort becomes higher.
        "VWTurnAction": 5  # We want to discourage any unnecessary turns.
    }

    EFFORTS: Dict[str, int] = __DEFAULT_EFFORTS
    DEFAULT_EFFORT_FOR_OTHER_ACTIONS: int = 1

    @staticmethod
    def override_default_effort_for_action(action_name: str, new_effort: int) -> None:
        assert type(action_name) == str and type(new_effort) == int

        if action_name in ActionEffort.EFFORTS:
            ActionEffort.EFFORTS[action_name] = new_effort
