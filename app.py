#!/usr/bin/env python3
# coding=utf-8
import tkinter as tk
import wxpy as wx
import threading
import logging.config
import time
import configparser
import traceback
import util
from login import LoginFrame
from main import MainFrame
from groups import parse_group
from template import parse_template
from util import init, init_user

"""
先显示描码登录界面
登录后显示群管理界面
"""
version = '1.1.2'
init()
config = configparser.ConfigParser()
config.read('config/app.ini')
encoding = config.get('basic', 'encoding', fallback=None)
logging.config.fileConfig('config/logging.conf')
logger = logging.getLogger('app')
window = tk.Tk()
window.title('微信群管理-' + version)
main_frame = None

def start():
    try:
        # if not check_licence():
        #     return
        window.geometry('400x300+400+200')
        frame = tk.Frame(window)
        pass_lb = tk.Label(frame, text='请输入密码：')
        pass_lb.grid(row=0, column=0, pady=5)
        passwd = tk.StringVar(master=frame)
        passwd_entry = tk.Entry(frame, textvariable=passwd, show='*')
        passwd_entry.grid(row=1, column=0)
        passwd_entry.focus()
        def _login():
            if passwd.get() == time.strftime('%Y%m%d') + '123':
                frame.destroy()
                threading.Thread(target=start_wxgroup, daemon=True).start()
            else:
                pass_lb.config(text='密码不正确，请重新输入:')

        passwd_entry.bind('<KeyPress>', lambda e: _login() if e.keysym_num == 65293 else '')
        tk.Button(frame, text='登录', width=5, command=_login).grid(row=2, column=0, pady=5)
        frame.pack()
    except Exception as e:
        exception(e)

def wxlogin():
    window.geometry('400x500+400+100')
    login_frame = LoginFrame(window)
    login_frame.pack()
    wxbot = wx.Bot(qr_callback=login_frame.qr_callback, login_callback=login_frame.login_callback, logout_callback=logout_callback)
    wxbot.enable_puid('wxpy_puid.pkl')
    wxbot.core.send_video()
    init_user(wxbot)
    logger.info('%s login', util.filter_unicode(wxbot.self.name))
    login_frame.destroy()
    return wxbot

def show_main(wxbot):
    global main_frame
    groups = parse_group(wxbot, encoding)
    templates = parse_template()
    window.geometry('1080x680+200+50')
    main_frame = MainFrame(window, wxbot, groups, templates, send_period=config.getint('basic', 'send.period'), thumbnail=config.getboolean('basic', 'send.thumbnail'))
    main_frame.grid()

def logout_callback():
    if main_frame:
        main_frame.destroy()
    window.geometry('400x400+400+100')
    lb = tk.Label(window, text='您已退出登录，请:')
    lb.grid(row=0, column=0)
    def relogin():
        lb.destroy()
        logout_btn.destroy()
        threading.Thread(target=start_wxgroup, daemon=True).start()
    logout_btn = tk.Button(window, text='重新登录', command=relogin)
    logout_btn.grid(row=0, column=1)

def exception(e):
    logger.warning('exception:', exc_info=e)
    window.geometry('600x500+400+100')
    text = tk.Text(window, width=400, height=400)

    if isinstance(e, ConnectionError):
        text.insert(tk.END, '网络异常，请检查网络并重新启动:\n' + str(e))
    else:
        text.insert(tk.END, '程序启动失败，请与管理员联系并报告以下异常信息:\n' + str(e) + '\n' + traceback.format_exc())

    text.grid(row=0, column=0)

def check_licence():
    end_date = '2018-06-18 00:00:00'
    if not util.check_licence() and util.get_net_time() > end_date:
        window.geometry('400x400+400+100')
        lb = tk.Label(window, text='程序试用己到期，请与管理员联系!')
        lb.grid(row=0, column=0)
        return False
    return True

def start_wxgroup():
    try:
        logger.info('starting...')
        wxbot = wxlogin()
        show_main(wxbot)
        logger.info('started')
    except Exception as e:
        exception(e)


start()

tk.mainloop()
