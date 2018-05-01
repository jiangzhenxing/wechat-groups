#!/usr/bin/env python3
# coding=utf-8
import tkinter as tk
import wxpy as wx
import threading
import logging.config
from login import LoginFrame
from main import MainFrame
from groups import parse_group
from template import parse_template
from util import init, init_user

"""
先显示描码登录界面
登录后显示群管理界面
"""
init()
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('app')
window = tk.Tk()
window.title('微信群管理')
main_frame = None

def login():
    window.geometry('400x500+400+100')
    login_frame = LoginFrame(window)
    login_frame.pack()
    wxbot = wx.Bot(qr_callback=login_frame.qr_callback, login_callback=login_frame.login_callback, logout_callback=logout_callback)
    wxbot.enable_puid('wxpy_puid.pkl')
    init_user(wxbot)
    logger.info('%s login', wxbot.self.puid)
    login_frame.destroy()
    return wxbot

def show_main(wxbot):
    global main_frame
    window.geometry('950x680+200+50')

    groups = parse_group(wxbot)  # [Group('变电所变电所aaa' + str(i), '主经路主aaabbbb' + str(i), '分支线路分支线路支线路' + str(i), '群名称群名称名称aaaaaa' + str(i)) for i in range(60)]

    templates = parse_template()    # [Template('Temp' + str(i), 'Content  Content ContentContent ' + str(i)) for i in range(3)]

    main_frame = MainFrame(window, wxbot, groups, templates)
    main_frame.pack()

def logout_callback():
    if main_frame:
        main_frame.destroy()
    window.geometry('400x400+400+100')
    lb = tk.Label(window, text='您已退出登录，请:')
    lb.grid(row=0, column=0)
    def relogin():
        lb.destroy()
        logout_btn.destroy()
        threading.Thread(target=start, daemon=True).start()
    logout_btn = tk.Button(window, text='重新登录', command=relogin)
    logout_btn.grid(row=0, column=1)

def start():
    try:
        logger.info('starting...')
        wxbot = login()
        show_main(wxbot)
        logger.info('started')
    except Exception as e:
        logger.warning('exception:', exc_info=e)


threading.Thread(target=start, daemon=True).start()
tk.mainloop()
