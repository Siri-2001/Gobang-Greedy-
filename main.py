from tkinter import *
import tkinter as tk
import numpy as np
from tkinter import messagebox

Pic_width = 600
Pic_height = 600
'''窗口长度'''
BoardSize = 15
'''棋盘大小'''
root = Tk()
root.resizable(False, False)
canvas_root = tk.Canvas(root, width=Pic_width, height=Pic_height)
per_width = Pic_width/BoardSize
per_height = Pic_height/BoardSize
Board = np.zeros((BoardSize, BoardSize))
SEARCH_DEPTH = 7
'''搜索时考虑的范围'''

THINK_DEPTH=2
'''搜索树长度'''

player_num = {}
player_num[True]=1
player_num[False]=2
color={}
player = True
color[True] = "black"
color[False] = "white"
def judge_win(x,y):
    '''判断棋盘中是否胜利'''
    if 0 not in Board:
        messagebox.showinfo(title='棋局已满', message='平局')
        #满棋盘时平局
        return
    count=[0,0,0,0]
    for i in range(BoardSize):
        if(Board[x][i]==player_num[player]):
            count[0] += 1
        else:
            count[0] =0
        if(Board[i][y]==player_num[player]):
            count[1] += 1
        else:
            count[1] =0
        if 5 in count:
            if player:
                messagebox.showinfo(title='胜负已分', message='黑子（人类）胜，看来AI无法统治人类了')
            else:
                messagebox.showinfo(title='胜负已分', message='白子(AI)胜，人类终将被AI统治')
            main()
            return
    '''判断横向、纵向有无相连5个棋子'''
    x1, y1=x, y
    x2, y2=x, y
    while x1-1>=0 and x1-1<BoardSize and y1-1>=0 and y1-1<BoardSize:
        x1 -= 1
        y1 -= 1
    while x1+1>=0 and x1+1<BoardSize and y1+1>=0 and y1+1<BoardSize:
        if (Board[x1][y1] == player_num[player]):
            count[2] += 1
        else:
            count[2]=0
        if 5 in count:
            if player:
                messagebox.showinfo(title='胜负已分', message='黑子（人类）胜，看来AI无法统治人类了')
            else:
                messagebox.showinfo(title='胜负已分', message='白子（AI）胜，人类终将被AI统治')
            main()
            return
        x1 += 1
        y1 += 1

        #print(x1,y1)

    while x2+1>=0 and x2+1<BoardSize and y2-1>=0 and y2-1<BoardSize:
        x2+=1
        y2-=1
    #print(x2,y2)
    while x2-1>=0 and x2-1<BoardSize and y2+1>=0 and y2+1<BoardSize:
        if (Board[x2][y2] == player_num[player]):
            count[3] += 1
        else:
            count[3]=0

        if 5 in count:
            if player:
                messagebox.showinfo(title='胜负已分', message='黑子（人类）胜，看来AI无法统治人类了')
            else:
                messagebox.showinfo(title='胜负已分', message='白子（AI）胜，人类终将被AI统治')
            main()
            return
        x2-=1
        y2+=1
    '''判断斜方向有没有相连五个旗子'''

