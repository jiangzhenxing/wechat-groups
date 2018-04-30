import tkinter as tk
import time
import threading
import traceback
import random
import logging
from tkinter import font
from message import MessageFrame
from search import parse_group_dict, SearchFrame
from groups import Group,GroupFrame
from template import Template

logger = logging.getLogger('app')

class MainFrame(tk.Frame):
    """
    群管理主界面
    """
    def __init__(self, master, wxbot, groups, templates, **cnf):
        super().__init__(master, **cnf)
        self.wxbot = wxbot
        tk.Label(master=self, text='欢迎使用微信群管理系统', width=32, fg='#333', font=font.Font(size=16, family='黑体', weight='bold')).grid(row=0, column=0, sticky=tk.S, pady=5)
        self.mframe = MessageFrame(self, wxbot.self.name, templates, self.send_message, self.stop_send)
        self.mframe.grid(row=1, column=0)
        self.gframe = GroupFrame(self, groups)
        self.gframe.grid(row=1, column=1)
        self.sframe = SearchFrame(self, *parse_group_dict(groups), group_frame=self.gframe)
        self.sframe.grid(row=0, column=1, sticky=tk.W)
        self.stop_send_flag = False

    def send_message(self, message):
        print('MainFrame:', message)
        groups = self.gframe.get_selected()
        self.gframe.reset()
        self.stop_send_flag = False
        threading.Thread(target=self._send, args=(message, groups), daemon=True).start()

    def _send(self, message, groups):
        n_succ = 0
        n_fail = 0
        for g in groups:
            try:
                if self.stop_send_flag:
                    break
                self.mframe.show_info('正在发送:' + g.name)
                # g.send_msg(message)
                print('发送成功:', g.name, ':' + message)
                g.row.set_bgcolor('green')
                n_succ += 1
                time.sleep(2 + random.random())
            except Exception as e:
                self.show_info('发送失败:' + str(e) + '\n' + traceback.format_exc(), color='red')
                logger.warning('发送信息出现异常：', exc_info=e)
                g.row.set_bgcolor('red')
                n_fail += 1
        self.mframe.show_info('发送成功:' + str(n_succ) + ', 发送失败:' + str(n_fail))
        self.mframe.reset()

    def stop_send(self):
        self.stop_send_flag = True

    def show_info(self, info, color):
        self.mframe.show_info(info, fg=color)


def main():
    root = tk.Tk()
    root.geometry('890x680+120+50')
    root.resizable(width=False, height=False)

    groups = [Group('变电所变电所aaa' + str(i), '主经路主aaabbbb' + str(i), '分支线路分支线路支线路' + str(i), '群名称群名称名称aaaaaa' + str(i)) for i in range(60)]
    templates = [Template('Temp' + str(i), 'Content  Content ContentContent ' + str(i)) for i in range(3)]
    class WxBot: pass
    wxbot = WxBot()
    wxbot.self = WxBot()
    wxbot.self.name = '姜'
    frame = MainFrame(root, wxbot, groups, templates)
    frame.pack()

    # tk.Button(root, text='获取选择的群', command=lambda: print(gframe.get_selected())).pack()
    # tk.Button(root, text='search', command=lambda: print(gframe.search(keyword='1'))).pack()

    tk.mainloop()

if __name__ == '__main__':
    main()
