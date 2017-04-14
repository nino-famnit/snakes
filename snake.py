# -*- encoding: utf-8 -*-

import random

# Igralno polje sestoji iz mreze kvadratkov (blokov)
WIDTH = 50  # sirina polja (stevilo blokov)
HEIGHT = 30 # visina polja
BLOCK = 20  # velikost enega bloka v tockah na zaslonu

# Pomozne funkcije

def brick(canvas, x, y):
    """Ustvari graficni element, ki predstavlja opeko (na robu polja)."""
    return canvas.create_rectangle(x*BLOCK, y*BLOCK, (x+1)*BLOCK, (y+1)*BLOCK,
                                   fill='brown', width=2)
def mouse(canvas, x, y):
    """Ustvari graficni element, ki predstavlja misko."""
    return canvas.create_oval(x*BLOCK+2, y*BLOCK+2, (x+1)*BLOCK-2, (y+1)*BLOCK-2,
                              fill = 'black')

# Razredi

class Snake():
    """Razred, ki predstavlja kaco.
       Vse kace v igrici so podrazredi tega razreda. Objekt razreda Snake
       ima naslednje atribute:

       field       --  objekt razreda Field, v katerem je kaca
       (dx, dy)    --  smerni vektor premikanja, eden od (-1,0), (1,0), (0,-1), (0,1)
       grow        --  za koliko clenkov mora kaca zrasti
       color_head  --  barva glave
       color_tail  --  barva repa
       coords      --  seznam koordinat clenkov kace (glava je coords[0])
       cells       --  seznam graficnih elementov, ki predstavljajo kaco
    """

    def __init__(self, field, color_head, color_tail, x, y, dx, dy):
        self.field = field
        self.dx = dx
        self.dy = dy
        self.grow = 0
        self.color_head = color_head
        self.color_tail = color_tail
        self.coords = []
        self.cells = []
        # the tail
        for k in range(2, 0, -1):
            self.add_cell(x - k * self.dx, y - k * self.dy)
        self.add_cell(x, y) # the head

    def add_cell(self, x, y):
        """Dodaj kaci novo celico."""
        cell = self.field.canvas.create_oval(
            x*BLOCK, y*BLOCK, (x+1)*BLOCK, (y+1)*BLOCK, fill = self.color_head)
        if len(self.cells) > 0:
                self.field.canvas.itemconfigure(self.cells[0], fill=self.color_tail)
        self.coords.insert(0, (x, y))
        self.cells.insert(0, cell)
                        

    def turn_left(self):
        """Obrni kaco v levo."""
        (self.dx, self.dy) = (-self.dy, self.dx)

    def turn_right(self):
        """Obrni kaco v desno."""
        (self.dx, self.dy) = (self.dy, -self.dx)
            
    def move(self):
        """Premakni kaco v smer, v katero je obrnjena.
           Ce je na polju, kamor se premaknemo, miska, jo pojemo.
           Ce je polje zasedeno z drugo kaco ali opeko, se ne zgodi nic."""
        (x,y) = self.coords[0]
        x += self.dx
        y += self.dy
        if self.field.is_mouse(x,y):
            self.grow = 1
            self.field.remove_mouse(x,y)
        if self.field.is_empty(x,y):
            if self.grow > 0:
                self.grow -= 1
                self.add_cell(x, y)
            else:
                # Reuse the last one
                self.coords.pop()
                self.coords.insert(0, (x,y))
                self.field.canvas.itemconfigure(self.cells[0], fill=self.color_tail)
                cell = self.cells.pop()
                self.field.canvas.coords(cell, x*BLOCK, y*BLOCK, (x+1)*BLOCK, (y+1)*BLOCK)
                self.field.canvas.itemconfigure(cell, fill=self.color_head)
                self.cells.insert(0, cell)

    def turn(self):
        """Po potrebi obrni kaco.
           Ta funkcija ne dela nicesar in jo je treba redefinirati v podrazredu,
           ki predstavlja kaco, glej prilozene primere."""
        pass

                
class Field():
    """Igralno polje, po katerem se gibljejo kace.
       Atributi:

       width  -- sirina polja
       height -- visina polja
       snakes -- seznam kac, ki so v polju
       mice   -- slovar, ki slika koordinate misk v id-je pripadajocih graficnih objektov
    """

    def __init__(self, canvas, width, height):
        self.width = width
        self.height = height
        self.canvas = canvas
        self.snakes = []
        self.mice = {}
        self.bricks = []
        # The bricks
        for i in range(width):
            self.bricks.append(brick(canvas, i, 0))
            self.bricks.append(brick(canvas, i, height-1))
        for j in range(1, height-1):
            self.bricks.append(brick(canvas, 0, j))
            self.bricks.append(brick(canvas, width-1, j))

    def add_snake(self, s):
        """Dodaj novo kaco v polje."""
        s.id = len(self.snakes)
        self.snakes.append(s)
    
    def is_mouse(self, x, y):
        """Ali je na lokaciji (x,y) miska?"""
        return (0 < x < self.width-1 and
                0 < y < self.height-1 and
                (x,y) in self.mice)
    
    def is_empty(self, x, y):
        """Ali je polje (x,y) prazno?"""
        if (0 < x < self.width-1 and
            0 < y < self.height-1 and
            (x,y) not in self.mice):
            for s in self.snakes:
                if (x,y) in s.coords: return False
            return True
        else:
            return False
                            
    def find_empty(self):
        """Nakljucno izberi prazno polje, poskusi najvec petkrat."""
        for i in range(5):
            x = random.randint(1, self.width-2)
            y = random.randint(1, self.height-2)
            if self.is_empty(x, y):
                return (x,y)
        return (None, None)

    def new_mouse(self):
        """Dodaj misko na nakljucno izbrano polje."""
        (x,y) = self.find_empty()
        if x and y:
            self.mice[(x,y)] = mouse(self.canvas, x, y)

    def remove_mouse(self, x, y):
        """Odstrani misko na lokaciji (x,y)."""
        m = self.mice.get((x,y))
        if m:
            self.canvas.delete(m)
            del self.mice[(x,y)]
