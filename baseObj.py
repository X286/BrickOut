# -*- coding: utf-8 -*-

import pygame
import math

class GameObj (pygame.sprite.Sprite):

    def __init__(self,x, y, width, height, color = '#FF0000'):
        super(GameObj, self).__init__()

        self.image = pygame.Surface ([width, height])

        self.color = pygame.Color(color)
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.ar = 0

    def direction_to_rect(self, drect):
        self.ar = math.atan2(self.rect.centery - self.rect.top,
                        self.rect.right - self.rect.centerx)  # half of the angle of the right side
        # construct the corner angles into an array to search for index such that the index indicates direction
        # this is normalized into [0, 2π] to make searches easier (no negative numbers and stuff)
        dirint = [2 * self.ar, math.pi, math.pi + 2 * self.ar, 2 * math.pi]
        # calculate angle towars the center of the other rectangle, + ar for normalization into
        ad = math.atan2(self.rect.centery - drect.centery, drect.centerx - self.rect.centerx) + self.ar
        # again normalization, sincen atan2 ouputs values in the range of [-π,π]
        if ad < 0:
            ad = 2 * math.pi + ad
        # search for the quadrant we are in and return it
        for i in xrange(len(dirint)):
            if ad < dirint[i]:
                return i
        # just in case -1 as error indicator
        return -1

    def loadImage(self, path_to_img):
        x, y = self.rect.x, self.rect.y
        self.image = pygame.image.load (path_to_img)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def setSurface (self, surface):
        x,y = self.rect.x, self.rect.y
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x,y


class SpriteGroup (pygame.sprite.Group):
    def __init__(self, *sprites):
        super(SpriteGroup, self).__init__(sprites)

