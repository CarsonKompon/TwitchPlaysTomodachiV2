import pyglet

# Lerp helper function
def lerp(a: float, b: float, t: float) -> float:
    return (1 - t) * a + t * b

# Visual Touches
touches = []
class Touch:

    def __init__(self, x, y, size, color, username="CarsonKompon"):
        self.x = x
        self.y = 240-y
        self.r = 0
        self.opacity = 1
        self.size = size
        self.color = color
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
            label = pyglet.text.Label(self.username, font_name='Arial', font_size=8, x=self.x, y=self.y-8, anchor_x='center', anchor_y='top', color=(*self.color, min(opacity*2,255)), batch=batch)
            label.draw()

def new_touch(x, y, size, color, username = "CarsonKompon"):
    touches.append(Touch(x, y, size, color, username))

def draw_touches():
    global touches
    batchVisualTouches = pyglet.graphics.Batch()
    for touch in touches:
        touch.draw(batchVisualTouches)
    touches = [touch for touch in touches if touch.opacity > 0.01]
    batchVisualTouches.draw()