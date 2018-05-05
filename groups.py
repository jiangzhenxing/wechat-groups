# coding=utf-8
"""
群列表
"""
import os
import tkinter as tk
from tkinter import font
from util import substr, help_message, user_path

WIDTH = 650         # 列表窗口的宽度
HEIGHT = 600        # 列表窗口的高度
BGCOLORS = ['white', '#FFE']    # 奇偶行的背景色


class Group:
    """
    一个微信群数据
    """
    def __init__(self, bdz, zxl, fzxl, tq, name, wxgroup=None, row=None, valid=True):
        """
        :param bdz:     变电站
        :param zxl:     主线路
        :param fzxl:    分支线路
        :param tq:      台区
        :param name:    群名称
        """
        self.bdz = bdz
        self.zxl = zxl
        self.fzxl = fzxl
        self.tq = tq
        self.name = name
        self.wxgroup = wxgroup
        self.row = row
        self.valid = valid

    def send_msg(self, msg):
        self.wxgroup.send_msg(msg)

    def send(self, content=None, media_id=None):
        self.wxgroup.send(content=content, media_id=media_id)


class GroupTitle:
    """
    微信群列表标题
    """
    def __init__(self, master, command):
        self._value = tk.IntVar(value=1)
        row = 0
        bgcolor = '#DDD'
        ft = font.Font(size=12, weight='bold')
        sticky = tk.N + tk.E + tk.S + tk.W
        self.ckb = tk.Checkbutton(master, variable=self._value, command=command, bg=bgcolor, pady=3)
        self.ckb.grid(row=row, column=0, sticky=sticky)
        self.bdz = tk.Label(master, text='变电站', bg=bgcolor, width=12, font=ft)
        self.zxl = tk.Label(master, text='10KV主线路', bg=bgcolor, width=12, font=ft)
        self.fzxl = tk.Label(master, text='分支线路', bg=bgcolor, width=12, font=ft)
        self.tq = tk.Label(master, text='台区', bg=bgcolor, width=12, font=ft)
        self.wxq = tk.Label(master, text='微信群', bg=bgcolor, width=17, font=ft)
        self.columns = [self.ckb, self.bdz, self.zxl, self.fzxl, self.tq, self.wxq]
        for i,c in enumerate(self.columns):
            c.grid(row=row, column=i, sticky=sticky)

    def reqheight(self):
        return max(map(lambda w: w.winfo_reqheight(),self.columns))

    def select(self):
        """
        选中
        """
        self.ckb.select()

    def selected(self):
        return self._value.get()


class GroupRow:
    """
    微信群列表中的一行
    """
    def __init__(self, master, row, group):
        self.row = row
        self.group = group
        self._value = tk.IntVar(value=1 if group.valid else 0)
        self.visible = True

        bgcolor = BGCOLORS[row % 2] if group.valid else 'red'
        ft = font.Font(size=11)
        sticky = tk.N + tk.E + tk.S + tk.W

        self.ckb = tk.Checkbutton(master, variable=self._value, bg=bgcolor, pady=3, state=tk.NORMAL if group.valid else tk.DISABLED)
        self.lb_bdz = tk.Label(master, text=substr(group.bdz, 11), width=13, bg=bgcolor, font=ft)
        self.lb_zxl = tk.Label(master, text=substr(group.zxl, 11), width=13, bg=bgcolor, font=ft)
        self.lb_fzxl = tk.Label(master, text=substr(group.fzxl, 11), width=13, bg=bgcolor, font=ft)
        self.lb_tq = tk.Label(master, text=substr(group.tq, 11), width=13, bg=bgcolor, font=ft)
        self.lb_name = tk.Label(master, text=substr(group.name, 18), width=21, bg=bgcolor, font=ft)
        self.columns = [self.ckb, self.lb_bdz, self.lb_zxl, self.lb_fzxl, self.lb_tq, self.lb_name]
        for i,c in enumerate(self.columns):
            c.grid(row=row, column=i, sticky=sticky)

    def reqheight(self):
        return max(map(lambda w: w.winfo_reqheight(),self.columns))

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

    def bind(self, event, func, add=None):
        for w in self.columns:
            w.bind(event, func, add=add)


class GroupList(tk.Frame):
    """
    微信群列表
    """
    def __init__(self, master, groups):
        tk.Frame.__init__(self, master=master)
        self.title = GroupTitle(self, command=self.toggle)
        self.groups = groups
        for row, group in enumerate(groups):
            group.row = GroupRow(self, row+1, group)

    def reqheight(self):
        n = self.visible_row_count()
        if n == 0:
            return self.title.reqheight()
        else:
            return self.title.reqheight() + self.groups[0].row.reqheight() * n

    def visible_row_count(self):
        return sum(map(lambda g: g.row.visible, self.groups))

    def search(self, bdz='', zxl='', fzxl='', tq='', keyword=''):
        """
        按所给条件搜索微信群
        将不符合条件的群设为不可见
        返回符合条件的结果数量
        """
        n = 0
        for group in self.groups:
            row = group.row
            if group.valid and (bdz == '' or bdz == group.bdz) and (zxl == '' or zxl == group.zxl) \
                    and (fzxl == '' or fzxl == group.fzxl) and (tq == '' or tq == group.tq) and (keyword == '' or keyword in group.name):
                row.show(row_num=n)
                row.select()
                n += 1
            else:
                row.hide()
        self.title.select()
        return n

    def show(self, groups):
        row = 0
        for group in self.groups:
            if group in groups:
                group.row.show(row_num=row)
                row += 1
            else:
                group.row.hide()

    def get_selected(self):
        """
        获取所有可见的并且选中的群
        """
        return [group for group in self.groups if group.valid and group.row.visible and group.row.seleted()]

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
        for group in self.groups:
            if group.valid and group.row.visible:
                group.row.select()

    def deselect_all(self):
        """
        将所有群的状态设为未选择
        """
        for group in self.groups:
            if group.row.visible:
                group.row.deselect()

    def reset(self):
        """
        重置群列表: 行的颜色等
        """
        for i,g in enumerate([g for g in self.groups if g.row.visible]):
            if g.valid:
                g.row.show(i)

    def bind(self, sequence=None, func=None, add=None):
        super().bind(sequence, func, add)
        for g in self.groups:
            g.row.bind(sequence, func, add)


