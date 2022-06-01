from tkinter import *
from cell import Cell
import settings
import utils


root = Tk()
root.configure(bg="blue")
root.geometry(f"{settings.WIDTH}x{settings.HEIGHT}")
root.title("Busca Minas")
root.resizable(False, False)

top_frame = Frame(root, bg="black", width=settings.WIDTH, height=utils.height_perct(25))
top_frame.place(x=0, y=0)

game_title = Label(top_frame, bg="black", fg="white", text="Busca Minas", font=("", 48))
game_title.place(x=utils.width_perct(25), y=0)

left_frame = Frame(
    root, bg="black", width=utils.width_perct(25), height=utils.height_perct(75)
)
left_frame.place(x=0, y=utils.height_perct(25))

center_frame = Frame(
    root, bg="black", width=utils.width_perct(75), height=utils.height_perct(75)
)
center_frame.place(x=utils.width_perct(25), y=utils.height_perct(25))

for x in range(settings.GRID_SIZE):
    for y in range(settings.GRID_SIZE):
        c = Cell(x, y)
        c.create_btn_obj(center_frame)
        c.cell_btn_obj.grid(column=x, row=y)

Cell.create_cell_count_label(left_frame)
Cell.cell_count_label_obj.place(x=0, y=0)

Cell.create_mine_count_label(left_frame)
Cell.mine_count_label_obj.place(x=0, y=50)

Cell.random_mines()

root.mainloop()