def get_enemy_value(x,y):
    '''获得（x，y）点敌方的价值，价值计算方式，看这个点附近最长的相连同类点个数'''
    count=[0, 0, 0, 0]
    i=0
    x1=x+1
    while(x1>=0 and x1<BoardSize ):
        #print(count1,count1<VALUE_SEARCH_DEPTH)
        if(Board[x1][y]==1):
            i+=1
            x1 += 1

        else:
            break
    x1=x-1
    while(x1>=0 and x1<BoardSize ):
        if(Board[x1][y]==1):
            i+=1
            #print(x1)
            x1 -= 1

        else:
            break
    count[1] = i



    i=0
    y1=y+1

    while(y1>=0 and y1<BoardSize ):
        if(Board[x][y1]==1):
            i+=1
            y1 += 1

        else:
            break
    y1=y-1

    while(y1>=0 and y1<BoardSize ):
        if(Board[x][y1]==1):
            i+=1
            y1 -= 1

        else:
            break
    count[0]=i


    i=0
    x1=x+1
    y1=y+1

    while(x1>=0 and x1<BoardSize and y1>=0 and y1<BoardSize ):
        if(Board[x1][y1]==1):
            i+=1
            #print(x1)
            x1 += 1
            y1+=1

        else:
            break
    x1=x-1
    y1=y-1

    while(x1>=0 and x1<BoardSize and y1>=0 and y1<BoardSize ):
        if(Board[x1][y1]==1):
            i+=1
            #print(x1)
            x1 -= 1
            y1 -= 1

        else:
            break
    count[2] = i


    i=0
    x1=x+1
    y1=y-1

    while(x1>=0 and x1<BoardSize and y1>=0 and y1<BoardSize):
        if(Board[x1][y1]==1):
            i+=1
            #print(x1)
            x1 += 1
            y1-=1

        else:
            break
    x1=x-1
    y1=y+1

    while(x1>=0 and x1<BoardSize and y1>=0 and y1<BoardSize ):
        if(Board[x1][y1]==1):
            i+=1
            #print(x1)
            x1 -= 1
            y1 += 1

        else:
            break
    count[3] = i
    value=max(count)
    if(value==3):
        '''如果发现地方已经连成了3个点，则优先下这个位置'''
        return 310
    elif value==4:
        '''如果发现地方已经连成了3个点，则此处权值无限大'''
        return 800
    return value

def get_self_value(x, y):
    '''获得（x，y）点己方的价值，价值计算方式，看这个点附近最长的相连同类点个数'''
    count = [0, 0, 0, 0]
    i = 0
    x1 = x + 1
    while (x1 >= 0 and x1 < BoardSize):
        # print(count1,count1<VALUE_SEARCH_DEPTH)
        if (Board[x1][y] == 2):
            i += 1
            x1 += 1

        else:
            break
    x1 = x - 1
    while (x1 >= 0 and x1 < BoardSize):
        if (Board[x1][y] == 2):
            i += 1
            # print(x1)
            x1 -= 1

        else:
            break
    count[1] = i

    i = 0
    y1 = y + 1

    while (y1 >= 0 and y1 < BoardSize):
        if (Board[x][y1] == 2):
            i += 1
            y1 += 1

        else:
            break
    y1 = y - 1

    while (y1 >= 0 and y1 < BoardSize):
        if (Board[x][y1] == 2):
            i += 1
            y1 -= 1

        else:
            break
    count[0] = i

    i = 0
    x1 = x + 1
    y1 = y + 1

    while (x1 >= 0 and x1 < BoardSize and y1 >= 0 and y1 < BoardSize):
        if (Board[x1][y1] == 2):
            i += 1
            # print(x1)
            x1 += 1
            y1 += 1

        else:
            break
    x1 = x - 1
    y1 = y - 1

    while (x1 >= 0 and x1 < BoardSize and y1 >= 0 and y1 < BoardSize):
        if (Board[x1][y1] == 2):
            i += 1
            # print(x1)
            x1 -= 1
            y1 -= 1

        else:
            break
    count[2] = i

    i = 0
    x1 = x + 1
    y1 = y - 1

    while (x1 >= 0 and x1 < BoardSize and y1 >= 0 and y1 < BoardSize):
        if (Board[x1][y1] == 2):
            i += 1
            # print(x1)
            x1 += 1
            y1 -= 1

        else:
            break
    x1 = x - 1
    y1 = y + 1

    while (x1 >= 0 and x1 < BoardSize and y1 >= 0 and y1 < BoardSize):
        if (Board[x1][y1] == 2):
            i += 1
            # print(x1)
            x1 -= 1
            y1 += 1

        else:
            break
    count[3] = i
    value=max(count)
    if value==3:
        return 10
    #如果自己已经连成了3个，则优先下这里
    elif value==4:
        return 1000
    #如果自己已经连成了4个，则立刻下这个位置，赢得比赛
    return value

