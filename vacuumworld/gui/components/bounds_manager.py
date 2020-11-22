class BoundsManager():
    def __init__(self, config: dict) -> None:
        self.__config: dict = config

    def in_bounds(self, x: int, y: int) -> bool:
        return x < self.__config["grid_size"] and x > 0 and y < self.__config["grid_size"] and y > 0