class GroupFrame(tk.Frame):
    """
    GroupList + Scrollbar
    """
    def __init__(self, master, groups):
        tk.Frame.__init__(self, master=master)
        canvas = tk.Canvas(self, bg='#EEE', bd='1', width=WIDTH, height=HEIGHT) #创建canvas
        canvas.grid(row=0, column=0, sticky=tk.N + tk.S+tk.E+tk.W) #放置canvas的位置
        self.canvas = canvas

        # 创建GroupList并放到canvas里
        self.group_list = GroupList(canvas, groups)
        self.set_scrollregion((0, 0, WIDTH, self.group_list.reqheight()))
        vbar=tk.Scrollbar(self,orient=tk.VERTICAL) #竖直滚动条
        vbar.grid(row=0, column=1, sticky=tk.N + tk.S)
        vbar.configure(command=canvas.yview)

        canvas.config(yscrollcommand=vbar.set)
        canvas.create_window((0, 0), window=self.group_list, anchor=tk.NW)  # create_window

        self.help_btn = tk.Button(self, text='帮助信息', font=font.Font(size=12), width=8, command=self.help)
        self.help_btn.grid(row=1, column=0, rowspan=2, sticky=tk.W, padx=5, pady=5)

        self.total = tk.Label(self, text='共 ' + str(len(groups)) + ' 个群', font=font.Font(size=14))
        self.total.grid(row=1, column=0, rowspan=2, sticky=tk.E)

        def move(event):
            b,e = vbar.get()
            h = e - b
            # d=0.1
            # print('event.delta:', event.delta)
            d = vbar.delta(deltax=0, deltay=event.delta) * 2
            # print('fractional:', d)
            b1 = max(b + d, 0)  # 最小是0
            e1 = min(e + d, 1)  # 最大是1
            if b1 == 0:
                e1 = h
            elif e1 == 1:
                b1 = 1 - h
            vbar.set(b1, e1)
            canvas.yview(tk.MOVETO, b1)
            # print(b1, e1)
            # self.canvas.yview_scroll(-1 * (event.delta / 120), "units")
        self.group_list.bind('<MouseWheel>', move)

    def search(self, bdz='', zxl='', fzxl='', tq='', keyword=''):
        """
        返回符合条件的结果条数
        """
        n = self.group_list.search(bdz, zxl, fzxl, tq, keyword)
        scrollregion = (0, 0, WIDTH, self.group_list.reqheight())
        self.set_scrollregion(scrollregion)
        self.total.configure(text='共 ' + str(n) + ' 个群')
        return n

    def show_groups(self, groups):
        self.group_list.show(groups)

    def get_selected(self):
        """
        获取所有选中的群名称
        """
        return self.group_list.get_selected()

    def set_scrollregion(self, region):
        self.canvas.configure(scrollregion=region)

    def reset(self):
        self.group_list.reset()

    def help(self):
        window_help = tk.Toplevel(self)
        window_help.geometry('750x500+300+100')
        window_help.title('帮助信息')
        tk.Label(window_help, text=help_message, font=font.Font(size=12), justify=tk.LEFT).pack()


def parse_group(wxbot):
    """
    从文件中解析微信群
    """
    path = user_path(wxbot)
    wxgroups = wxbot.groups()
    groups = []
    if not os.path.exists(path+'/groups.csv'):
        with open(path+'/groups.csv', 'w', encoding='utf-8') as f:
            f.write('变电站,主线路,分支线路,台区,群名称\n')
            for g in wxgroups:
                f.write(',,,,' + g.name + '\n')
                groups.append(Group('', '', '', g.name, wxgroup=g))
    else:
        wxgroup_dict = {g.name: g for g in wxgroups}
        with open(path+'/groups.csv', encoding='utf-8') as f:
            f.readline()    # skip title
            for line in f:
                if len(line.strip()) == 0:
                    continue
                bdz,zxl,fzxl,tq,name = line.strip().split(',')
                if name in wxgroup_dict:
                    groups.append(Group(bdz, zxl, fzxl, tq, name, wxgroup=wxgroup_dict[name]))
                else:
                    groups.insert(0, Group(bdz, zxl, fzxl, tq, name, valid=False))
    return groups

#vbar.set(*map(lambda x: x-0.1, vbar.get()))
# tk.Button(text='down', command=move).grid(row=1, column=0) #print(vbar.delta(0,-50))
# tk.Button(text='up', command=lambda: print(vbar.delta(0,50))).grid(row=2, column=0)
# vbar.delta(0, 50)

def main():
    root = tk.Tk()
    root.geometry('600x720+120+50')
    root.resizable(width=False, height=False)

    groups = [Group('变电所变电所变电所'+str(i), '主经路主经路主经路'+str(i), '分支线路分支线路支线路'+str(i), '群名称群名称群名称群名称群名称'+str(i)) for i in range(60)]

    gframe = GroupFrame(root, groups)
    gframe.pack()

    tk.Button(root, text='获取选择的群', command=lambda: print(gframe.get_selected())).pack()
    tk.Button(root, text='search', command=lambda: print(gframe.search(keyword='1'))).pack()

    tk.mainloop()

if __name__ == '__main__':
    main()
