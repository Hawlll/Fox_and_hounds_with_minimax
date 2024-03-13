import pygame as pyg
from constants import BLOCK_SIZE

def draw_piece(surface, x, y, file_path):
    """
    draw_piece() places image onto a surface given x and y

    Parameters:
    surface: surface of desired image placement
    x: x coordinate of placement
    y: y coordinate of placement
    file_path: path to image
    """

    image = pyg.image.load(file_path).convert()
    image = pyg.transform.scale(image, (BLOCK_SIZE, BLOCK_SIZE))
    surface.blit(image, (x, y))
