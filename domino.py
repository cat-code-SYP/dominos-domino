#!/usr/bin/env python3

import pygame
from sys import exit
#mae
#original values:   window resolution 2000x1300 px, 
#                   GRID_SIZE = 1152 px, 
#                   BLOCK_SIZE = 96 px
#                   GRID_X, GRID_Y (starting grid coordinates) = 750, 74

pygame.init() #initializes pygame

#displays the surface that the player sees (stored in a variable 'screen'):
#set_mode((width,height)) - size of the window in pixels

#MONITOR_SETTINGS
monitor = pygame.display.Info()
SW = round(monitor.current_w * 0.58) 
SH = round((1300 / 2000) * SW) 
screen = pygame.display.set_mode((SW, SH))

SCALE = SW / 2000

def scale(pixels):
    return max(1, round(pixels * SCALE))
#/MONITOR_SETTINGS

pygame.display.set_caption("Domino's Domino")
icon = pygame.image.load('domino.png')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

score_font = pygame.font.Font(None, scale(50)) #text font upto change

#GRID_SIZING
GRID_X, GRID_Y = scale(750), scale(74) #distance of grid from starting point in (x, y) coodinates
BLOCK_SIZE = scale(96)
GRID_SIZE = BLOCK_SIZE * 12
#/GRID_SIZING

#SURFACES
score_surface = pygame.Surface((scale(650), SH))
text_surface = score_font.render("Score:", True, '#262724')
grid_background_surface = pygame.Surface((GRID_SIZE + scale(40), GRID_SIZE + scale(40)))
#/SURFACES

#SURFACE_COLORS
screen.fill('#f9f9f1')
score_surface.fill('#e3e8d4')
grid_background_surface.fill('#ebede6')
#/SURFACE_COLORS

#RECTANGLES
domino_block = pygame.Rect(scale(200), scale(500), BLOCK_SIZE * 2, BLOCK_SIZE)
#/RECTANGLES

def drawGrid():
    for x in range(GRID_X, GRID_X + GRID_SIZE, BLOCK_SIZE):
        for y in range(GRID_Y, GRID_Y + GRID_SIZE, BLOCK_SIZE):
            grid_square = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, "#cacab5", grid_square, scale(2), border_radius=scale(20))
    grid_square = pygame.Rect(GRID_X, GRID_Y, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, "#cacab5", grid_square, scale(4), border_radius=scale(20))

def drawDomino(): #argument defined outside of function, initial coordinates hardcoded
    pygame.draw.rect(screen, '#FFFFFF', domino_block, BLOCK_SIZE, border_radius=scale(20))
    pygame.draw.rect(screen, '#000000', domino_block, scale(2), border_radius=scale(20))
    pygame.draw.line(screen, '#000000', (domino_block.centerx, domino_block.top), (domino_block.centerx, domino_block.bottom), scale(2))
            

mouse_pos_old = (0, 0)
domino_pos_old = (0, 0)
click = False

#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() #pygame uninitialised
            exit() #assures that the code (in this case the while loop) is terminated
        if event.type == pygame.MOUSEBUTTONDOWN:
            if domino_block.collidepoint(pygame.mouse.get_pos()) and not click:
                click = True
                mouse_pos_old = pygame.mouse.get_pos()
                domino_pos_old = domino_block.center
        if event.type == pygame.MOUSEBUTTONUP:
            click = False

    if click:
        mouse_pos = pygame.mouse.get_pos()
        dx = mouse_pos[0] - mouse_pos_old[0]
        dy = mouse_pos[1] - mouse_pos_old[1]
        domino_block.center = (domino_pos_old[0] + dx, domino_pos_old[1] + dy)
    
    screen.fill('#f9f9f1')

    #SURFACE_POSITIONING
    screen.blit(score_surface,(0, 0))
    screen.blit(text_surface,(scale(75), scale(50)))
    screen.blit(grid_background_surface,(GRID_X - scale(20), GRID_Y - scale(20)))
    #/SURFACE_POSITIONING

    drawGrid()
    drawDomino()

    pygame.display.update() #updates the display surface
    clock.tick(60) #max 60fps