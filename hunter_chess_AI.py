# -*- coding: utf-8 -*-
import wx
from hunter_chess_basic import Chess
import time,os
import pickle
import random

wildcard='History file (*.history)|*.history|All files (*.*)|*.*'
class ComputerChess(Chess):
    def __init__(self, parent, id, title,AILevel=0):
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

        self.AILevel=AILevel
        
    def MenuNewGame(self,e=None):
        self.newGame()
        self.OnSize(None)
    def MenuSet(self,e=None):
        '����AI�ȼ�'
        dlg = wx.SingleChoiceDialog(self, '��ѡ��:', 'ѡ���սģʽ',['���˶�ս','�򵥵ĵ���','�����ĵ���'], 
        wx.CHOICEDLG_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.AILevel=dlg.GetSelection()
    def MenuRunHistory(self,e=None):
        dlg = wx.FileDialog(self, message="Choose a file",defaultDir=os.getcwd(),defaultFile="",
        wildcard=wildcard,
        style=wx.OPEN | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            try:
                hs=pickle.load(open(path,'r'))
                self.runHistory(hs)
            except:
                wx.MessageBox('�޷�ʶ����ļ���','����',wx.ICON_ERROR)
    def MenuSaveHistory(self,e=None):
        if not self.history:
            return
        dlg = wx.FileDialog(self, message="Save file as ...", defaultDir=os.getcwd(), 
        defaultFile="1.history", wildcard=wildcard, style=wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            pickle.dump(self.history,open(path,'w'))
    def getAllSteps(self,player):
        '����һ����ҿ����ߵ����п���'
        r=[]
        for i in range(len(self.map)):
            for j in range(len(self.map)):
                if self.map[i][j]==player:
                    r.extend(self.getStepsOfOne((i,j)))
        return r
    def getStepsOfOne(self,pos):
        '����һ���ӿ����ߵ����п���'
        x,y=pos
        r=[]
        surround=[[x-1,y],[x+1,y],[x,y-1],[x,y+1]]
        for i,j in surround:
            if 0<=i<=3 and 0<=j<=3 and self.map[i][j]==0:
                r.append(((x,y),(i,j)))
        return r
    def afterClick(self):
        '''���������ִ��'''
        if self.AILevel==0:
            #AI������
            return
        if self.currentPlayer==2:
            time.sleep(0.5)
            if self.AILevel==1:
                #��ȡ���������
                step=self.rndMove(2)
            else:
                #��ȡ��������ĽϺ�����
                step=self.getBestMove(2)
            if step:
                self.move(step[0],step[1])
                self.OnSize(None)
                self.ifWin(self.currentPlayer)
    def getBestMove(self,player):
        "���������������ؽϺõ�����"
        move,score=self.negMax(4,player,self.getAnotherPlayer(player))
        return move
    def negMax(self,ply,player,opponent):
        best=[0,-1024]
        steps=self.getAllSteps(player)
        if ply==0 or (not steps):
            score=self.evaluate(player)
            return [None,score]
        for move in steps:
            self.move(move[0],move[1])
            m,score=self.negMax(ply-1,opponent,player)
            self.undo()
            if -score>best[1]:
                best=[move,-score]
        # print player,best
        if not best[0]:
            best[0]=move
        return best
    def evaluate(self,player):
        return self.evaluateByEat(player)
    def evaluateByEat(self,player):
        value=10
        steps=self.getAllSteps(player)
        if not steps:
            return -1024
        for i,j in steps:
            eat=self.move(i,j)
            self.undo()
            if eat:
                value+=10
        return value
    def rndMove(self,player):
        '������ܳ��ӷ���һ����������ӣ��������'
        steps=self.getAllSteps(player)
        if not steps:
            return None
        for i,j in steps:
            eat=self.move(i,j)
            self.undo()
            if eat:
                return i,j
        return random.choice(steps)
    def runHistory(self,history):
        '������ʷ'
        self.newGame()
        self.OnSize(None)
        for pos1,pos2,eat in history:
            self.move(pos1,pos2)
            time.sleep(1)
            self.OnSize(None)
if __name__=='__main__':
    app = wx.App()
    c=ComputerChess(None, -1, 'Chess',AILevel=2)
    c.Show(True)
    app.MainLoop()