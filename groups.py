#coding=utf-8
# -*- coding: UTF-8 -*-
import tkinter as tk
from tkinter import font

"""
群列表界面
"""
WIDTH = 450         # 列表窗口的宽度
HEIGHT = 600        # 列表窗口的高度
ROW_HEIGHT = 30     # 行高
BGCOLORS = ['white', '#FFE']    # 行的背景色

class Group:
    """
    一个微信群数据
    """
    def __init__(self, bdz, zxl, fzxl, name):
        """
        :param bdz:     变电站
        :param zxl:     主线路
        :param fzxl:    分支线路
        :param name:    群名称
        """
        self.bdz = bdz
        self.zxl = zxl
        self.fzxl = fzxl
        self.name = name


class GroupTitle:
    """
    微信群列表标题
    """
    def __init__(self, master, command):
        self._value = tk.IntVar(value=1)
        row = 0
        bgcolor = '#DDD'
        ft = font.Font(size=14, weight='bold')
        sticky = tk.N + tk.E + tk.S + tk.W
        tk.Checkbutton(master, variable=self._value, command=command, bg=bgcolor, pady=5).grid(row=row, column=0, sticky=sticky)
        tk.Label(master, text='变电站', bg=bgcolor, font=ft).grid(row=row, column=1, sticky=sticky)
        tk.Label(master, text='10KV主线路', bg=bgcolor, font=ft).grid(row=row, column=2, sticky=sticky)
        tk.Label(master, text='分支线路', bg=bgcolor, font=ft).grid(row=row, column=3, sticky=sticky)
        tk.Label(master, text='微信群', bg=bgcolor, font=ft).grid(row=row, column=4, sticky=sticky)

    def selected(self):
        return self._value.get()


class GroupRow:
    """
    微信群列表中的一行
    """
    def __init__(self, master, row, group):
        self.row = row
        self.group = group
        self._value = tk.IntVar(value=1)
        self.visible = True

        bgcolor = BGCOLORS[row % 2]
        ft = font.Font(size=14)
        sticky = tk.N + tk.E + tk.S + tk.W

        self.ckb = tk.Checkbutton(master, variable=self._value, bg=bgcolor, pady=5)
        self.lb_bdz = tk.Label(master, text=group.bdz, bg=bgcolor, font=ft)
        self.lb_zxl = tk.Label(master, text=group.zxl, bg=bgcolor, font=ft)
        self.lb_fzxl = tk.Label(master, text=group.fzxl, bg=bgcolor, font=ft)
        self.lb_name = tk.Label(master, text=group.name, bg=bgcolor, font=ft)
        self.columns = [self.ckb, self.lb_bdz, self.lb_zxl, self.lb_fzxl, self.lb_name]

        self.ckb.grid(row=row, column=0, sticky=sticky)
        self.lb_bdz.grid(row=row, column=1, sticky=sticky)
        self.lb_zxl.grid(row=row, column=2, sticky=sticky)
        self.lb_fzxl.grid(row=row, column=3, sticky=sticky)
        self.lb_name.grid(row=row, column=4, sticky=sticky)

    def set_bgcolor(self, color):
        for c in self.columns:
            c.configure(bg=color)

    def seleted(self):
        """
        本行是否被选中
        """
        return self._value.get()

    def select(self):
        """
        选中
        """
        self.ckb.select()

    def deselect(self):
        """
        取消选中
        """
        self.ckb.deselect()

    def hide(self):
        """
        隐藏本行
        """
        for c in self.columns:
            c.grid_remove()
        self.visible = False

    def show(self, row_num):
        """
        显示本行
        :param row_num:    显示在第几行
        """
        for c in self.columns:
            c.grid()
            c.configure(bg=BGCOLORS[row_num % 2])
        self.visible = True


