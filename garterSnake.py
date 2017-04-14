import random
from snake import *

# Barva glave in repa
COLOR_HEAD = 'green'
COLOR_TAIL = 'orange'

class GarterSnake(Snake):
    def __init__(self, field, x, y, dx, dy):
        # Poklicemo konstruktor nadrazreda
        Snake.__init__(self,
            field = field,
            color_head = COLOR_HEAD,
            color_tail = COLOR_TAIL,
            x = x, y = y, dx = dx, dy = dy)
        # V konstruktor lahko dodate se kaksne atribute

    def turn(self):
        """Igrica poklice metodo turn vsakic, preden premakne kaco. Kaca naj se tu odloci, ali se
           bo obrnila v levo, v desno, ali pa bo nadaljevala pot v isti smeri.

           * v levo se obrne s self.turn_left()
           * v desno se obrne s self.turn_right()
           * koordinate glave so self.coords[0]
           * smer, v katero potuje je (self.dx, self.dy)
           * spisek koordinat vseh misk je self.field.mice.keys()
           * spisek vseh kac je self.field.snakes
        """
        xh, yh = self.coords[0]
        goal = (1, 1)
        for x in range(1, self.field.height - 1):
            for y in range(1, self.field.height - 1):
                if self.field.is_mouse(x,y):
                   if distance((x,y), self.coords[0]) < distance(goal, self.coords[0]):
                       goal = (x,y)

         if goal is None:
             return

         head = self.coords[0]
         my_dir = get.direction(self.dx, self.dy)
         good_dir = []
         x_delta = goal[0] - head[0]
         y_delta = goal[1] - head[1]
         if x_delta > 0:
             good_dir.append(0)
         elif x_delta < 0:
             good_dir.append(2)
         if y_delta > 0:
             good_dir.append(1)
         elif y_delta < 0:
             good_dir.append(3)

         if my_dir is good_dir:
             return
   
        if (my_dir + 1) % 4 in good_dir:
            self.turn_left()
            return
   
        if random.randint(0,1)==1:
            self.turn_left()
        else:
            self.turn_right()
            

   
        """ if random.randint(0,10) < 5:
            if random.randint(0,1) == 1:
                self.turn_left()
            else:
                self.turn_right() """
