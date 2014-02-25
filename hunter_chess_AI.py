# -*- coding: utf-8 -*-
import wx
from hunter_chess import Chess
class ComputerChess(Chess):
    def __init__(self, parent, id, title):
        Chess.__init__(self, parent, id, title)
    def get_all_steps(self,player):
        pass

if __name__=='__main__':
    app = wx.App()
    c=ComputerChess(None, -1, 'Chess')
    c.Show(True)
    app.MainLoop()