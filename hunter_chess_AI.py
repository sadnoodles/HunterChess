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
        menu1.Append(104, "About")
        menuBar.Append(menu1, "&Game")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.MenuNewGame, id=100)
        self.Bind(wx.EVT_MENU, self.MenuSaveHistory, id=101)
        self.Bind(wx.EVT_MENU, self.MenuSet, id=102)
        self.Bind(wx.EVT_MENU, self.MenuRunHistory, id=103)
        self.Bind(wx.EVT_MENU, self.MenuAbout, id=104)

        self.AILevel=AILevel
        
    def MenuAbout(self,e=None):
        from wx.lib.wordwrap import wordwrap
        info = wx.AboutDialogInfo()
        info.Name = "Hunter Chess"
        info.Version = "0.1.0"
        info.Description = wordwrap(
        'HunterChess��һ��������Ϸ����Ϸ�������README�ļ���\n���ߣ����ƽ�\n�ʼ�:sadnoodles@gmail.com'.decode('gbk')
        ,500, wx.ClientDC(self))
        info.WebSite = ("https://github.com/sadnoodles/HunterChess", "HunterChess @github")
        info.License = wordwrap('Use and redistribute Under the terms of GNU GENERAL PUBLIC LICENSE.See the LICENSE file for detail.', 500, wx.ClientDC(self))
        wx.AboutBox(info)
    def MenuNewGame(self,e=None):
        self.newGame()
        self.OnSize(None)
    def MenuSet(self,e=None):
        '����AI�ȼ�'
        dlg = wx.SingleChoiceDialog(self, '��ѡ��:', 'ѡ���սģʽ',['���˶�ս','��ɸ�ӵĵ���','����������ĵ���','�����ĵ���','O,DeepThought'], 
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
        import pathname
        cd=os.getcwd()
        filename=pathname.numberName(dir=cd,start=1,ext='.history')
        dlg = wx.FileDialog(self, message="Save file as ...", defaultDir=cd, 
        defaultFile=filename, wildcard=wildcard, style=wx.SAVE)
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
        player=2
        if self.currentPlayer==player and self.GameOver==False:
            time.sleep(0.5)
            if self.AILevel==1:
                #��ȡ���������
                step=self.rndMove(player)
            elif self.AILevel==2:
                #��ȡ��������ĽϺ�����
                step,score=self.getBetterMove(player)
            elif self.AILevel==3:
                #��ȡ��������ĸ��õ�����
                step=self.getBetterMoveByDeep(player,3)
            elif self.AILevel==4:
                # step=self.getBestMove(player)
                step=self.getBetterMoveByDeep(player,5)
                
            if step:
                self.move(step[0],step[1])
                self.OnSize(None)
                self.ifWin(self.currentPlayer)
    ##########���������ĵ���########
    """���������ĵ���ʹ�õķ�����
    ������ϵݹ���������С����
    ���۽����һ��1,0��ɵ��б��磬[1,0]
    ����λ��ʾ��һ�������Ƿ��г��ӣ�1Ϊ��
    ż��λ��ʾ������һ�������Ƿ��г��ӣ�1Ϊû�г�
    �Ƚϵ�ʱ���������[1,1]��˼�ǣ�����    ��û�б���
                      [1,0]��˼�ǣ�����    ������
                      [0,1]��˼�ǣ�û�г��ӣ�û�б���
                      [0,0]��˼�ǣ�û�г��ӣ�����
    """
    def getBetterMoveByDeep(self,player,deep):
        
        s=[] #��������߷������շ���
        tmp=[] #��ʱ��ŷ���
        m=[] #��ʱ����߷�
        self.lookdown(deep,player,s,tmp,m,original=player)
        s.sort(lambda x,y:cmp(x[1],y[1]))
        # import pprint
        # pprint.pprint(s)
        # print s[-2]
        # print len(s)
        # print s[-1]
        # print '*'*8
        if s:
            return s[-1][0]
        else:
            return
    def lookdown(self,deep,player,s,tmp,m,original):
        import copy
        steps=self.getAllSteps(player)
        if deep==0 or not steps:
            s.append((copy.copy(m[0]),copy.copy(tmp)))
        else:
            ms=self.getBetterMove(player)
            if ms:
                mv,scs=ms
                h=scs[-1][-1]
                bests=map(lambda x:x[0],filter(lambda x:x[-1]>=h,scs))
            else:
                bests=steps
            random.shuffle(bests) #����һ��仯
            for i,j in bests:
                eat=self.move(i,j)
                m.append((i,j))
                player2=self.getAnotherPlayer(player)
                e=self.hasEat(player2)
                if player==original:
                    tmp.append(1 if eat else 0)
                    tmp.append(-e)
                elif player2==original:
                    tmp.append(0 if eat else 1)
                    tmp.append(e)
                self.lookdown(deep-1,player2,s,tmp,m,original)
                tmp.pop()
                tmp.pop()
                m.pop()
                self.undo()
        # print s,len(s)
        
    def getBetterMove(self,player):
        steps=self.getAllSteps(player)
        if not steps:
            return
        scores=[]
        highscore=[0,0]
        highmove=None
        for i,j in steps:
            score=[]
            eat=self.move(i,j)
            player2=self.getAnotherPlayer(player)
            score.append(not self.hasEat(player2))
            self.undo()
            score.insert(0,1 if eat else 0)
            scores.append(((i,j),score))
            if score>=highscore:
                highscore=score
                highmove=(i,j)
        scores.sort(lambda x,y:cmp(x[1],y[1]))
        # print scores
        return highmove,scores
    def hasEat(self,player):
        steps=self.getAllSteps(player)
        e=0
        for i,j in steps:
            eat=self.move(i,j)
            self.undo()
            if eat:
                e+=1
        return e
    
    ##########�����ĵ���########
    def getBestMove(self,player):
        "���������������ؽϺõ��߷�"
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
    #########����ĵ���#########
    def rndMove(self,player):
        '������ܳ��ӷ���һ��������߷����������'
        steps=self.getAllSteps(player)
        if not steps:
            return None
        for i,j in steps:
            eat=self.move(i,j)
            self.undo()
            if eat:
                return i,j
        return random.choice(steps)
    ####################
    def runHistory(self,history):
        '������ʷ'
        self.newGame()
        self.OnSize(None)
        for pos1,pos2,eat in history:
            self.move(pos1,pos2)
            time.sleep(0.5)
            self.OnSize(None)
            self.ifWin(self.currentPlayer)
if __name__=='__main__':
    app = wx.App()
    c=ComputerChess(None, -1, 'Chess',AILevel=3)
    c.Show(True)
    app.MainLoop()