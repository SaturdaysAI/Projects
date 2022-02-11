import configparser
import os


class Params:
    CFG = configparser.ConfigParser()
    CFG.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.cfg'), encoding='utf-8')

    PRM = CFG.get('DEFAULT', 'env')
    path_abs = CFG[PRM]['path_abs']
    path_dcm = os.path.join(path_abs, 'DCM')
    path_jpg = os.path.join(path_abs, 'JPG')