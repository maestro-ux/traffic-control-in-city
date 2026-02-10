from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from math import cos, sin, pi
import random


#               GLOBAL VARIABLES 



signal_h = 2
signal_v = 0
is_day = True
time = 0.0



#                Horizontal vehicles (left → right)


cars = [
    {"x": -1.8, "y": -0.06, "speed": 0.014, "color": (0.9,0.1,0.1)},
    {"x": -2.2, "y": 0.02,  "speed": 0.012, "color": (0.1,0.6,0.9)},
    {"x": -2.6, "y": -0.13, "speed": 0.01,  "color": (0.2,0.8,0.3)},
    {"x": -3.0, "y": 0.09,  "speed": 0.011, "color": (0.9,0.7,0.2)}
]

#                Vertical vehicles (both directions)


cars_v = [
    {"x": -0.06, "y": -1.0, "speed": 0.012, "dir": 1, "color": (0.8,0.2,0.2)},
    {"x":  0.06, "y":  1.0, "speed": 0.011, "dir": -1, "color": (0.2,0.8,0.2)}
]

#   stars with movement


stars = []
for _ in range(120):
    stars.append({
        "x": random.uniform(-1.0, 1.0),
        "y": random.uniform(0.35, 1.0),
        "size": random.uniform(0.004, 0.014),
        "base_brightness": random.uniform(0.5, 1.0),
        "phase": random.uniform(0, 2*pi),
        "dx": random.uniform(-0.0008, 0.0008)
    })



#              BASIC SHAPE 



def draw_circle(x, y, r):
    glBegin(GL_POLYGON)
    for i in range(100):
        a = 2 * pi * i / 100
        glVertex2f(x + r*cos(a), y + r*sin(a))
    glEnd()



#              TREE 

def draw_tree(x, y, scale=1.0):
    glColor3f(0.38, 0.22, 0.10)
    glBegin(GL_QUADS)
    glVertex2f(x - 0.025*scale, y)
    glVertex2f(x + 0.025*scale, y)
    glVertex2f(x + 0.025*scale, y + 0.16*scale)
    glVertex2f(x - 0.025*scale, y + 0.16*scale)
    glEnd()

    glColor3f(0.14, 0.52, 0.10) if is_day else glColor3f(0.10, 0.38, 0.08)
    draw_circle(x, y + 0.26*scale, 0.10*scale)
    draw_circle(x - 0.05*scale, y + 0.18*scale, 0.08*scale)
    draw_circle(x + 0.05*scale, y + 0.18*scale, 0.08*scale)
    draw_circle(x, y + 0.36*scale, 0.09*scale)



#           ROADS 


def draw_roads():
    glColor3f(0.13, 0.13, 0.13)

    glBegin(GL_QUADS)
    glVertex2f(-1.0, -0.20)
    glVertex2f(1.0, -0.20)
    glVertex2f(1.0, 0.20)
    glVertex2f(-1.0, 0.20)
    glEnd()

    glBegin(GL_QUADS)
    glVertex2f(-0.20, -1.0)
    glVertex2f(0.20, -1.0)
    glVertex2f(0.20, 1.0)
    glVertex2f(-0.20, 1.0)
    glEnd()

    glColor3f(0.98, 0.94, 0.60)
    for i in range(-40, 41, 4):
        y = i * 0.07
        glBegin(GL_QUADS)
        glVertex2f(-0.014, y)
        glVertex2f(-0.014, y + 0.045)
        glVertex2f(0.014, y + 0.045)
        glVertex2f(0.014, y)
        glEnd()

    glColor3f(0.92, 0.92, 0.92)
    glLineWidth(3.0)
    glBegin(GL_LINES)
    glVertex2f(-1.0, -0.20); glVertex2f(1.0, -0.20)
    glVertex2f(-1.0, 0.20); glVertex2f(1.0, 0.20)
    glVertex2f(-0.20, -1.0); glVertex2f(-0.20, 1.0)
    glVertex2f(0.20, -1.0); glVertex2f(0.20, 1.0)
    glEnd()
    glLineWidth(1.0)

    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glVertex2f(-0.18, -0.24); glVertex2f(0.18, -0.24)
    glVertex2f(0.18, -0.20);  glVertex2f(-0.18, -0.20)
    glVertex2f(-0.18, 0.20);  glVertex2f(0.18, 0.20)
    glVertex2f(0.18, 0.24);   glVertex2f(-0.18, 0.24)
    glEnd()



#                 FOOTPATH 


