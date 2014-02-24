import copy
def pprint(x):
    for i in x :
        print i
LEFT=0
RIGHT=1
UP=2
DOWN=3
KILL=4
class qi:
    def __init__(self):
        self.newGame()
        pprint(self.newM)
    def newGame(self):
        self.newM=[[1,1,1,1],[0,0,0,0],[0,0,0,0],[2,2,2,2]]
        self.currentPlayer=1
        self.history=[]
    def getAnotherPlayer(self,currentPlayer):
        return 2 if currentPlayer==1 else 1
    def _strip(self,l):
        line=[a for a in l]
        while len(line)>0 and line[0]==0:
            line.pop(0)
        while len(line)>0 and line[-1]==0:
            line.pop()
        return line
    def _hasEatPattern(self,line,currentPlayer,lastStep):
        left=self._strip(line)
        if currentPlayer==1:
            if left==[1,1,2] or left==[2,1,1]:
                return True
            return False
        if currentPlayer==2:
            if left==[1,2,2] or left==[2,2,1]:
                return True
            return False
    def getP2(self,p1,towards):
        if towards==DOWN:
            p2=(p1[0]+1,p1[1])
        elif towards==UP:
            p2=(p1[0]-1,p1[1])
        elif towards==LEFT:
            p2=(p1[0],p1[1]-1)
        elif towards==RIGHT:
            p2=(p1[0],p1[1]+1)
        elif towards==KILL:
            return None
        else:
            raise TypeError,"Please use RIGHT,LEFT,UP,DOWN to move"
        return p2
    def a2b(self,m,currentPlayer=1,p1=(0,0),p2=(1,0)):
        if not  abs(p2[0]-p1[0])+abs(p2[1]-p1[1])==1:
            return False
        if m[p1[0]][p1[1]]==currentPlayer and m[p2[0]][p2[1]]==0:
            m[p1[0]][p1[1]]=0
            m[p2[0]][p2[1]]=currentPlayer
            return True
        else:
            return False
    def canEat(self,m,currentPlayer,lastStep=(0,0)):
        line=m[lastStep[0]]
        col=[a[lastStep[1]] for a in m]
        if self._hasEatPattern(line,currentPlayer,lastStep):
            return True,(lastStep[0],line.index(self.getAnotherPlayer(currentPlayer)))
        if self._hasEatPattern(col,currentPlayer,lastStep):
            return True,(col.index(self.getAnotherPlayer(currentPlayer)),lastStep[1])
        return False
    def evalute(self,currentM,currentPlayer):
        copyM=copy.copy(currentM)
        allSteps=self.getAllSteps(copyM,currentPlayer)
        print allSteps
    def getAllSteps(self,m,player):
        r=[]
        for i in range(len(m)):
            for j in range(len(m[0])):
                if m[i][j]==player:
                    if i-1>=0 and m[i-1][j]==0:
                        r.append(((i,j),LEFT))
                    if i+1<len(m) and m[i+1][j]==0:
                        r.append(((i,j),RIGHT))
                    if j-1>=0 and m[i][j-1]==0:
                        r.append(((i,j),UP))
                    if j+1<len(m[0]) and m[i][j+1]==0:
                        r.append(((i,j),DOWN))
        return r
    def move(self,p1,towards):
        print "current player:",self.currentPlayer
        p2=self.getP2(p1,towards)
        if p2==None:return
        moved=self.a2b(self.newM,self.currentPlayer,p1,p2)
        if moved:
            print "Done!"
            self.history.append((p1,towards))
            Killed=self.canEat(self.newM,self.currentPlayer,p2)
            print "KILL:",Killed
            if Killed:
                self.history.append((Killed[1],KILL))
                self.newM[Killed[1][0]][Killed[1][1]]=0
            self.currentPlayer=self.getAnotherPlayer(self.currentPlayer)
        pprint(self.newM)
    def runHistory(self,history):
        self.newGame()
        for i,j in history:
            self.move(i,j)
q=qi()
# q.move((0,1),DOWN)
# q.move((3,2),UP)
# q.move((1,1),RIGHT)
# pprint(q.getAllSteps(q.newM,2))
print '*'*15
# q.runHistory(q.history)
def move(p,towards):
    a,b=p
    p=a-1,b-1
    q.move(p,towards)
move((0+1,0+1),DOWN)
move((3+1,0+1),UP)
move((0+1,1+1),DOWN)
move((3+1,2+1),UP)
move((0+1,3+1),DOWN)
move((2+1,0+1),DOWN)
move((1+1,3+1),DOWN)
move((3+1,1+1),UP)
move((0+1,2+1),LEFT)