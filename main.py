from tkinter import Tk, Canvas
from conway import Board


class TkBoard(Board):

    BORDER_WIDTH = 1
    CELL_SIZE = 20
    UPDATE_KEY_TK = '<space>'
    UPADTE_KEY_VERBOSE = 'Spacebar'
    ALIVE_COLOUR = 'black'
    DEAD_COLOUR = 'white'

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.drawing = False
        self.erasing = False

        self.window = Tk()
        self.window.title(
            "John Conway's Game of Life. "
            f"Press {self.UPADTE_KEY_VERBOSE} to simulate."
        )
        self.window.resizable(False, False)
        self.window.bind(self.UPDATE_KEY_TK, self.update)
        self.canvas = Canvas(
            self.window,
            height=self.HEIGHT * self.CELL_SIZE,
            width=self.WIDTH * self.CELL_SIZE,
        )
        self.canvas.bind('<ButtonPress-1>', self.on_pressed)
        self.canvas.bind('<ButtonRelease-1>', self.on_released)
        self.canvas.bind('<B1-Motion>', self.on_motion)
        self.draw_board()

    def get_2d_index(self, canvas_index):

        flat_index = canvas_index[0] - 1
        return flat_index // self.WIDTH, flat_index % self.WIDTH

    def get_canvas_index(self, x, y):

        return (x * self.WIDTH + y + 1,)

    def on_pressed(self, event):

        canvas_index = self.canvas.find_closest(event.x, event.y)
        index_2d = self.get_2d_index(canvas_index)
        if index_2d in self.alive_cells:
            self.erasing = True
        else:
            self.drawing = True

        self.on_motion(event, canvas_index)

    def on_released(self, event):

        self.drawing = self.erasing = False

    def on_motion(self, event, canvas_index=None):

        if self.drawing or self.erasing:
            if canvas_index is None:
                canvas_index = self.canvas.find_closest(event.x, event.y)

            index_2d = self.get_2d_index(canvas_index)

            if self.drawing:
                self.canvas.itemconfig(canvas_index, fill=self.ALIVE_COLOUR)
                self.alive_cells.add(index_2d)
            elif self.erasing:
                self.canvas.itemconfig(canvas_index, fill=self.DEAD_COLOUR)
                self.alive_cells.discard(index_2d)

    def draw_board(self):

        _size = self.CELL_SIZE
        _offset = self.BORDER_WIDTH + 1

        for x in range(self.HEIGHT):
            for y in range(self.WIDTH):

                colour = self.ALIVE_COLOUR \
                    if (x, y) in self.alive_cells \
                    else self.DEAD_COLOUR



                self.canvas.create_rectangle(
                    _size * y + 2, _size * x + 2,
                    _size * (y+1) + 2, _size * (x+1) + 2,
                    fill=colour, width=_offset
                )

        self.canvas.pack()

    def update(self, event, *args, **kwargs):

        old_state = self.alive_cells.copy()
        super().update(*args, **kwargs)
        for x in range(self.HEIGHT):
            for y in range(self.WIDTH):
                index = (x, y)
                if (index in old_state) != (index in self.alive_cells):
                    self.canvas.itemconfig(
                        self.get_canvas_index(x, y),
                        fill=self.ALIVE_COLOUR if index in self.alive_cells
                        else self.DEAD_COLOUR
                    )

    def mainloop(self):

        self.window.mainloop()

if __name__ == '__main__':

    TkBoard(20, 40).mainloop()
