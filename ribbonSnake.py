import random
from snake import *

# Barva glave in repa
COLOR_HEAD = 'blue'
COLOR_TAIL = 'red'

class RibbonSnake(Snake):
    def __init__(self, field, x, y, dx, dy):
        # Poklicemo konstruktor nadrazreda
        Snake.__init__(self,
            field = field,
            color_head = COLOR_HEAD,
            color_tail = COLOR_TAIL,
            x = x, y = y, dx = dx, dy = dy)
        # V konstruktor lahko dodate se kaksne atribute
    def distance(self, p, q):
        xp, yp = p 
        xq, yq = q
        return abs(xp-xq) + abs(yp-yq)
    
    def get_direction(self,dx, dy):
        if dx == 1:
            return 0
        if dx == -1:
            return 2
        if dy == 1:
            return 1
        return 3
    
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
        goal = None
        for x in range(1, self.field.width - 1):
            for y in range(1, self.field.height - 1):
                if goal is None or (self.distance((x,y), self.coords[0]) < self.distance(goal, self.coords[0])):
                    goal = (x,y)
        if goal is None:
            return
##                    if yh<y:
##                        self.dy=1
##                        if xh<x:
##	                        self.dx=1
##                        elif xh==x:
##	                        self.dx=0
##                        elif xh>x:
##	                        self.dx=-1
##                    elif yh==y:
##                        self.dy=0
##                        if xh<x:
##	                        self.dx=1
##                        elif xh==x:
##	                        self.dx=0
##                        elif xh>x:
##	                        self.dx=-1
##                    elif yh>y:
##                        self.dy=-1
##                        if xh<x:
##	                        self.dx=1
##                        elif xh==x:
##	                        self.dx=0
##                        elif xh>x:
##	                        self.dx=-1
        head = self.coords[0]
        my_dir = self.get_direction(self.dx, self.dy)                    
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

        if my_dir in good_dir:
            return
            
        if (my_dir + 1) % 4 in good_dir:
            self.turn_left()
            return
            
        if (my_dir - 1) % 4 in good_dir:
            self.turn_right()
            return
        
        if random.randint(0,1) == 1:
            self.turn_left()
        else:
            self.turn_right()
        
        
        
        
        
        
        
        
        
