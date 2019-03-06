#!/usr/bin/python

import pygame
import sys
import random
import math

# image/canvas size
image_x_size = 1280
image_y_size = 720

pygame.init()
screen = pygame.display.set_mode((image_x_size, image_y_size))
#surface = pygame.Surface((image_x_size, image_y_size))
#pyarray = pygame.PixelArray(surface)
pygame.display.set_caption("Blobs")

clock = pygame.time.Clock()
carryOn = True

while carryOn:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      carryOn = False
    screen.fill((0,0,255,0))
 #   pyarray[0:2073600] = (0,255,0,0)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()

exit()
