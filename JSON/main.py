import json
from PIL import ImageColor
from figures import *


class JSONContentException(Exception):
    pass


def convert_to_rgb(palette, color):
    if color in palette.keys():
        color = palette[color]
    if color[0] == '(':
        return eval(color)
    if color[0] == '#':
        return ImageColor.getrgb(color)
    raise JSONContentException('Unknown color!')


def parse_json(path):
    with open(path) as f:
        parsed_json = json.load(f)
    if not {'Figures', 'Screen', 'Palette'} == set(parsed_json.keys()):
        raise JSONContentException('Invalid JSON content')
    palette = parsed_json['Palette']
    scr_dict = parsed_json['Screen']

    if not {'width', 'height', 'bg_color', 'fg_color'} == set(scr_dict.keys()):
        raise JSONContentException('Invalid JSON content in "Screen"')

    image = Img(scr_dict['width'], scr_dict['height'], convert_to_rgb(palette, scr_dict['bg_color']),
                convert_to_rgb(palette, scr_dict['fg_color']))

    figures = []
    for figure in parsed_json['Figures']:
        if 'color' not in figure:
            f_color = image.fg_color
        else:
            f_color = convert_to_rgb(palette, figure['color'])

        f_type = figure['type']

        if f_type == 'point':
            if not {'x', 'y'}.issubset(figure.keys()):
                raise JSONContentException('Invalid arguments in "point" entry')

            figures.append(Point(f_color, figure['x'], figure['y']))
        elif f_type == 'polygon':
            if 'points' not in figure:
                raise JSONContentException('Invalid arguments in "polygon" entry')

            figures.append(Polygon(f_color, figure['points']))
        elif f_type == 'rectangle':
            if not {'x', 'y', 'width', 'height'}.issubset(figure.keys()):
                raise JSONContentException('Invalid arguments in "rectangle" entry')

            figures.append(Rectangle(f_color, figure['x'], figure['y'], figure['width'], figure['height']))
        elif f_type == 'square':
            if not {'x', 'y', 'size'}.issubset(figure.keys()):
                raise JSONContentException('Invalid arguments in "square" entry')

            figures.append(Square(f_color, figure['x'], figure['y'], figure['size']))
        elif f_type == 'circle':
            if not {'x', 'y', 'radius'}.issubset(figure.keys()):
                raise JSONContentException('Invalid arguments in "circle" entry')

            figures.append(Circle(f_color, figure['x'], figure['y'], figure['radius']))
        else:
            raise JSONContentException('Unknown figure')

    return figures, image


def draw_figures(figures, image: Img):
    screen = image.screen()
    for figure in figures:
        figure.draw(screen)
    image.show()


def main():
    figures, image = parse_json('text.json')
    draw_figures(figures, image)

    image.image.save('alamakota.png', 'PNG')


if __name__ == "__main__":
    main()
