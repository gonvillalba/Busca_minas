from tkinter import Button, Label
import random
import settings
import ctypes
import sys


class Cell:
    all = []
    cell_count_label_obj = None
    mine_count_label_obj = None
    cell_count = settings.CELL_COUNT
    mine_count = settings.MINES

    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_open = False
        self.is_marked = False
        self.cell_btn_obj = None
        self.x = x
        self.y = y

        # Append the objects to the list
        Cell.all.append(self)

    def create_btn_obj(self, location):
        btn = Button(location, width=12, height=4)
        btn.bind("<Button-1>", self.left_click_actions)  # left click
        btn.bind("<Button-3>", self.right_click_actions)  # rigth click

        self.cell_btn_obj = btn

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg="black",
            fg="white",
            text=f"Celdas restantes: {Cell.cell_count}",
            font=("", 12),
        )
        Cell.cell_count_label_obj = lbl

    @staticmethod
    def create_mine_count_label(location):
        lbl = Label(
            location,
            bg="black",
            fg="white",
            text=f"Minas restantes: {Cell.mine_count}",
            font=("", 12),
        )
        Cell.mine_count_label_obj = lbl

    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()

        else:
            if self.count_mines() == 0:
                # print("Presionar vecinos")
                for cell in self.sourronded_cells():
                    cell.number_mines()

            self.number_mines()

        # Si se llega a la condicion que la cantidad de celdas restantes es igual a las minas se gana el juego
        if Cell.cell_count == settings.MINES:
            ctypes.windll.user32.MessageBoxW(0, "Ganaste el juego!", "Felicidades!", 0)
            sys.exit()
            pass

    def right_click_actions(self, event):
        if self.is_marked and Cell.mine_count < 9 and not self.is_open:
            Cell.mine_count += 1
            Cell.mine_count_label_obj.configure(
                text=f"Minas restantes: {Cell.mine_count}"
            )
            self.cell_btn_obj.configure(bg="systemButtonFace")
            self.is_marked = False
        elif not self.is_marked and Cell.mine_count > 0 and not self.is_open:
            Cell.mine_count -= 1
            Cell.mine_count_label_obj.configure(
                text=f"Minas restantes: {Cell.mine_count}"
            )
            self.cell_btn_obj.configure(bg="yellow")
            self.is_marked = True

    @staticmethod
    def random_mines():
        picked_cells = random.sample(Cell.all, settings.MINES)
        for row in picked_cells:
            row.is_mine = True
            # print(row)

    def __repr__(self):
        return f"Cell({self.x},{self.y})"

    def number_mines(self):
        if not self.is_open:
            number = self.count_mines()
            self.cell_btn_obj.configure(text=number)
            # Verifica el Label y actualiza cada vez que se toca una celda
            if Cell.cell_count_label_obj:
                Cell.cell_count -= 1
                Cell.cell_count_label_obj.configure(
                    text=f"Celdas restantes: {Cell.cell_count}"
                )
        self.cell_btn_obj.configure(bg="systemButtonFace")
        # Marca la celda como abierta cuando se muestra el numero de minas a su alrededor
        self.is_open = True

    def count_mines(self):
        number = 0
        cells = self.sourronded_cells()
        for cell in cells:
            if cell.is_mine:
                number += 1
        return number

    def sourronded_cells(self):
        cells = []
        for row in range(3):
            for column in range(3):
                x_cell = row + self.x - 1
                y_cell = column + self.y - 1
                # print(x_cell, y_cell)
                # verifica que sea una celda valida
                if x_cell >= 0 and y_cell >= 0:
                    # Busca una celda por coordenadas y verifica que sea una mina
                    cell = self._find_cell(x_cell, y_cell)
                    if cell is not None:
                        cells.append(cell)
        # print(cells)
        return cells

    def _find_cell(self, x, y):
        for cell in Cell.all:
            # print(x, y, cell)
            if cell.x == x and cell.y == y:
                # print(cell.is_mine)
                return cell

    def show_mine(self):
        self.cell_btn_obj.configure(bg="red")
        ctypes.windll.user32.MessageBoxW(0, "Tocaste una mina", "Game Over", 0)
        sys.exit()
