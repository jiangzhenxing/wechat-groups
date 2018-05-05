# coding=utf-8
import tkinter as tk
import logging
from tkinter import ttk
from groups import Group, GroupFrame

BDZ_DEFAULT = '请选择变电站'
ZXL_DEFAULT = '请选择主线路'
FZXL_DEFAULT = '请选择分支线路'
TQ_DEFAULT = '请选择台区'
GROUP_NAME_DEFAULT = '群名称关键词'

logger = logging.getLogger('app')

class SearchFrame(tk.Frame):
    """
    搜索框
    包含变电站，主经路，分支线路的选择和按群名称搜索
    """
    def __init__(self, master, bdz_dict, zxl_dict, fzxl_dict, tq_dict, group_frame):
        tk.Frame.__init__(self, master)
        self.bdz_dict = bdz_dict
        self.zxl_dict = zxl_dict
        self.fzxl_dict = fzxl_dict
        self.tq_dict = tq_dict
        self.group_frame = group_frame

        # 变电所选择
        # tk.Label(self, text='变电站:').grid(row=0, column=0)
        bdz_var = tk.StringVar()
        bdzs = [BDZ_DEFAULT] + list(bdz_dict.keys())
        bdz_choosen = ttk.Combobox(self, width=16, textvariable=bdz_var, values=bdzs, height=20, state='readonly')
        bdz_choosen.current(0)
        bdz_choosen.pack(side=tk.LEFT, padx=3)
        self.bdz_var = bdz_var
        self.bdz_choosen = bdz_choosen
        bdz_choosen.bind('<<ComboboxSelected>>', self.bdz_selected)

        # 主线路选择
        # tk.Label(self, text='主线路:').grid(row=0, column=2)
        zxl_var = tk.StringVar()
        zxls = [ZXL_DEFAULT]
        zxl_choosen = ttk.Combobox(self, width=16, textvariable=zxl_var, values=zxls, height=20, state='readonly')
        zxl_choosen.current(0)
        zxl_choosen.pack(side=tk.LEFT, padx=3)
        self.zxl_var = zxl_var
        self.zxl_choosen = zxl_choosen
        zxl_choosen.bind('<<ComboboxSelected>>', self.zxl_selected)

        # 分支线路选择
        # tk.Label(self, text='分支线路:').grid(row=0, column=4)
        fzxl_var = tk.StringVar()
        fzxls = [FZXL_DEFAULT]
        fzxl_choosen = ttk.Combobox(self, width=16, textvariable=fzxl_var, values=fzxls, height=20, state='readonly')
        fzxl_choosen.current(0)
        fzxl_choosen.pack(side=tk.LEFT, padx=3)
        self.fzxl_var = fzxl_var
        self.fzxl_choosen = fzxl_choosen
        fzxl_choosen.bind('<<ComboboxSelected>>', self.fzxl_selected)

        # 台区选择
        tq_var = tk.StringVar()
        tqs = [TQ_DEFAULT]
        tq_choosen = ttk.Combobox(self, width=16, textvariable=tq_var, values=tqs, height=20, state='readonly')
        tq_choosen.current(0)
        tq_choosen.pack(side=tk.LEFT, padx=3)
        self.tq_var = tq_var
        self.tq_choosen = tq_choosen
        tq_choosen.bind('<<ComboboxSelected>>', self.tq_selected)

        # 群名称搜索
        # tk.Label(self, text='群名称:').grid(row=0, column=6)
        name_var = tk.StringVar(value=GROUP_NAME_DEFAULT)
        search_entry = tk.Entry(self, textvariable=name_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=3)
        self.name_var = name_var
        search_entry.bind('<KeyPress>', lambda e: self.search() if e.keysym_num==65293 else '')
        search_entry.bind('<Button-1>', lambda e: name_var.set('') if name_var.get() == GROUP_NAME_DEFAULT else '')

        self.search_condition = ''

    def search(self):
        bdz = '' if self.bdz_var.get() == BDZ_DEFAULT else self.bdz_var.get()
        zxl = '' if self.zxl_var.get() == ZXL_DEFAULT else self.zxl_var.get()
        fzxl = '' if self.fzxl_var.get() == FZXL_DEFAULT else self.fzxl_var.get()
        tq = '' if self.tq_var.get() == TQ_DEFAULT else self.tq_var.get()
        name = '' if self.name_var.get() == GROUP_NAME_DEFAULT else self.name_var.get()
        # print('search', bdz, zxl, fzxl, tq, name)
        search_condition = ','.join([bdz, zxl, fzxl, tq, name])
        logger.info(search_condition)
        if search_condition != self.search_condition:
            self.group_frame.search(bdz, zxl, fzxl, tq, keyword=name)
            self.search_condition = search_condition

    def bdz_selected(self, event):
        self.bdz_choosen.selection_clear()
        bdz = self.bdz_var.get()
        zxl_values = [ZXL_DEFAULT] + ([] if bdz == BDZ_DEFAULT else list(self.bdz_dict[bdz]))
        self.zxl_choosen.configure(values=zxl_values)
        self.zxl_choosen.current(0)
        self.fzxl_choosen.configure(values=[FZXL_DEFAULT])
        self.fzxl_choosen.current(0)
        self.search()

    def zxl_selected(self, event):
        self.zxl_choosen.selection_clear()
        zxl = self.zxl_var.get()
        fzxl_values = [FZXL_DEFAULT] + ([] if zxl == ZXL_DEFAULT else list(self.zxl_dict[zxl]))
        self.fzxl_choosen.configure(values=fzxl_values)
        self.fzxl_choosen.current(0)
        self.search()

    def fzxl_selected(self, e):
        self.fzxl_choosen.selection_clear()
        fzxl = self.fzxl_var.get()
        tq_values = [TQ_DEFAULT] + ([] if fzxl == FZXL_DEFAULT else list(self.fzxl_dict[fzxl]))
        self.tq_choosen.configure(values=tq_values)
        self.tq_choosen.current(0)
        self.search()

    def tq_selected(self, e):
        self.tq_choosen.selection_clear()
        self.search()