class GroupList(tk.Frame):
    """
    微信群列表
    """
    def __init__(self, master, groups):
        tk.Frame.__init__(self, master=master)
        self.title = GroupTitle(self, command=self.toggle)
        self.group_rows = [GroupRow(self,row+1,group) for row,group in enumerate(groups)]

    def search(self, bdz='', zxl='', fzxl='', keyword=''):
        """
        按所给条件搜索微信群
        将不符合条件的群设为不可见
        返回符合条件的结果数量
        """
        n = 0
        for row in self.group_rows:
            if bdz in row.group.bdz and zxl in row.group.zxl and fzxl in row.group.fzxl and keyword in row.group.name:
                row.show(row_num=n)
                n += 1
            else:
                row.hide()
        return n

    def get_selected(self):
        """
        获取所有可见的并且选中的群名称
        """
        return [row.group.name for row in self.group_rows if row.visible and row.seleted()]

    def toggle(self):
        """
        全选或全不选
        """
        # print('toggle', self.title.selected())
        if self.title.selected():
            self.select_all()
        else:
            self.deselect_all()

    def select_all(self):
        """
        选择所有可见的群
        """
        for row in self.group_rows:
            if row.visible:
                row.select()

    def deselect_all(self):
        """
        将所有群的状态设为未选择
        """
        for row in self.group_rows:
            if row.visible:
                row.deselect()


class GroupFrame(tk.Frame):
    """
    GroupList + Scrollbar
    """
    def __init__(self, master, groups):
        tk.Frame.__init__(self, master=master)
        canvas = tk.Canvas(self, bg='green', bd='1', width=WIDTH, height=HEIGHT, scrollregion=(0, 0, WIDTH, ROW_HEIGHT * (len(groups)+1))) #创建canvas
        canvas.grid(row=0, column=0, sticky=tk.N + tk.S+tk.E+tk.W) #放置canvas的位置

        # 创建GroupList并放到canvas里
        self.group_list = GroupList(canvas, groups)
        vbar=tk.Scrollbar(self,orient=tk.VERTICAL) #竖直滚动条
        vbar.grid(row=0, column=1, sticky=tk.N + tk.S)
        vbar.configure(command=canvas.yview)

        canvas.config(yscrollcommand=vbar.set)
        canvas.create_window((0, 0), window=self.group_list, anchor=tk.NW)  # create_window
        self.canvas = canvas

        def move(event):
            b,e = vbar.get()
            h = e - b
            # d=0.1
            print('event.delta:', event.delta)
            d = vbar.delta(deltax=0, deltay=event.delta)
            print('fractional:', d)
            b1 = max(b + d, 0)  # 最小是0
            e1 = min(e + d, 1)  # 最大是1
            if b1 == 0:
                e1 = h
            elif e1 == 1:
                b1 = 1 - h
            vbar.set(b1, e1)
            canvas.yview(tk.MOVETO, b1)
            print(b1, e1)
            # self.canvas.yview_scroll(-1 * (event.delta / 120), "units")

        canvas.bind_all('<MouseWheel>', move)
        # self.group_list.bind('<MouseWheel>', move, add=True)

    def search(self, bdz='', zxl='', fzxl='', keyword=''):
        """
        返回符合条件的结果条数
        """
        n = self.group_list.search(bdz, zxl, fzxl, keyword)
        scrollregion = (0, 0, WIDTH, ROW_HEIGHT * (n + 1))
        self.set_scrollregion(scrollregion)
        return n

    def get_selected(self):
        """
        获取所有选中的群名称
        """
        return self.group_list.get_selected()

    def set_scrollregion(self, region):
        self.canvas.configure(scrollregion=region)


#vbar.set(*map(lambda x: x-0.1, vbar.get()))
# tk.Button(text='down', command=move).grid(row=1, column=0) #print(vbar.delta(0,-50))
# tk.Button(text='up', command=lambda: print(vbar.delta(0,50))).grid(row=2, column=0)
# vbar.delta(0, 50)

def main():
    root = tk.Tk()
    root.geometry('600x720')

    groups = [Group('变电所'+str(i), '主经路'+str(i), '分支线路'+str(i), '群名称'+str(i)) for i in range(60)]

    gframe = GroupFrame(root, groups)
    gframe.pack()

    tk.Button(root, text='获取选择的群', command=lambda: print(gframe.get_selected())).pack()
    tk.Button(root, text='search', command=lambda: print(gframe.search(keyword='1'))).pack()

    tk.mainloop()

if __name__ == '__main__':
    main()
