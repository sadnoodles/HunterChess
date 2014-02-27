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
        '设置AI等级'
        dlg = wx.SingleChoiceDialog(self, '请选择:', '选择对战模式',['人人对战','掷筛子的电脑','会计算两步的电脑','聪明的电脑','O,DeepThought'], 
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
                wx.MessageBox('无法识别的文件。','错误：',wx.ICON_ERROR)
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
        '返回一个玩家可以走的所有可能'
        r=[]
        for i in range(len(self.map)):
            for j in range(len(self.map)):
                if self.map[i][j]==player:
                    r.extend(self.getStepsOfOne((i,j)))
        return r
    def getStepsOfOne(self,pos):
        '返回一个子可以走的所有可能'
        x,y=pos
        r=[]
        surround=[[x-1,y],[x+1,y],[x,y-1],[x,y+1]]
        for i,j in surround:
            if 0<=i<=3 and 0<=j<=3 and self.map[i][j]==0:
                r.append(((x,y),(i,j)))
        return r
    def afterClick(self):
        '''在鼠标点击后执行'''
        if self.AILevel==0:
            #AI被禁用
            return
        player=2
        if self.currentPlayer==player and self.GameOver==False:
            time.sleep(0.5)
            if self.AILevel==1:
                #获取随机的走子
                step=self.rndMove(player)
            elif self.AILevel==2:
                #获取经过计算的较好走子
                step,score=self.getBetterMove(player)
            elif self.AILevel==3:
                #获取经过计算的更好的走子
                step=self.getBetterMoveByDeep(player)
            elif self.AILevel==4:
                step=self.getBestMove(player)
                
            if step:
                self.move(step[0],step[1])
                self.OnSize(None)
                self.ifWin(self.currentPlayer)
    ##########计算两步的电脑########
    """计算两步的电脑使用的方法，
    如果加上递归就是最大最小树了
    评价结果是一个1,0组成的列表如，[1,0]
    奇数位表示这一步走子是否有吃子，1为吃
    偶数位表示对手这一步走子是否有吃子，1为没有吃
    比较的时候排序就是[1,1]意思是：吃子    ，没有被吃
                      [1,0]意思是：吃子    ，被吃
                      [0,1]意思是：没有吃子，没有被吃
                      [0,0]意思是：没有吃子，被吃
    """
    def getBetterMoveByDeep(self,player):
        
        s=[] #存放最终走法和最终分数
        tmp=[] #临时存放分数
        m=[] #临时存放走法
        self.lookdown(5,player,s,tmp,m,original=player)
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
    
    ##########聪明的电脑########
    def getBestMove(self,player):
        "搜索博弈树，返回较好的走法"
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
    #########随机的电脑#########
    def rndMove(self,player):
        '如果不能吃子返回一个随机的走法，否则吃子'
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
        '运行历史'
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