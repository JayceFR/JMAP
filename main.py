import pygame
import tkinter as tk
from tkinter.filedialog import askopenfilename
import os
tk.Tk().withdraw()


import tiles as t

pygame.init()
s_width = 1000
s_height = 600
screen = pygame.display.set_mode((s_width,s_height))
pygame.display.set_caption("JMAP")


tile_count = len(os.listdir('./Tiles'))
print("Tiles found ", tile_count)

#Helper subroutines

def add(tiles, place_pos, tile_imgs, scroll, inventory_pos):
    delete(tiles, place_pos, scroll)
    tiles.append(t.Tiles(place_pos[0] + scroll[0], place_pos[1] + scroll[1], tile_imgs[0].get_width(), tile_imgs[0].get_height(), tile_imgs[inventory_pos], inventory_pos+1))

def delete(tiles, place_pos, scroll):
    for pos, tile in sorted(enumerate(tiles), reverse=True):
        if tile.get_rect().x == place_pos[0] + scroll[0] and tile.get_rect().y == place_pos[1] + scroll[1]:
            tiles.pop(pos)

def id_dhedho(tiles, check_x, check_y):
    for tile in tiles:
        if tile.get_rect().x == check_x and tile.get_rect().y == check_y:
            return tile.get_id()
    return 0

def save(tiles, CELLSIZE, list_of_available_signs):
    min = [0,0]
    max = [0,0]
    for tile in tiles:
        if tile.get_rect().x < min[0]:
            min[0] = tile.get_rect().x
        if tile.get_rect().y < min[0]:
            min[1] = tile.get_rect().y
        if tile.get_rect().x > max[0]:
            max[0] = tile.get_rect().x
        if tile.get_rect().y > max[1]:
            max[1] = tile.get_rect().y
    map_text = ""
    while min[1] <= max[1]:
        start = min[0]
        while start <= max[0]:
            id_of_tile = id_dhedho(tiles, start, min[1])
            if id_of_tile != 0:
                map_text += list_of_available_signs[id_of_tile-1]
            else:
                map_text += "0"
            start += CELLSIZE
        map_text += "\n"
        min[1] += CELLSIZE
    return map_text

def load(data, CELLSIZE, list_of_available_signs):
    tiles = []
    row = data.split("\n")
    y = 0
    for r in row:
        x = 0
        for element in r:
            posid = 0
            while posid < len(list_of_available_signs) and list_of_available_signs[posid] != element:
                posid += 1
            if posid < len(list_of_available_signs):
                add(tiles, (x,y), tile_imgs, scroll, posid)
            x += CELLSIZE
        y += CELLSIZE
    return tiles

def load_tile_imgs(CELLSIZE, tile_count):
    tile_imgs = []
    for x in range(tile_count):
        curr_tile = pygame.image.load("./Tiles/tile" + str(x+1) + ".png").convert_alpha()
        curr_tile = pygame.transform.scale(curr_tile, (CELLSIZE, CELLSIZE))
        tile_imgs.append(curr_tile)
    return tile_imgs

def refresh(tiles, tile_imgs):
    for tile in tiles:
        tile.img = tile_imgs[tile.get_id()-1]

CELLSIZE = 32
#Test tiles
tile_logo_imgs = []
tile_imgs = []
for x in range(tile_count):
    curr_tile = pygame.image.load("./Tiles/tile" + str(x+1) + ".png").convert_alpha()
    curr_tile = pygame.transform.scale(curr_tile, (CELLSIZE, CELLSIZE))
    tile_imgs.append(curr_tile)
    second_tile = pygame.transform.scale(curr_tile, (32, 32))
    tile_logo_imgs.append(second_tile)

clock = pygame.time.Clock()

tiles = []

open_file = False

place_pos = [0,0]

scroll = [0,0]

inventory_pos = -1

hover_pos = -1

list_of_available_signs = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "!", "@", "#", "$", "%", "^", "&", "*", "-", "+", ":", ";", "<", ">", "/", "~"]
print("Max Limit Of Tiles -> ", len(list_of_available_signs))
run = True
while run:
    clock.tick(60)
    screen.fill((0,0,0))
    mouse_pos = list(pygame.mouse.get_pos())
    left = 0
    if open_file:
        f = open(file_loc, "r")
        data = f.read()
        f.close()
        tiles = load(data, CELLSIZE, list_of_available_signs)
        open_file = False
    for x in range((s_width//CELLSIZE)+1):
        pygame.draw.line(screen, (255,255,255), (left,0), (left,600))
        pygame.draw.line(screen, (255,255,255), (0, left), (1000,left))
        if mouse_pos[1] > left and mouse_pos[1] < left + CELLSIZE:
            place_pos[1] = left
        if mouse_pos[0] > left and mouse_pos[0] < left + CELLSIZE:
            place_pos[0] = left
        left += CELLSIZE
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if mouse_pos[0] < 130:
                    inventory_pos = hover_pos
                else:
                    add(tiles, place_pos, tile_imgs, scroll, inventory_pos)
            if event.button == 3:
                delete(tiles, place_pos, scroll)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                scroll[0] += CELLSIZE
            if event.key == pygame.K_LEFT:
                scroll[0] -= CELLSIZE
            if event.key == pygame.K_UP:
                scroll[1] -= CELLSIZE
            if event.key == pygame.K_DOWN:
                scroll[1] += CELLSIZE
            if event.key == pygame.K_s:
                print(save(tiles, CELLSIZE, list_of_available_signs))
            if event.key == 61:
                data = save(tiles, CELLSIZE, list_of_available_signs)
                CELLSIZE += 16
                tile_imgs = load_tile_imgs(CELLSIZE, tile_count)
                refresh(tiles, tile_imgs)
                tiles = load(data, CELLSIZE, list_of_available_signs)
            if event.key == pygame.K_MINUS:
                data = save(tiles, CELLSIZE, list_of_available_signs)
                if CELLSIZE > 16:
                    CELLSIZE -= 16
                tile_imgs = load_tile_imgs(CELLSIZE, tile_count)
                refresh(tiles, tile_imgs)
                tiles = load(data, CELLSIZE, list_of_available_signs)
            if event.key == pygame.K_t:
                print(len(tiles))
            if event.key == pygame.K_o:
                file_loc = askopenfilename()
                open_file = True
    for tile in tiles:
        tile.draw(screen, scroll)
    pygame.draw.polygon(screen, (0,0,0), [[0,0], [130,0], [130,600], [0,600]])
    start_pos = 0
    while start_pos < len(tile_logo_imgs):
        x = 0
        while x < 2:
            try:
                screen.blit(tile_logo_imgs[start_pos+x], ((50 * x)+15, 20*start_pos))
                current_rect = pygame.rect.Rect((50 * x)+15, 20*start_pos, 32, 32)
                if current_rect.collidepoint(mouse_pos):
                    hover_pos = start_pos + x
            except IndexError as e:
                pass
            x += 1
        start_pos += 2
    pygame.display.update()
    