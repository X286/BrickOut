import glob, os, re

class lvl_open (object):
    def __init__(self, lvl_dir):
        self.__lst = os.listdir(lvl_dir)
        self.__lst = self.__natural_sort(self.__lst)
    def get_sorted (self):
        return self.__lst
    @staticmethod
    def __natural_sort(l):
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
        return sorted(l, key = alphanum_key)


