def pprint(x):
    for i in x :
        print i
newM=[[1,1,1,1],[0,0,0,0],[0,0,0,0],[2,2,2,2]]
pprint(newM)
def a2b(m,current=1,p1=(0,0),p2=(1,0)):
    if not abs(p2[0]-p1[0])+abs(p2[1]-p1[1])==1:
        return False
    if m[p1[0]][p1[1]]==current and m[p2[0]][p2[1]]==0:
        m[p1[0]][p1[1]]=0
        m[p2[0]][p2[1]]=current
        return True
    else:
        return False
# print a2b(newM,1,(0,0),(1,0))
# pprint(newM)
def canEat(m,current=1,Point=(0,0)):
    return None
    return (m,n)
currentPlayer=1
def move(p1,p2):
    global currentPlayer
    print "current player:",currentPlayer
    moved=a2b(newM,currentPlayer,p1,p2)
    if moved:
        if canEat(newM,currentPlayer,p2):pass
    print {True:'Done!',False:'Failed!'}[moved]
    pprint(newM)
    if moved:
        currentPlayer=2 if currentPlayer==1 else 1
