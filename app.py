#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import wxpy as wx
import io
import threading
import time
from login import LoginFrame
from main import MainFrame
from groups import Group
from template import Template

"""
先显示描码登录界面
后显示群管理界面
"""
window = tk.Tk()
window.title('微信群管理')
window.geometry('400x500')

login_frame = LoginFrame(window)
login_frame.pack()
qr_callback = login_frame.qr_callback

def login_callback():
    print('seccess login!')

def show_main(wxbot):
    window.geometry('890x680+120+50')
    login_frame.destroy()
    groups = [Group('变电所变电所aaa' + str(i), '主经路主aaabbbb' + str(i), '分支线路分支线路支线路' + str(i), '群名称群名称名称aaaaaa' + str(i)) for i in range(60)]
    templates = [Template('Temp' + str(i), 'Content  Content ContentContent ' + str(i)) for i in range(3)]

    frame = MainFrame(window, wxbot, groups, templates)
    frame.pack()

def start():
    wxbot = wx.Bot(qr_callback=qr_callback, login_callback=login_callback)
    print('wxbot', wxbot)
    for g in wxbot.groups():
        print(g)
    show_main(wxbot)

if __name__ == '__main__':
    threading.Thread(target=start, daemon=True).start()
    print('------------------------------------------')
    tk.mainloop()