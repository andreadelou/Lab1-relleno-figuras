import struct
from obj import Obj
from Vector import *

def char(c):
    # 1 byte
  return struct.pack('=c', c.encode('ascii'))


def word(w):
    # 2 bytes
    return struct.pack('=h', w)

def dword(d):
    # 4 bytes
    return struct.pack('=l',d)


def color(r,g,b):
    # Creacion de Color (255 deja usar todos los colores)
    return bytes([int(b*255),
                int(g*255),
                int(r*255)])



class Render(object):
    # Constructor
    def __init__(self):
        self.viewPortX = 0
        self.viewPortY = 0
        self.height = 0
        self.width = 0
        self.clearColor = color(0, 0, 0)

        self.current_color = color(1, 1, 1)
        self.framebuffer = []
       
        self.glViewport(0,0,self.width, self.height)
        self.glClear() 

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()

    def glViewport(self, x, y, width, height):
        self.viewpx = x
        self.viewpy = y
        self.viewpwidth = width
        self.viewpheight = height
    
    def glClear(self):
        self.framebuffer = [[self.clearColor for x in range(self.width+1)]
                            for y in range(self.height+1)]

    def glClearColor(self, r, g, b):
        self.clearColor = color(r, b, g)
        self.glClear()

    def glColor(self, r, g, b):
        self.current_color = color(r, g, b)

    def glPoint(self, x, y, color):
      self.framebuffer[int(round((x+1) * self.width / 2))][int(round((y+1) * self.height / 2))] = color

    def glFill(self, polygon):
      for y in range(self.height):
          for x in range(self.width):
              i = 0
              j = len(polygon) - 1
              draw_point = False
              for i in range(len(polygon)):
                  if (polygon[i][1] < y and polygon[j][1] >= y) or (polygon[j][1] < y and polygon[i][1] >= y):
                      if polygon[i][0] + (y - polygon[i][1]) / (polygon[j][1] - polygon[i][1]) * (polygon[j][0] - polygon[i][0]) < x:
                          draw_point = not draw_point
                  j = i
              if draw_point:
                  self.glPoint((float(x)/(float(self.width)/2))-1,(float(y)/(float(self.height)/2))-1,self.current_color)
                    
    # Función para crear la imagen
    def glFinish(self, filename):
        with open(filename, 'bw') as file:
            # Header
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))

            # file size
            file.write(dword(14 + 40 + self.height * self.width * 3))
            file.write(dword(0))
            file.write(dword(14 + 40))

            # Info Header
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # Color table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.framebuffer[x][y])
            file.close()
      

  
w = 1000
h = 1000
rend = Render()
rend.glCreateWindow(w, h)

rend.glViewport(int(0),
                int(0), 
                int(w/1), 
                int(h/1))

rend.glClear()

#poligono1: estrella
#color
rend.glColor(1, 0.93, 0.25)
polygon1 = ((165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383))
rend.glFill(polygon1)

#poligono3: cuadrado
#color
rend.glColor(0.5, 0.2, 0.87)
polygon2 = ((321, 335), (288, 286), (339, 251), (374, 302))
rend.glFill(polygon2)

#poligono3: triangulo
#color
rend.glColor(0.3, 0.1, 0.26)
polygon3 = ((377, 249), (411, 197), (436, 249))
rend.glFill(polygon3)


#poligono4: tetera
#color
rend.glColor(0.2,0.7,1)
polygon4 = ((413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52), (750, 145), (761, 179), (672, 192), (659, 214), (615, 214), (632, 230), (580, 230), (597, 215), (552, 214), (517, 144), (466, 180))
rend.glFill(polygon4)

#poligono4: hoyo tetera
#color
rend.glColor(0, 0, 0)
polygon5 = ((682, 175), (708, 120), (735, 148), (739, 170))
rend.glFill(polygon5)

rend.glFinish("a.bmp")