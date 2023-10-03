class VWActionEffort():
    '''
    This class specifies the effort of each kind of `VWAction`.

    The effort of a kind `VWAction` is an `int` number that specifies how intensive such kind `VWAction` is to attempt.
    '''
    __DEFAULT_EFFORTS: dict[str, int] = {
        "VWBroadcastAction": 1,
        "VWCleanAction": 1,
        "VWDropAction": 1,
        "VWIdleAction": 1,
        "VWMoveAction": 1,
        "VWSpeakAction": 1,
        "VWTurnAction": 1
    }

    REASONABLE_EFFORTS: dict[str, int] = {
        "VWBroadcastAction": 5,  # Broadcasting is a costly operation, and needs to be used strategically.
        "VWCleanAction": 1,  # Not 0, because we want to discourage any unnecessary attempt.
        "VWDropAction": 1,  # Does not really matter for cleaning agents.
        "VWIdleAction": 1,  # Not 0, because we want to discourage any unnecessary loss of time.
        "VWMoveAction": 3,  # Moving is a somewhat costly operation, and needs to be used strategically.
        "VWSpeakAction": 2,  # Speaking is a mildly costly operation, and must not be abused. If the speech is broadcasted, the effort becomes higher.
        "VWTurnAction": 5  # We want to discourage any unnecessary turns.
    }

    EFFORTS: dict[str, int] = __DEFAULT_EFFORTS
    DEFAULT_EFFORT_FOR_OTHER_ACTIONS: int = 1

    @staticmethod
    def override_default_effort_for_action(action_name: str, new_effort: int) -> None:
        '''
        Overrides the default effort of the specified `action_name` with the specified `new_effort`.

        If the specified `action_name` is not a valid `VWAction` name, then nothing happens.

        This method assumes (via assertion) that `action_name` is a `str`, and `new_effort` is an `int`.
        '''
        assert isinstance(action_name, str) and isinstance(new_effort, int)

        if action_name in VWActionEffort.EFFORTS:
            VWActionEffort.EFFORTS[action_name] = new_effort
