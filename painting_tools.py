#coding=utf-8
from tkinter import *
import tkinter as tk
import numpy as np
import threading
graph_type=None
graph_type='point'# 初始化绘图类型
Pic_width = 1000
Pic_height = 1000
'''窗口长度'''
BoardSize = 500
'''棋盘大小'''
Board = np.zeros((BoardSize, BoardSize),dtype=int)
color="black"
cur_thread=None
# 主面板生成开始
root = Tk()
root.resizable(False, False)
canvas_root = tk.Canvas(root, width=Pic_width, height=Pic_height)
per_width = Pic_width/BoardSize
per_height = Pic_height/BoardSize
#主面板生成结束

point_list=[]
#画图操作
def line_Bersenham():
    point = point_list[-2:] #这里假定前面是x(纵轴)，后面是y(横轴)
    if point[1][1] - point[0][1]<0:
        point=[point[1], point[0]]
    delta_y = point[1][0] - point[0][0]
    delta_x = point[1][1] - point[0][1]
    d = 0
    if delta_x == 0:
        min_y = min(point[0][0],point[1][0])
        max_y = max(point[0][0], point[1][0])
        for i in range(min_y,max_y+1):
            change_Board(fake_event([i, point[0][1]]))
        return
    k = delta_y/delta_x
    x = point[0][1]
    y = point[0][0]
    delta_k=np.ceil(abs(k)) if k>0 else -np.ceil(abs(k))
    print("斜率为：",k,"delta_k:",delta_k)
    if y<point[1][0]:
        while(y<=point[1][0]):
            change_Board(fake_event([y, x]))
            x+=1
            d+=k
            if abs(d)>0.5:
                i = 0
                while (i < abs(delta_k)):
                    change_Board(fake_event([y, x]))
                    y += 1 if k>0 else -1
                    i+=1
                d=d-delta_k
    else:
        while(y>=point[1][0] and x<=point[1][1]):
            change_Board(fake_event([y, x]))
            x+=1
            d+=k
            if abs(d)>0.5:
                i=0
                while(i<abs(delta_k)):
                    change_Board(fake_event([y, x]))
                    y += 1 if k>0 else -1
                    i += 1
                # y += delta_k
                d=d-delta_k
def Bersenham(two_point):
    point = two_point
    if point[1][1] - point[0][1]<0:
        point=[point[1], point[0]]
    delta_y = point[1][0] - point[0][0]
    delta_x = point[1][1] - point[0][1]
    d = 0
    if delta_x == 0:
        min_y = min(point[0][0],point[1][0])
        max_y = max(point[0][0], point[1][0])
        for i in range(min_y,max_y+1):
            change_Board(fake_event([i, point[0][1]]))
        return
    k = delta_y/delta_x
    x = point[0][1]
    y = point[0][0]
    delta_k=np.ceil(abs(k)) if k>0 else -np.ceil(abs(k))
    if y<point[1][0]:
        while(y<=point[1][0] and x<=point[1][1]):
            change_Board(fake_event([y, x]))
            x+=1
            d+=k
            if abs(d)>0.5:
                i = 0
                while (i < abs(delta_k) and y<=point[1][0]):
                    change_Board(fake_event([y, x]))
                    y += 1 if k>0 else -1
                    i+=1
                d=d-delta_k
    else:
        while(y>=point[1][0] and x<=point[1][1]):
            change_Board(fake_event([y, x]))
            x+=1
            d+=k
            if abs(d)>0.5:
                i=0
                while(i<abs(delta_k) and y>=point[1][0] and x<=point[1][1]):
                    change_Board(fake_event([y, x]))
                    y += 1 if k>0 else -1
                    i += 1
                # y += delta_k
                d=d-delta_k
def draw_tri_angle():
    my_point_list=point_list[-3:]
    Bersenham([my_point_list[-1] , my_point_list[-2]])
    Bersenham([my_point_list[-1], my_point_list[-3]])
    Bersenham([my_point_list[-2], my_point_list[-3]])
def draw_quadrilateral():
    my_point_list=point_list[-4:]
    Bersenham([my_point_list[0] , my_point_list[1]])
    Bersenham([my_point_list[1], my_point_list[2]])
    Bersenham([my_point_list[2], my_point_list[3]])
    Bersenham([my_point_list[3], my_point_list[0]])
def draw_circle():
    my_point_list=point_list[-2:]
    R=np.sqrt((my_point_list[0][1]-my_point_list[1][1])**2+(my_point_list[0][0]-my_point_list[1][0])**2)
    d=1.25-R
    x=0
    y=R
    while(x<y):
        if d<=0:
            d+=2*x+3
            x+=1
        else:
            d+=2*(x-y)+5
            x+=1
            y-=1
        change_Board(fake_event([my_point_list[0][0] + y, my_point_list[0][1] + x]))
        change_Board(fake_event([my_point_list[0][0] - y, my_point_list[0][1] + x]))
        change_Board(fake_event([my_point_list[0][0] + y, my_point_list[0][1] - x]))
        change_Board(fake_event([my_point_list[0][0] - y, my_point_list[0][1] - x]))
        change_Board(fake_event([my_point_list[0][0] + x, my_point_list[0][1] + y]))
        change_Board(fake_event([my_point_list[0][0] - x, my_point_list[0][1] + y]))
        change_Board(fake_event([my_point_list[0][0] + x, my_point_list[0][1] - y]))
        change_Board(fake_event([my_point_list[0][0] - x, my_point_list[0][1] - y]))








