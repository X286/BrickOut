# -*- coding: utf-8 -*-


from PIL import Image
import pygame
class ImgPil(object):

    def __init__(self, loadedimg, (cutposx, cutposy, width, height), (mergedx, mergedy), splitf, imgtype='RGBA'):
        self.cuted = loadedimg.crop((cutposx, cutposy, cutposx+width, cutposy+height))
        merged = Image.new(imgtype,  (mergedx, mergedy))
        self.__surface_to_Blit = splitf(merged, self.cuted).tobytes("raw", "RGBA")

    def rotate (self, angle):
        self.cuted =  self.cuted.rotate (angle)

    def retbuffer(self):
        return self.__surface_to_Blit

    def convert_to_pygame_surface(self, (width, height), imgtype='RGBA'):
        return pygame.image.frombuffer(self.__surface_to_Blit,  (width, height), imgtype)