def draw_footpath():
    glColor3f(0.78,0.78,0.78)
    glBegin(GL_QUADS)
    glVertex2f(-1, 0.20); glVertex2f(1, 0.20); glVertex2f(1, 0.28); glVertex2f(-1, 0.28)
    glVertex2f(-1, -0.28); glVertex2f(1, -0.28); glVertex2f(1, -0.20); glVertex2f(-1, -0.20)
    glEnd()



#        ROAD MARKINGS + ZEBRA CROSSING


def draw_markings():
    glColor3f(1,1,1)

    for i in range(-12,13):
        glBegin(GL_QUADS)
        glVertex2f(i*0.1 - 0.025, -0.008)
        glVertex2f(i*0.1 + 0.025, -0.008)
        glVertex2f(i*0.1 + 0.025,  0.008)
        glVertex2f(i*0.1 - 0.025,  0.008)
        glEnd()

    stripe_w = 0.045
    gap = 0.025

    for i in range(9):
        x = -0.18 + i*(stripe_w + gap)
        if x > 0.18 - stripe_w: break
        glBegin(GL_QUADS)
        glVertex2f(x, -0.28); glVertex2f(x + stripe_w, -0.28)
        glVertex2f(x + stripe_w, -0.20); glVertex2f(x, -0.20)
        glEnd()

        glBegin(GL_QUADS)
        glVertex2f(x, 0.20); glVertex2f(x + stripe_w, 0.20)
        glVertex2f(x + stripe_w, 0.28); glVertex2f(x, 0.28)
        glEnd()

    for i in range(9):
        y = -0.18 + i*(stripe_w + gap)
        if y > 0.18 - stripe_w: break
        glBegin(GL_QUADS)
        glVertex2f(-0.28, y); glVertex2f(-0.20, y)
        glVertex2f(-0.20, y + stripe_w); glVertex2f(-0.28, y + stripe_w)
        glEnd()

        glBegin(GL_QUADS)
        glVertex2f(0.20, y); glVertex2f(0.28, y)
        glVertex2f(0.28, y + stripe_w); glVertex2f(0.20, y + stripe_w)
        glEnd()



#            FOR  BUILDINGS 



def building(x,y,w,h,color):
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x,y); glVertex2f(x+w,y); glVertex2f(x+w,y+h); glVertex2f(x,y+h)
    glEnd()

    glColor3f(color[0]*0.82, color[1]*0.82, color[2]*0.82)
    glBegin(GL_QUADS)
    glVertex2f(x,y+h); glVertex2f(x+w,y+h)
    glVertex2f(x+w,y+h+0.05); glVertex2f(x,y+h+0.05)
    glEnd()

    glColor3f(1,1,0.65 if not is_day else 0.92)
    for i in range(4):
        for j in range(4):
            wx = x + 0.045 + i*0.055
            wy = y + 0.065 + j*0.09
            glBegin(GL_QUADS)
            glVertex2f(wx, wy); glVertex2f(wx+0.035, wy)
            glVertex2f(wx+0.035, wy+0.07); glVertex2f(wx, wy+0.07)
            glEnd()


def draw_city():
    building(-0.95,0.32,0.28,0.6,(0.6,0.7,0.9))
    building(-0.6,0.32,0.25,0.5,(0.8,0.6,0.6))
    building(0.5,0.32,0.3,0.65,(0.6,0.8,0.6))
    building(-0.9,-0.95,0.35,0.45,(0.7,0.7,0.5))
    building(0.55,-0.9,0.35,0.5,(0.6,0.6,0.8))

#            FOR STREET LIGHT



def street_light(x,y):
    glColor3f(0.22,0.22,0.22)
    glBegin(GL_QUADS)
    glVertex2f(x-0.012,y); glVertex2f(x+0.012,y)
    glVertex2f(x+0.012,y+0.38); glVertex2f(x-0.012,y+0.38)
    glEnd()

    glColor3f(0.32,0.32,0.32)
    glBegin(GL_QUADS)
    glVertex2f(x-0.055,y+0.38); glVertex2f(x+0.055,y+0.38)
    glVertex2f(x+0.055,y+0.42); glVertex2f(x-0.055,y+0.42)
    glEnd()

    if not is_day:
        glColor3f(1.0, 0.98, 0.75)
        draw_circle(x, y+0.46, 0.055)

