# -*- coding: utf-8 -*-
import wx
from hunter_chess import Chess
import time,os
import pickle

wildcard='History file (*.history)|*.history|All files (*.*)|*.*'
class ComputerChess(Chess):
    def __init__(self, parent, id, title):
        Chess.__init__(self, parent, id, title)
        
        menuBar = wx.MenuBar()
        menu1 = wx.Menu()
        menu1.Append(100, "NewGame")
        menu1.Append(101, "SaveHistory")
        menu1.Append(102, "Set")
        menu1.Append(103, "RunHistory")
        menuBar.Append(menu1, "&Game")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.MenuNewGame, id=100)
        self.Bind(wx.EVT_MENU, self.MenuSaveHistory, id=101)
        self.Bind(wx.EVT_MENU, self.MenuSet, id=102)
        self.Bind(wx.EVT_MENU, self.MenuRunHistory, id=103)

    def MenuNewGame(self,e=None):
        self.newGame()
        self.OnSize(None)
    def MenuSet(self,e=None):
        for i,j in self.get_all_steps(self.currentPlayer):print i,'-->',j
        print '-'*10
    def MenuRunHistory(self,e=None):
        dlg = wx.FileDialog(self, message="Choose a file",defaultDir=os.getcwd(),defaultFile="",
        wildcard=wildcard,
        style=wx.OPEN | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            try:
                hs=pickle.load(open(path,'r'))
                self.run_history(hs)
            except:
                wx.MessageBox('无法识别的文件。','错误：',wx.ICON_ERROR)
    def MenuSaveHistory(self,e=None):
        if not self.history:
            return
        dlg = wx.FileDialog(self, message="Save file as ...", defaultDir=os.getcwd(), 
        defaultFile="1.history", wildcard=wildcard, style=wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            pickle.dump(self.history,open(path,'w'))
    def get_all_steps(self,player):
        r=[]
        for i in range(len(self.map)):
            for j in range(len(self.map)):
                if self.map[i][j]==player:
                    r.extend(self.get_steps_of_one((i,j)))
        return r
    def get_steps_of_one(self,pos):
        x,y=pos
        r=[]
        surround=[[x-1,y],[x+1,y],[x,y-1],[x,y+1]]
        for i,j in surround:
            if 0<=i<=3 and 0<=j<=3 and self.map[i][j]==0:
                r.append(((x,y),(i,j)))
        return r
    def afterClick(self):
        if self.currentPlayer==2:
            step=self.rndMove(2)
            #step=self.getBestMove(2)
            if step:
                self.move(step[0],step[1])
                self.OnSize(None)
    def getBestMove(self,player):
        steps=self.get_all_steps(player)
        pass
    def rndMove(self,player):
        import random
        steps=self.get_all_steps(player)
        if steps:
            return random.choice(steps)
    def run_history(self,history):
        self.newGame()
        self.OnSize(None)
        for pos1,pos2,eat in history:
            self.move(pos1,pos2)
            time.sleep(1)
            self.OnSize(None)
if __name__=='__main__':
    app = wx.App()
    c=ComputerChess(None, -1, 'Chess')
    c.Show(True)
    app.MainLoop()