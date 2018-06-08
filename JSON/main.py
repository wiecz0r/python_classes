#!/usr/bin/env python3 
import json
from PIL import ImageColor
from figures import *
from argparse import ArgumentParser
from os.path import exists
from colorama import Fore


def convert_to_rgb(palette, color):
    if color in palette.keys():
        color = palette[color]
    if color[0] == '(':
        return eval(color)
    if color[0] == '#':
        return ImageColor.getrgb(color)
    raise ValueError('Unknown color!')


def parse_json(path):
    with open(path) as f:
        parsed_json = json.load(f)
    if not {'Figures', 'Screen', 'Palette'} == set(parsed_json.keys()):
        raise ValueError('Invalid JSON content')
    palette = parsed_json['Palette']
    scr_dict = parsed_json['Screen']

    if not {'width', 'height', 'bg_color', 'fg_color'} == set(scr_dict.keys()):
        raise ValueError('Invalid JSON content in "Screen"')

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
                raise ValueError('Invalid arguments in "point" entry')

            figures.append(Point(f_color, figure['x'], figure['y']))
        elif f_type == 'polygon':
            if 'points' not in figure:
                raise ValueError('Invalid arguments in "polygon" entry')

            figures.append(Polygon(f_color, figure['points']))
        elif f_type == 'rectangle':
            if not {'x', 'y', 'width', 'height'}.issubset(figure.keys()):
                raise ValueError('Invalid arguments in "rectangle" entry')

            figures.append(Rectangle(f_color, figure['x'], figure['y'], figure['width'], figure['height']))
        elif f_type == 'square':
            if not {'x', 'y', 'size'}.issubset(figure.keys()):
                raise ValueError('Invalid arguments in "square" entry')

            figures.append(Square(f_color, figure['x'], figure['y'], figure['size']))
        elif f_type == 'circle':
            if not {'x', 'y', 'radius'}.issubset(figure.keys()):
                raise ValueError('Invalid arguments in "circle" entry')

            figures.append(Circle(f_color, figure['x'], figure['y'], figure['radius']))
        else:
            raise ValueError('Unknown figure')

    return figures, image


def draw_figures(figures, image):
    screen = image.screen()
    for figure in figures:
        figure.draw(screen)
    image.show()


def process_args():
    parser = ArgumentParser(description="Draw figures")
    parser.add_argument('input', help="Input file")
    parser.add_argument('-o', '--output_file', help="Output file", nargs='?')
    args = parser.parse_args()
    in_file = args.input
    out_file = args.output_file
    print(" Input file:",Fore.GREEN,in_file,Fore.RESET)
    if not exists(in_file):
        raise ValueError("File doesn't exist")
    if in_file[-5:] != '.json':
        raise ValueError("Wrong file type. Should be .json")
    if out_file:
        if out_file[-4:] != '.png':
            out_file = out_file + '.png'
        print("Output file:", Fore.GREEN,out_file,Fore.RESET)

    return in_file, out_file


def main():
    try:
        in_file, out_file = process_args()
        figures, image = parse_json(in_file)
        draw_figures(figures, image)
        if out_file:
            image.image.save(out_file, 'PNG')
    except ValueError as e:
        print(Fore.RED,e)
        exit(1)


if __name__ == "__main__":
    main()