def parse_group_dict(groups):
    bdz_dict = {}
    zxl_dict = {}
    fzxl_dict = {}
    tq_dict = {}

    for g in groups:
        if g.bdz not in bdz_dict: bdz_dict[g.bdz] = set()
        if g.zxl not in zxl_dict: zxl_dict[g.zxl] = set()
        if g.fzxl not in fzxl_dict: fzxl_dict[g.fzxl] = set()
        if g.tq not in tq_dict: tq_dict[g.tq] = set()

        bdz_dict[g.bdz].add(g.zxl)
        zxl_dict[g.zxl].add(g.fzxl)
        fzxl_dict[g.fzxl].add(g.tq)
        tq_dict[g.tq].add(g.name)

    return bdz_dict, zxl_dict, fzxl_dict, tq_dict

def main():
    root = tk.Tk()
    root.geometry('600x720+120+50')
    root.resizable(width=False, height=False)

    groups = [Group('变电所变电所' + str(i%10), '主经路主经路' + str(i%20), '分支线路支线路' + str(i%50), '台区台区台区台区','群名称群名称' + str(i)) for i in range(500)]
    bdz_dict, zxl_dict, fzxl_dict, tq_dict = parse_group_dict(groups)

    gframe = GroupFrame(root, groups)
    sframe = SearchFrame(root, bdz_dict, zxl_dict, fzxl_dict, gframe)
    print(bdz_dict)
    print(zxl_dict)
    print(fzxl_dict)
    sframe.pack()
    gframe.pack()
    # tk.Button(root, text='获取选择的群', command=lambda:print(gframe.get_selected())).pack()
    # tk.Button(root, text='search', command=lambda:print(gframe.search(keyword='1'))).pack()

    tk.mainloop()


if __name__ == '__main__':
    main()