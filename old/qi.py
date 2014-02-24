# -*- coding: utf-8 -*-
import copy #��������matrix��ģ��
import random
def pprint(x):
    for i in x :
        print i
LEFT=0
RIGHT=1
UP=2
DOWN=3
KILL=4
def getP2(p1,towards):
    #������ת��Ϊ����
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
class Step:
    def __init__(self,point,towards):
        self.p1=point
        self.towards=towards
        self.p2=getP2(self.p1,self.towards)
        self.step=(self.p1,self.towards)
        self.score=0
class qi:
    def __init__(self):
        self.newGame()
        pprint(self.newM)
    def newGame(self):
    #��ʼ��Ϸ
        self.newM=[ [1,1,1,1],
                    [0,0,0,0],
                    [0,0,0,0],
                    [2,2,2,2]]
        self.currentPlayer=1
        self.history=[]
    def getAnotherPlayer(self,currentPlayer):
    #��ȡ��һ�����
        return 2 if currentPlayer==1 else 1
    def _strip(self,l):
    #ȥ���б���β��0������ʣ���
        line=[a for a in l]
        while len(line)>0 and line[0]==0:
            line.pop(0)
        while len(line)>0 and line[-1]==0:
            line.pop()
        return line
    def _hasEatPattern(self,line,currentPlayer,lastStep):
    #�ж��Ƿ��г��ӵĽṹ
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
    #�ж��Ƿ��ܳ��ӣ����򷵻����Լ������ӵ�λ�ã����򷵻ؼ�
        line=m[lastStep[0]]
        col=[a[lastStep[1]] for a in m]
        if self._hasEatPattern(line,currentPlayer,lastStep):
            return True,(lastStep[0],line.index(self.getAnotherPlayer(currentPlayer)))
        if self._hasEatPattern(col,currentPlayer,lastStep):
            return True,(col.index(self.getAnotherPlayer(currentPlayer)),lastStep[1])
        return False
    def runHistory(self,history):
        self.newGame()
        for i,j in history:
            self.move(i,j)
    def isFailed(self,m,player):
        if not self.getAllSteps(m,player):
            return True
        else:
            return False
    def getAllSteps(self,m,player):
    #��ȡ��ǰ������п����ߵķ�ʽ
        r=[]
        for i in range(len(m)):
            for j in range(len(m[0])):
                if m[i][j]==player:
                    if i-1>=0 and m[i-1][j]==0:
                        r.append(Step((i,j),UP))
                    if i+1<len(m) and m[i+1][j]==0:
                        r.append(Step((i,j),DOWN))
                    if j-1>=0 and m[i][j-1]==0:
                        r.append(Step((i,j),LEFT))
                    if j+1<len(m[0]) and m[i][j+1]==0:
                        r.append(Step((i,j),RIGHT))
        return r
#######################################################
########���Ϻ�����ȷ���������������###################
    def canMove(self,step):
        if 0<=step.p2[0]<len(self.newM) and \
        0<=step.p2[1]<len(self.newM[0]) and \
        (abs(step.p2[0]-step.p1[0])+abs(step.p2[1]-step.p1[1]))==1 and \
        self.newM[step.p2[0]][step.p2[1]]==0:
            return True
        else:
            return False
    def a2b(self,m,currentPlayer,step):
    #��a�����ƶ���b�㣬�ɹ������棬���򷵻ؼ�
        p1,p2=step.p1,step.p2
        if m[p1[0]][p1[1]]==currentPlayer and self.canMove(step):
            m[p1[0]][p1[1]]=0
            m[p2[0]][p2[1]]=currentPlayer
            return True
        else:
            return False
    def evaluateAllSteps(self,currentM,currentPlayer):
        steps=self.getAllSteps(currentM,currentPlayer)
        for step in steps:
            copyM=copy.deepcopy(currentM)
            self.a2b(copyM,currentPlayer,step)
            if self.canEat(copyM,currentPlayer,step.p2):
                step.score=1
            step.M=copyM
        return steps
    
    def evaluateOneRound(self,currentM,currentPlayer,LEVEL=1):
    #���۵�ǰ��ҵ�ǰ���棬������һ������Ժõ��߷�
    #����ֵΪһ��step
        steps=self.evaluateAllSteps(currentM,currentPlayer)
        if LEVEL>=5:
            return steps
        for step in steps:
            if step.score==1:
                return [step,]
            for istep in self.evaluateOneRound(step.M,self.getAnotherPlayer(currentPlayer),LEVEL+1):
                step.score=-istep.score
        return steps
    def getMaxScore(self,steps):
        max=-65535
        maxi=0
        for i in range(len(steps)):
            if steps[i].score>=max:
                max=steps[i].score
                maxi=i
        return steps[i]
    def evaluate(self,currentM,currentPlayer,LEVEL=0):
        steps=self.evaluateOneRound(currentM,currentPlayer,0)
        print [s.score for s in steps]
        return self.getMaxScore(steps)
    def move(self,p1,towards):
        print "current player:",self.currentPlayer
        s=Step(p1,towards)
        p1,p2=s.p1,s.p2
        if p2==None:return
        moved=self.a2b(self.newM,self.currentPlayer,s)
        if moved:
            print "Done!"
            self.history.append((s.step))
            Killed=self.canEat(self.newM,self.currentPlayer,p2)
            print "KILL:",Killed
            if Killed:
                self.history.append((Killed[1],KILL))
                self.newM[Killed[1][0]][Killed[1][1]]=0
            self.currentPlayer=self.getAnotherPlayer(self.currentPlayer)
        if self.isFailed(self.newM,self.currentPlayer):
            print "Player%s has Failed!"%self.currentPlayer
        pprint(self.newM)
q=qi()
# q.move((0,1),DOWN)
# q.move((3,3),UP)
# pprint(q.getAllSteps(q.newM,2))
print '*'*15
def move(p,towards):
    # a,b=p
    # p=a-1,b-1
    q.move(p,towards)
    s=q.evaluate(q.newM,q.currentPlayer)
    print "Computer:"
    q.move(s.p1,s.towards)
    print "-"*20
# move((0,0),DOWN)
# move((3,2),UP)
# move((1,0),RIGHT)
# move((3,3),LEFT)
# move((0,1),DOWN)

# q.runHistory(q.history)
# move((1,1),RIGHT)
# move((0,0),RIGHT)

for i in range(10):
    s=q.evaluate(q.newM,q.currentPlayer)
    print "Computer:"
    q.move(s.p1,s.towards)