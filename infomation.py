# coding=utf-8
"""
顶部消息提示区
"""
import tkinter as tk
from tkinter import font


class InfomationFrame(tk.Frame):

    def __init__(self, master, **cnf):
        tk.Frame.__init__(self, master, **cnf)
        tk.Label(master=self, text='欢迎使用微信群管理系统', width=32, font=font.Font(size=16, family='黑体', weight='bold')).pack(side=tk.TOP)
        self.infomation = tk.StringVar(master=self, value='消息提示消息提示消息')
        self.info_label = tk.Label(master=self, textvariable=self.infomation, fg='#555', font=font.Font(size=14))
        self.info_label.pack(side=tk.TOP)

    def show_info(self, info, fg='#CCC'):
        self.infomation.set(info)
        self.info_label.configure(fg=fg)

    def clear_info(self):
        self.infomation.set('')


def main():
    root = tk.Tk()
    root.geometry('600x720+120+50')
    root.resizable(width=False, height=False)


    gframe = InfomationFrame(root, width=400, height=100)
    gframe.pack(side=tk.LEFT)

    # tk.Button(root, text='获取选择的群', command=lambda: print(gframe.get_selected())).pack()
    # tk.Button(root, text='search', command=lambda: print(gframe.search(keyword='1'))).pack()

    tk.mainloop()

if __name__ == '__main__':
    main()
