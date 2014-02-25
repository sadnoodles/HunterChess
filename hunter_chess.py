# -*- coding: utf-8 -*-
#!/usr/bin/python
import wx
class Chess(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(10, 10))
        self.SetBackgroundColour('WHITE')
        self.newGame()
        self.BlackPiece=wx.Bitmap(r'GitHub40001.ico', wx.BITMAP_TYPE_ICO)
        # print self.BlackPiece.Size
        self.WhitePiece=wx.Bitmap(r'GitHub32512.ico', wx.BITMAP_TYPE_ICO)
        self.piece_r=20
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
        
        
    def OnSize(self, evt): 
        # When the window size changes we need a new buffer. 
        self.InitBuffer() 
    def OnPaint(self, evt):   
        dc = wx.BufferedPaintDC(self, self.buffer)

    def InitBuffer(self): 
        '''生成一个缓存PaintDC,并在其上绘制，避免直接显示造成闪烁'''
        w, h = self.GetClientSize()         
        self.buffer = wx.EmptyBitmap(w, h) 
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer) 
        self._mesh(dc)
        self._draw_info(dc)
        self._draw_pieces(dc)
        
    def _mesh(self,dc):
        '''绘制网格'''
        dc.SetBackground(wx.Brush(self.GetBackgroundColour())) 
        dc.Clear()
        dc.DrawRectangle(self.meshLeftTop[0]-1,self.meshLeftTop[1]-1, self.rcWidth*3+2, self.rcWidth*3+2)
        for i in range(3):
            for j in range(3):
                dc.DrawRectangle(self.meshLeftTop[0]+self.rcWidth*i,self.meshLeftTop[1]+self.rcWidth*j, self.rcWidth, self.rcWidth)
    def _draw_info(self,dc):
        '''显示当前玩家信息'''
        info="Current player:%s"%(['','black','white'][self.currentPlayer])
        dc.DrawText(info,10,10)
    def _draw_piece_by_pos(self,dc,pos,player=1):
        """根据在棋盘中的位置绘制一个棋子"""
        x,y=self.pos2xy(pos)
        # dc.DrawCircle(x,y,self.piece_r)
        # ic=wx.Bitmap(r'GitHub40001.ico', wx.BITMAP_TYPE_ICO)
        if player==1:
            x0,y0=self.BlackPiece.Size
            dc.DrawBitmap(self.BlackPiece,x-x0/2,y-y0/2,True)
        else:
            x0,y0=self.WhitePiece.Size
            dc.DrawBitmap(self.WhitePiece,x-x0/2,y-y0/2,True)
    def _draw_pieces(self,dc):
        '''绘制所有棋子'''
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j]==0:
                    continue
                color='black' if self.map[i][j]==1 else 'white'
                if (i,j)==self.selected_pos: #绘出选中的棋子
                    dc.SetPen(wx.Pen("yellow", 3))
                else:
                    dc.SetPen(wx.Pen("black", 1)) #外圈线条颜色
                dc.SetBrush(wx.Brush(color))
                self._draw_piece_by_pos(dc,(i,j),self.map[i][j])
    def OnDbClick(self,event):
        self.undo()
        self.OnSize(None)
        #for i in self.history:print i
    def OnClick(self,event):
        x,y = event.GetPosition()
        pos=self.xy2pos(x,y)
        #printpos
        if pos:
            if (not self.selecting):
                if self.map[pos[0]][pos[1]]==self.currentPlayer:
                    self.selecting=True
                    self.selected_pos=pos
            else:
                self.selecting=False
                if self.selected_pos and  self.canMove(self.selected_pos,pos):
                    self.move(self.selected_pos,pos)
                self.selected_pos=None
            self.OnSize(None)
            if self.count[self.currentPlayer]==0:
                wx.MessageBox("Player %s WIN!"%(['','black','white'][self.getAnotherPlayer(self.currentPlayer)]),'提示')
                self.newGame()
                self.OnSize(None)
    def newGame(self):
        '''新游戏开始，初始化数据
        currentPlayer：当前玩家 值为1或2
        selecting    ：是否正在选择False
        selected_pos ：被选中的子位置
        history      ：走子历史
        count        ：计数，剩余子的数目，列表,第一项起占位作用[0,4,4]
        map          : 棋盘的数据
            '''
        self.currentPlayer=1
        self.selecting=False
        self.selected_pos=None
        self.history=[]
        self.count=[0,4,4]
        self.map=[[1,1,1,1],
                  [0,0,0,0],
                  [0,0,0,0],
                  [2,2,2,2]]
    def canMove(self,pos1,pos2):
        """判断是否能移动，判断标准：1，距离为1；2，没有子。"""
        s1=abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])
        return s1==1 and self.map[pos2[0]][pos2[1]]==0
    def undo(self):
        """撤销移动，如果有吃子，也同时撤销"""
        if not self.history:
            return
        from_pos,to_pos,eat=self.history.pop()
        if eat:
            self.map[eat[0]][eat[1]]=self.currentPlayer
            self.count[self.currentPlayer]+=1
        self.map[to_pos[0]][to_pos[1]]=0
        self.map[from_pos[0]][from_pos[1]]=self.getAnotherPlayer(self.currentPlayer)
        self.currentPlayer=self.getAnotherPlayer(self.currentPlayer)
        
    def move(self,pos1,pos2):
        '''移动一个棋子从pos1到pos2，如果有吃子eaten是被吃的坐标'''
        self.map[pos2[0]][pos2[1]]=self.currentPlayer
        self.map[pos1[0]][pos1[1]]=0
        eaten=self.canEat(self.map,self.currentPlayer,pos2)
        if eaten:
            self.map[eaten[0]][eaten[1]]=0
            self.count[self.getAnotherPlayer(self.currentPlayer)]-=1
        self.history.append((pos1,pos2,eaten))
        self.currentPlayer=self.getAnotherPlayer(self.currentPlayer)
    def _strip(self,l):
        '''去除列表首尾的0，返回剩余的'''
        line=[a for a in l]
        while len(line)>0 and line[0]==0:
            line.pop(0)
        while len(line)>0 and line[-1]==0:
            line.pop()
        return line
    def _hasEatPattern(self,line,currentPlayer,lastStep):
        '''判断是否有吃子的结构'''
        left=self._strip(line)
        if currentPlayer==1:
            if left==[1,1,2] or left==[2,1,1]:
                return True
            return False
        if currentPlayer==2:
            if left==[1,2,2] or left==[2,2,1]:
                return True
            return False
    def canEat(self,m,currentPlayer,lastStep=(0,0)):
        '''判断是否能吃子，是则返回被吃子的位置；否则返回None'''
        line=m[lastStep[0]]
        col=[a[lastStep[1]] for a in m]
        if self._hasEatPattern(line,currentPlayer,lastStep):
            return (lastStep[0],line.index(self.getAnotherPlayer(currentPlayer)))
        if self._hasEatPattern(col,currentPlayer,lastStep):
            return (col.index(self.getAnotherPlayer(currentPlayer)),lastStep[1])
        return None
    def getAnotherPlayer(self,player):
        return 1 if player==2 else 2
    def pos2xy(self,pos):
        """ 将地图坐标，即列表的行、列转化为GUI的坐标  """
        x0,y0=self.meshLeftTop[0],self.meshLeftTop[1]
        w=self.rcWidth
        return y0+w*pos[1],x0+w*pos[0]
    def xy2pos(self,x,y):
        """ 将GUI的坐标转化为地图坐标，即列表的行、列  """
        x,y=x-self.meshLeftTop[0],y-self.meshLeftTop[1]
        r=self.piece_r
        if -r<x<r+3*self.rcWidth and -r<y<r+3*self.rcWidth:
            posx=(x+r)/self.rcWidth
            posy=(y+r)/self.rcWidth
            if x <=(posx*self.rcWidth+r) and y<=(posy*self.rcWidth+r):
                return posy,posx
        return None
#

if __name__=='__main__':
    app = wx.App()
    c=Chess(None, -1, 'Chess')
    def test():
        c.move((0,0),(1,0));print c.currentPlayer
        c.move((3,0),(2,0));print c.currentPlayer
        c.move((0,1),(0,0));print c.currentPlayer
        print c.map
        print c.history
        c.undo()
        print c.history
    # test()
    c.Show(True)
    app.MainLoop()