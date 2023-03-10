import colorsys
import random

import pyglet

# Lerp helper function
def lerp(a: float, b: float, t: float) -> float:
    return (1 - t) * a + t * b

# Visual Touches
touches = []
class Touch:

    def __init__(self, x, y, size, username="CarsonKompon"):
        random.seed(username)
        color = colorsys.hsv_to_rgb(random.random(), 0.8, 1)
        self.x = x
        self.y = 240-y
        self.r = 0
        self.opacity = 1
        self.size = size
        self.color = (int(color[0]*255), int(color[1]*255), int(color[2]*255))
        self.username = username

    def draw(self, batch):
        opacity = round(self.opacity * 255)
        self.r = lerp(self.r, self.size, 0.1)
        self.opacity = lerp(self.opacity, 0, 0.03)
        circle = pyglet.shapes.Circle(self.x, self.y, self.r, color=self.color, batch=batch)
        circle.opacity = opacity
        circle.draw()
        innerCircle = pyglet.shapes.Circle(self.x, self.y, self.r*0.92, color=(0, 0, 0), batch=batch)
        innerCircle.draw()
        dot = pyglet.shapes.Circle(self.x, self.y, 2, color=self.color, batch=batch)
        dot.opacity = opacity
        dot.draw()
        if self.username != "":
            yoff = self.y-8
            if self.y < 120:
                yoff = self.y+23
            label = pyglet.text.Label(self.username, font_name='Arial', font_size=8, x=self.x, y=yoff, anchor_x='center', anchor_y='top', color=(*self.color, min(opacity*2,255)), batch=batch)
            label.draw()

def new_touch(x, y, username = "CarsonKompon"):
    touches.append(Touch(x, y, 16, username))

def draw_touches():
    global touches
    batchVisualTouches = pyglet.graphics.Batch()
    for touch in touches:
        touch.draw(batchVisualTouches)
    touches = [touch for touch in touches if touch.opacity > 0.01]
    batchVisualTouches.draw()

# Visual Drags
drags = []
class Drag:

    def __init__(self, x1, y1, x2, y2, username="CarsonKompon"):
        random.seed(username)
        color = colorsys.hsv_to_rgb(random.random(), 0.8, 1)
        self.x = x1
        self.y = 240-y1
        self.x2 = x2
        self.y2 = 240-y2
        self.r = 0
        self.opacity = 1
        self.color = (int(color[0]*255), int(color[1]*255), int(color[2]*255))
        self.username = username

    def draw(self, batch):
        opacity = round(self.opacity * 255)
        self.r = lerp(self.r, 4, 0.1)
        self.x = lerp(self.x, self.x2, 0.1)
        self.y = lerp(self.y, self.y2, 0.1)
        self.opacity = lerp(self.opacity, 0, 0.03)
        circle = pyglet.shapes.Circle(self.x, self.y, self.r, color=self.color, batch=batch)
        circle.opacity = opacity
        circle.draw()
        if self.username != "":
            yoff = self.y-8
            if self.y < 120:
                yoff = self.y+23
            label = pyglet.text.Label(self.username, font_name='Arial', font_size=8, x=self.x, y=yoff, anchor_x='center', anchor_y='top', color=(*self.color, min(opacity*2,255)), batch=batch)
            label.draw()

def new_drag(x1, y1, x2, y2, username = "CarsonKompon"):
    drags.append(Drag(x1, y1, x2, y2, username))

def draw_drags():
    global drags
    batchVisualDrags = pyglet.graphics.Batch()
    for drag in drags:
        drag.draw(batchVisualDrags)
    drags = [drag for drag in drags if drag.opacity > 0.01]
    batchVisualDrags.draw()