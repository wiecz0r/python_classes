from PIL import Image, ImageDraw
from matplotlib.pyplot import imshow



class Figure:
    def __init__(self, color):
        self.color = color

    def draw(self, screen):
        return None


class Point(Figure):
    def __init__(self, color, x, y):
        super().__init__(color)
        self.x = x
        self.y = y

    def draw(self, screen):
        screen.point([self.x, self.y], self.color)


class Polygon(Figure):
    def __init__(self, color, points):
        super().__init__(color)
        self.points = [tuple(a) for a in points]

    def draw(self, screen):
        screen.polygon(self.points, self.color, self.color)


class Square(Figure):
    def __init__(self, color, x, y, size):
        super().__init__(color)
        self.x = x
        self.y = y
        self.width = size

    def draw(self, screen):
        screen.rectangle([self.x, self.y, self.x + self.width, self.y + self.width], self.color, self.color)


class Rectangle(Square):
    def __init__(self, color, x, y, width, height):
        super().__init__(color, x, y, width)
        self.height = height

    def draw(self, screen):
        screen.rectangle([self.x, self.y, self.x + self.width, self.y + self.height], self.color, self.color)


class Circle(Figure):
    def __init__(self, color, x, y, radius):
        super().__init__(color)
        self.x = x
        self.y = y
        self.r = radius

    def draw(self, screen):
        screen.ellipse([self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r], self.color, self.color)


class Img:
    def __init__(self, width, height, bg_color, fg_color):
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self._fg_color = fg_color
        self._image = Image.new('RGBA', (self.width, self.height), self.bg_color)

    def screen(self):
        return ImageDraw.Draw(self._image, 'RGBA')

    @property
    def image(self):
        return self._image

    def show(self):
        #imshow(self._image)
        self._image.show("My image")

    @property
    def fg_color(self):
        return self._fg_color
