# -*- coding: utf-8 -*-
#!/usr/bin/python
import wx
class chess(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(10, 10))
        self.SetBackgroundColour('WHITE')
        self.newGame()
        self.stone_r=20
        self.rcWidth=100
        self.meshLeftTop=(50,50)
        self.Size=2*self.meshLeftTop[0]+self.rcWidth*3+20,3*self.meshLeftTop[1]+self.rcWidth*3
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnDbClick)
        # wx.EVT_LEFT_DCLICK
        # wx.EVT_LEFT_DOWN
        # wx.EVT_LEFT_UP
        self.InitBuffer() 
        self.Bind(wx.EVT_SIZE, self.OnSize) 
        self.Bind(wx.EVT_PAINT, self.OnPaint) 
        self.Centre()
        self.Show(True)
        
    def OnSize(self, evt): 
        # When the window size changes we need a new buffer. 
        self.InitBuffer() 
    def OnPaint(self, evt):   
        dc = wx.BufferedPaintDC(self, self.buffer)   
    def InitBuffer(self):   
        w, h = self.GetClientSize()         
        self.buffer = wx.EmptyBitmap(w, h) 
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer) 
        self._mesh(dc)
        self._draw_stones(dc)
        
    def _mesh(self,dc):
        dc.SetBackground(wx.Brush(self.GetBackgroundColour())) 
        dc.Clear()
        dc.DrawRectangle(self.meshLeftTop[0]-1,self.meshLeftTop[1]-1, self.rcWidth*3+2, self.rcWidth*3+2)
        for i in range(3):
            for j in range(3):
                dc.DrawRectangle(self.meshLeftTop[0]+self.rcWidth*i,self.meshLeftTop[1]+self.rcWidth*j, self.rcWidth, self.rcWidth)
    def _draw_stone_by_pos(self,dc,pos):
        x,y=self.pos2xy(pos)
        dc.DrawCircle(x,y,self.stone_r)
    def _draw_stones(self,dc):
        info="Current player:%s"%(['black','white'][self.currentPlayer])
        dc.DrawText(info,10,10)
        black=True
        for player in self.stones_pos:
            color='black' if black else 'white'
            for i in player:
                if i==self.selected_stone: #绘出选中的棋子
                    dc.SetPen(wx.Pen("yellow", 3))
                    dc.SetBrush(wx.Brush(color))
                    self._draw_stone_by_pos(dc,i)
                else:
                    dc.SetPen(wx.Pen("black", 1))
                    dc.SetBrush(wx.Brush(color))
                    self._draw_stone_by_pos(dc,i)
            black=not black
    
    def OnDbClick(self,event):
        for i in self.history:print i
    def OnClick(self,event):
        x, y = event.GetPosition()
        pos=self.xy2pos(x,y)
        if pos:
            if (not self.selecting):
                if (pos in self.stones_pos[self.currentPlayer]):
                    self.selecting=True
                    self.selected_stone=pos
            else:
                self.selecting=False
                if self.selected_stone and  self.canMove(self.selected_stone,pos):
                    self.move(self.selected_stone,pos)
                self.selected_stone=None
            self.OnSize(None)
    def newGame(self):
        self.currentPlayer=0
        self.selecting=False
        self.selected_stone=None
        self.history=[]
        self.stones_pos=[[(0,0),(1,0),(2,0),(3,0)], #black
                        [(0,3),(1,3),(2,3),(3,3)]]  #white
    def canMove(self,pos1,pos2):
        s1=abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])
        return s1==1 and (not self.isStone(pos2))
    def move(self,pos1,pos2):
        i=self.stones_pos[self.currentPlayer].index(pos1)
        self.stones_pos[self.currentPlayer][i]=pos2
        eaten=self.eat(self.currentPlayer,pos2)
        if eaten:
            self.stones_pos[not self.currentPlayer].remove(eaten)
            if not(self.stones_pos[not self.currentPlayer]):
                wx.MessageBox("Player %s WIN!"%(['black','white'][self.currentPlayer]))
        self.history.append((pos1,pos2,eaten))
        self.currentPlayer=not self.currentPlayer
    def eat(self,player,lastpos):
        x,y=lastpos
        surroundings=[(x-1,y),(x,y-1),(x+1,y),(x,y+1)]
        headtails=[ ((x-2,y),(x+1,y)),
                    ((x,y-2),(x,y+1)),
                    ((x-1,y),(x+2,y)),
                    ((x,y-1),(x,y+2))]
        headtails2=[ ((x-3,y),(x+2,y)),
                    ((x,y-3),(x,y+2)),
                    ((x-2,y),(x+3,y)),
                    ((x,y-2),(x,y+3))]
        for i in range(4):
            if surroundings[i] in self.stones_pos[player]:
                    h,t=headtails[i]
                    h2,t2=headtails2[i]
                    if (h in self.stones_pos[not player]) and (not self.isStone(t)) and not(h2 in self.stones_pos[not player]):
                            return h
                    if (t in self.stones_pos[not player]) and (not self.isStone(h)) and not(t2 in self.stones_pos[not player]):
                            return t
        return None
    def isStone(self,pos):
        return (pos in self.stones_pos[0]) or (pos in self.stones_pos[1])       

    def pos2xy(self,pos):
        x0,y0=self.meshLeftTop[0],self.meshLeftTop[1]
        w=self.rcWidth
        return x0+w*pos[0],y0+w*pos[1]
    def xy2pos(self,x,y):
        x,y=x-self.meshLeftTop[0],y-self.meshLeftTop[1]
        r=self.stone_r
        if -r<x<r+3*self.rcWidth and -r<y<r+3*self.rcWidth:
            posx=(x+r)/self.rcWidth
            posy=(y+r)/self.rcWidth
            if x <=(posx*self.rcWidth+r) and y<=(posy*self.rcWidth+r):
                return posx,posy
        return None
app = wx.App()
c=chess(None, -1, 'Chess')
app.MainLoop()