#控制面板函数定义开始
def listener(cur_n,need_num,execute=None):
    while(np.sum(Board)-cur_n!=need_num):
        pass
    print('点迹选择结束,已绘图')
    execute()
    return

def painter_go():
    global graph_type, cur_thread
    if graph_type == 'line':
        need_num = 2
        cur_num = np.sum(Board, dtype=int)
        cur_thread = threading.Thread(target=listener, args=[cur_num, need_num, line_Bersenham])
        cur_thread.start()
    elif graph_type == 'tri_angle':
        need_num = 3
        cur_num = np.sum(Board, dtype=int)
        cur_thread = threading.Thread(target=listener, args=[cur_num, need_num, draw_tri_angle])
        cur_thread.start()
    elif graph_type == 'quadrilateral':
        need_num = 4
        cur_num = np.sum(Board, dtype=int)
        cur_thread = threading.Thread(target=listener, args=[cur_num, need_num, draw_quadrilateral])
        cur_thread.start()
    elif graph_type == 'circle':
        need_num = 2
        cur_num = np.sum(Board, dtype=int)
        cur_thread = threading.Thread(target=listener, args=[cur_num, need_num, draw_circle])
        cur_thread.start()

def exit_button_clicked():
    exit('正常退出Siri的绘图程序，欢迎下次使用')
def clear_button_clicked():
    canvas_root.delete(ALL)  # 删除所有绘图痕迹
def point_button_clicked():
    global graph_type
    disable_all_button()
    graph_type='point'
    painter_go()
def line_button_clicked():
    global graph_type
    disable_all_button()
    graph_type='line'
    painter_go()
def circle_button_clicked():
    global graph_type
    disable_all_button()
    graph_type = 'circle'
    painter_go()
def quadrilateral_button_clicked():
    global graph_type
    disable_all_button()
    graph_type = 'quadrilateral'
    painter_go()
def tri_angel_button_clicked():
    global graph_type
    disable_all_button()
    graph_type = 'tri_angle'
    painter_go()
#控制面板函数定义结束

#控制面板生成
control_pannel = Tk()
control_pannel.title("控制面板")
control_pannel.geometry("400x100")
button_list=[]
point_button = Button(control_pannel, command=point_button_clicked, text='point')
line_button = Button(control_pannel, command=line_button_clicked, text='line')
circle_button = Button(control_pannel, command=circle_button_clicked, text='circle')
quadrilateral_button = Button(control_pannel, command=quadrilateral_button_clicked, text='quadrilateral')
tri_angle_button = Button(control_pannel, command=tri_angel_button_clicked, text='tri_angle')
clear_button = Button(control_pannel, command=clear_button_clicked,text='clear')
exit_button = Button(control_pannel, command=exit_button_clicked,text='exit')
button_list.extend([point_button,line_button,circle_button,quadrilateral_button,tri_angle_button,clear_button])
def disable_all_button():
    # for i in button_list:
    #     i.config(state=tk.DISABLED)
    return
def able_all_button():
    for i in button_list:
        i['state'] = 'normal'
point_button.pack(side='left')
line_button.pack(side='left')
circle_button.pack(side='left')
quadrilateral_button.pack(side='left')
tri_angle_button.pack(side='left')
exit_button.pack(side='right')
clear_button.pack(side='right')

#控制面板生成结束



class fake_event():
    '''模拟鼠标点击的event，便于图形互动'''
    def __init__(self,point):
        self.y = point[0]*per_width+per_width//2
        self.x = point[1]*per_height+per_height//2


def change_Board(event):
    '''在图像上画点'''
    global player, root
    Board[int(event.y // per_height)][int(event.x // per_width)] += 1
    point_list.append([int(event.y // per_height), int(event.x // per_width)])
    try:
        canvas_root.create_oval(per_width * int(event.x // per_width), per_height * int(event.y // per_height),
                                per_width * int(event.x // per_width + 1),
                                per_height * int(event.y // per_height + 1), fill=color)
    except:
        return
def run_painting_tools():
    global Board, root, graph_type
    Board = np.zeros((BoardSize, BoardSize), dtype=int)
    canvas_root.delete(ALL)  # 删除所有绘图痕迹
    root.title("Siri的绘图软件")
    point_list=[]
    # 栅栏生成开始
    # cur_height = 0
    # cur_width = 0
    # for i in range(BoardSize+1):
    #     canvas_root.create_line(cur_width, 0, cur_width, Pic_height,c='blue')
    #     canvas_root.create_line(0,cur_height, Pic_width, cur_height,c='blue' )
    #     cur_width += per_width
    #     cur_height += per_height
    canvas_root.pack()
    # 栅栏生成结束

    #画布按钮绑定开始
    canvas_root.bind("<Button-1>", change_Board,canvas_root)
    #画布按钮绑定结束
    mainloop()#开始运行UI
run_painting_tools()




