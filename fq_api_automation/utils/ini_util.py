import configparser
import os

ini_path=os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),"config","configs.ini")
class HandleIni:
    def __init__(self):
        self.path=ini_path

    def read_ini(self):
        config=configparser.ConfigParser()
        config.read(self.path,encoding='utf-8')
        return config

read_ini=HandleIni()