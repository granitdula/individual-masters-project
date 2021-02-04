from panda3d.core import loadPrcFile
from direct.showbase.ShowBase import ShowBase

loadPrcFile("../config_3d/conf.prc")


class View3D(ShowBase):

    def __init__(self):
        super().__init__()
