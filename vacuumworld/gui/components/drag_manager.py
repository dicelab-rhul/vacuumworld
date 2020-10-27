class CanvasDragManager():
    def __init__(self, config, key, grid, canvas, item, on_start, on_drop):
        self.__config: dict = config
        self.x = 0
        self.y = 0
        self.canvas = canvas

        self._on_start = on_start
        self._on_drop = on_drop
        self.canvas.tag_bind(item, "<ButtonPress-1>", self.on_start)
        self.canvas.tag_bind(item, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(item, "<ButtonRelease-1>", self.on_drop)

        self.key = key
        self.drag_image = None
        self.drag = None
        self.dragging = False
        self.grid = grid

    def on_start(self, event):
        if not self.dragging:
            self._on_start(event)
            self.dragging = True
            self.x = event.x
            self.y = event.y

    def on_drag(self, event):
        inc = self.__config["grid_size"] / self.grid.dim
        x = int(event.x / inc) * inc + (inc / 2) + 1
        y = int(event.y / inc) * inc + (inc / 2) + 1

        if event.x < 0 or event.y < 0:
            self.canvas.itemconfigure(self.drag, state="hidden")
        elif x <= self.__config["grid_size"] and y <= self.__config["grid_size"]:
            self.canvas.itemconfigure(self.drag, state="normal")
        
        # To prevent unnecessary re-renderings.
        if x != self.x or y != self.y:
            dx = x - self.x
            dy = y - self.y
            self.canvas.move(self.drag, dx, dy)
            self.x = x
            self.y = y

    def on_drop(self, event):
        if self.in_bounds(event.x, event.y):
            self._on_drop(event, self)
        self.dragging = False


    def in_bounds(self, x, y) -> bool:
        return x < self.__config["grid_size"] and x > 0 and y < self.__config["grid_size"] and y > 0
