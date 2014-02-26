# -*- coding: utf-8 -*-
#!/usr/bin/python
#HunterChess:
#    author: ¡ı∫∆Ω‹
#    e-mail£∫sadnoodles@gmail.com
import wx
from hunter_chess_AI import ComputerChess

if __name__=='__main__':
    app = wx.App()
    c=ComputerChess(None, -1, 'Chess',AILevel=1)
    c.Show(True)
    app.MainLoop()