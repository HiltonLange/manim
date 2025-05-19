from manim import *
class MagnifyingGlass(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lens = Circle(radius=0.8, color=BLUE)
        self.lens.set_stroke(width=10)
        self.lens.set_fill(WHITE, opacity=0.1)
        self.handle = Rectangle(height=0.2, width=1.5, color=GOLD, fill_opacity=1)
        self.handle.set_stroke(width=4)
        self.handle.rotate(-PI / 4)
        self.handle.next_to(self.lens, direction=DR, buff=-0.3)
        self.add(self.lens, self.handle)
        self.offset = self.get_center() - self.lens.get_center()

    def move_to(self, location, **kwargs):
        super().move_to(location + self.offset, **kwargs)