def get_around_point(x,y,depth=SEARCH_DEPTH):
    #获得SEARCH_DEPTH范围内的所有点，以方便后续对这些点进行价值评估
    list=[]
    for i in range(x-depth,x+depth+1):
        for j in range(y - depth, y + depth+1):
            if(i>=0 and i<BoardSize and j>=0 and j<BoardSize and Board[i][j]==0):
                list.append([i, j])
    return list

class fake_event():
    '''模拟鼠标点击的event，便于图形互动'''
    def __init__(self,point):
        self.y = point[0]*per_width+per_width//2
        self.x = point[1]*per_height+per_height//2

class TreeNode():
    '''蒙特卡洛树'''
    def __init__(self,x,y,Board,player):
        self.Board = Board
        self.value=-100
        self.x=x
        self.y=y
        self.player=player
        self.children=[]
    def get_value_leaf(self):
        return get_enemy_value(self.x,self.y)+get_self_value(self.x,self.y)
    def get_value_not_leaf(self):

        if player==False:

            value_list = []
            point_list = self.children
            for node in point_list:
                value_list.append(node.get_value_leaf())
            print(point_list[np.argmax(value_list)].x,point_list[np.argmax(value_list)].y)
            return [point_list[np.argmax(value_list)].x,point_list[np.argmax(value_list)].y]
    def get_children(self):
        point_list=get_around_point(self.x, self.y)
        for point in point_list:
            childBoard=self.Board
            childBoard[point[0]][point[1]]=player_num[not player]
            self.children.append(TreeNode(point[0],point[1],childBoard,not player))
def Siri_Go(x,y):
    '''AI下棋主程序'''
    try:
        value_list=[]
        point_list=get_around_point(x,y)
        for point in point_list:
            value_list.append(get_enemy_value(point[0], point[1])+get_self_value(point[0], point[1]))
            '''此处的价值计算，某点的价值为该点的己方价值+敌方价值'''
        change_Board(fake_event(point_list[np.argmax(value_list)]))
            #模拟图像点击
    except:
        return

def change_Board(event):
    '''在图像上画棋子'''
    global player, root

    try:
        if(Board[int(event.y//per_height)][int(event.x//per_width)]!=0):
                #print(int(event.y//per_height),int(event.x//per_height),22222222222)
                return
        else:
                Board[int(event.y//per_height)][int(event.x//per_width)] = player_num[player]
                if not player:
                    root.title("五子棋:黑子（人类）下")
                else:
                    root.title("五子棋:白子（AI）下")
                canvas_root.create_oval(per_width * int(event.x // per_width), per_height * int(event.y // per_height),
                                        per_width * int(event.x // per_width + 1),
                                        per_height * int(event.y // per_height + 1), fill=color[player])
                judge_win(int(event.y // per_height), int(event.x // per_width))
                player = (not player)
                if player==False:
                    Siri_Go(int(event.y//per_height), int(event.x//per_width))
    except:
        return

def main():
    global Board,root,player
    player=True
    canvas_root.delete(ALL)
    Board=np.zeros((BoardSize,BoardSize))
    cur_height=0
    cur_width=0
    root.title("五子棋:黑子（人类）先下")
    for i in range(BoardSize+1):
        canvas_root.create_line(cur_width, 0, cur_width, Pic_height)
        canvas_root.create_line(0,cur_height, Pic_width, cur_height)
        cur_width += per_width
        cur_height += per_height
    '''五子棋盘的绘制'''
    canvas_root.pack()
    canvas_root.bind("<Button-1>", change_Board,canvas_root)
    mainloop()
if __name__ == '__main__':
    main()




