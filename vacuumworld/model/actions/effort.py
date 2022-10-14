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

    EFFORTS: Dict[str, int] = __DEFAULT_EFFORTS
    DEFAULT_EFFORT_FOR_OTHER_ACTIONS: int = 1

    @staticmethod
    def override_default_effort_for_action(action_name: str, new_effort: int) -> None:
        assert type(action_name) == str and type(new_effort) == int

        if action_name in ActionEffort.EFFORTS:
            ActionEffort.EFFORTS[action_name] = new_effort