#     FOR  SIGNAL 
def draw_signal(x,y):
    glColor3f(0.05,0.05,0.05)
    glBegin(GL_QUADS)
    glVertex2f(x,y); glVertex2f(x+0.09,y)
    glVertex2f(x+0.09,y+0.32); glVertex2f(x,y+0.32)
    glEnd()

    glColor3f(1,0,0) if signal_h==0 or signal_v==0 else glColor3f(0.3,0,0)
    draw_circle(x+0.045,y+0.26,0.028)
    glColor3f(1,1,0) if signal_h==1 or signal_v==1 else glColor3f(0.3,0.3,0)
    draw_circle(x+0.045,y+0.16,0.028)
    glColor3f(0,1,0) if signal_h==2 or signal_v==2 else glColor3f(0,0.3,0)
    draw_circle(x+0.045,y+0.06,0.028)



#    FOR VEHICLES 




def draw_car(car):
    x,y = car["x"], car["y"]
    glColor3f(*car["color"])
    glBegin(GL_QUADS)
    glVertex2f(x,y); glVertex2f(x+0.26,y); glVertex2f(x+0.26,y+0.09); glVertex2f(x,y+0.09)
    glEnd()
    glColor3f(car["color"][0]*0.88,car["color"][1]*0.88,car["color"][2]*0.88)
    glBegin(GL_QUADS)
    glVertex2f(x+0.06,y+0.09); glVertex2f(x+0.18,y+0.09)
    glVertex2f(x+0.16,y+0.15); glVertex2f(x+0.08,y+0.15)
    glEnd()
    glColor3f(0.08,0.08,0.08)
    draw_circle(x+0.06,y-0.005,0.022)
    draw_circle(x+0.20,y-0.005,0.022)

def draw_vertical_car(car):
    x = car["x"]
    y = car["y"]
    dir_ = car["dir"]
    color = car["color"]

    offset = 0.035 if dir_ == 1 else -0.035

    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x-0.045, y+offset)
    glVertex2f(x+0.045, y+offset)
    glVertex2f(x+0.045, y+offset+0.22)
    glVertex2f(x-0.045, y+offset+0.22)
    glEnd()

    glColor3f(color[0]*0.88, color[1]*0.88, color[2]*0.88)
    glBegin(GL_QUADS)
    glVertex2f(x-0.035, y+offset+0.13)
    glVertex2f(x+0.035, y+offset+0.13)
    glVertex2f(x+0.03,  y+offset+0.20)
    glVertex2f(x-0.03,  y+offset+0.20)
    glEnd()

    glColor3f(0.08,0.08,0.08)
    draw_circle(x-0.035, y+offset+0.005, 0.022)
    draw_circle(x+0.035, y+offset+0.005, 0.022)

#  DISPLAY 


def display():
    global time
    glClear(GL_COLOR_BUFFER_BIT)



    # Sky gradient



    glBegin(GL_QUADS)
    glColor3f(0.55, 0.82, 1.00) if is_day else glColor3f(0.02, 0.02, 0.08)
    glVertex2f(-1,1); glVertex2f(1,1)
    glColor3f(0.80, 0.92, 1.00) if is_day else glColor3f(0.04, 0.04, 0.12)
    glVertex2f(1,0.28); glVertex2f(-1,0.28)
    glEnd()




    # Stars - twinkling + slow movement



    if not is_day:
        glPointSize(2.5)
        glBegin(GL_POINTS)
        for star in stars:
            twinkle = sin(time * 6 + star["phase"]) * 0.45
            brightness = star["base_brightness"] + twinkle
            r = 1.0 + twinkle * 0.1
            g = 1.0 + twinkle * 0.05
            b = 0.95 + twinkle * 0.15
            glColor3f(r, g, b)
            glVertex2f(star["x"], star["y"])



            star["x"] += star["dx"] * 0.04
            if star["x"] < -1.0:
                star["x"] = 1.0
            if star["x"] > 1.0:
                star["x"] = -1.0

        glEnd()
        glPointSize(1.0)

    draw_roads()
    draw_footpath()
    draw_markings()
    draw_city()





    # for tree's in BOTTOM empty corner spaces 




    draw_tree(-0.96, -0.85, 1.20)  # bottom-left
    draw_tree( 0.96, -0.85, 1.15)  # bottom-right

    draw_signal(-0.25,0.24)
    draw_signal(0.19,-0.62)

    street_light(-0.72,-0.35)
    street_light(0.72,0.30)
    street_light(-0.42,0.30)
    street_light(0.42,-0.35)

    for car in cars:
        draw_car(car)

    for car in cars_v:
        draw_vertical_car(car)

    glFlush()


