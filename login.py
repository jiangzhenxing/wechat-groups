# coding=utf-8
"""
登录界面
"""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import wxpy as wx
import io
import threading
import time



class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.info = tk.Label(self, text='请用手机微信扫描以下二维码并确认登录', font=('Arial', 14), width=35, height=4)
        self.info.pack()
        self.label_qr = tk.Label(self)
        self.label_qr.pack()
        self.n = 0

    def qr_callback(self, uuid, status, qrcode):
        global img_qr
        self.n += 1
        colors = ['green', 'red', 'blue']
        # print(uuid, status, qrcode, sep='\t')
        code = io.BytesIO(qrcode)
        img = Image.open(code)
        # print(img.size)
        img = img.resize((300, 300), Image.ANTIALIAS)
        # img.show()
        img_qr = ImageTk.PhotoImage(img)
        code.close()
        # qr_img.save('qrcode2.png')
        # print(self.label_qr)
        # time.sleep(1)
        self.label_qr.configure(image=img_qr)
        c = self.n % 3
        # print('color is:', c)
        self.label_qr.configure(background=colors[c])

    def login_callback(self):
        # print('seccess login!')
        self.info.configure(text='登录成功')


def start(qr_callback, login_callback):
    bot = wx.Bot(qr_callback=qr_callback, login_callback=login_callback)
    for g in bot.groups():
        print(g)
    return bot

def login_callback():
    print('log in.')

def main():
    window = tk.Tk()
    window.title('微信群管理')
    window.geometry('400x500')
    f = LoginFrame(window)
    f.pack()
    threading.Thread(target=start, args=(f.qr_callback, f.login_callback), daemon=True).start()
    print('------------------------')
    tk.mainloop()

if __name__ == '__main__':
    main()
