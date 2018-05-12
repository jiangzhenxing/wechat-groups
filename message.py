# coding=utf-8
"""
消息发送界面
"""

import tkinter as tk
import logging
import traceback
import util
from tkinter import ttk, font, filedialog
from template import Template

PIC_FORMAT = {'jpeg','jpg','gif','png'}
VIDEO_FORMAT = {'mp4'}
logger = logging.getLogger('app')

class MessageFrame(tk.Frame):
    def __init__(self, master, wxbot, templates, send_method, stop_send_method, width=300, height=500):
        tk.Frame.__init__(self, master)
        self.wxbot = wxbot
        self.send_method = send_method
        self.stop_send_method = stop_send_method
        tk.Label(self, text='您好, %s(%s)' % (wxbot.self.name, wxbot.self.puid), padx=5, pady=5).grid(row=0, column=0)
        logout = tk.Label(self, text='退出', cursor='hand2', padx=5)
        logout.grid(row=0, column=0, columnspan=3, sticky=tk.E)
        logout.bind('<Button-1>', lambda e: wxbot.logout())
        book = ttk.Notebook(self, width=width, height=height)
        texts = [tk.Text(book) for _ in templates]
        for text,template in zip(texts,templates):
            text.insert(tk.END, template.content)
            book.add(text, text=template.name, sticky=tk.N + tk.E + tk.S + tk.W)
        book.grid(row=1, column=0, columnspan=3, sticky=tk.E+tk.W+tk.N+tk.S)
        self.texts = texts
        self.book = book

        # 文件选择
        self.file_path = tk.StringVar()
        self.file_entry = tk.Entry(self, textvariable=self.file_path, width=25)
        self.file_entry.grid(row=2, column=0, sticky=tk.W)
        tk.Button(master=self, text='选择', command=self.select_file).grid(row=2, column=1, sticky=tk.W)

        # 发送按扭
        self.send_btn_text = tk.StringVar(value='发送')
        self.send_btn = tk.Button(self, textvariable=self.send_btn_text, command=self.send_massage, width=8, bg='#DDD')
        self.send_btn.grid(row=2, column=2, sticky=tk.E, pady=10) #.pack(side=tk.RIGHT, pady=10)

        # 消息提示
        self._infomation = '消息提示'
        self.infomation = tk.StringVar(master=self, value=self._infomation[:21])
        self.info_label = tk.Label(master=self, textvariable=self.infomation, width=32, height=2, cursor='hand2', fg='#555', font=font.Font(size=12))
        self.info_label.bind('<Button-1>', lambda e:self.show_info_detail())
        self.info_label.grid(row=3, column=0, columnspan=3, sticky=tk.W, padx=5)  # .pack(side=tk.LEFT, padx=5)

    def send_massage(self):
        """
        前缀 部分可为: ‘@fil@’, ‘@img@’, ‘@msg@’, ‘@vid@’ (不含引号)
        """
        try:
            if self.send_btn_text.get() == '发送':
                filepath = self.file_path.get()
                content = self.get_content().strip()
                if filepath:
                    suffix = util.suffix(filepath)
                    if suffix in PIC_FORMAT:
                        filepath = util.thumbnail(filepath)
                        content = '@img@' + filepath
                    elif suffix in VIDEO_FORMAT:
                        content = '@vid@' + filepath
                    else:
                        content = '@fil@' + filepath
                    media_id = self.wxbot.upload_file(path=filepath)
                    self.send_method(content=content, media_id=media_id)
                elif content != '':
                    self.send_method(content=content)
                    self.send_btn_text.set('停止发送')
                else:
                    self.show_info('请填写要发送的消息！', 'red')
            elif self.send_btn_text.get() == '停止发送':
                self.stop_send_method()
        except Exception as e:
            self.show_info('发送失败:' + str(e) + '\n' + traceback.format_exc(), fg='red')
            logger.warning('发送信息出现异常：', exc_info=e)
            self.reset()

    def reset(self):
        self.send_btn_text.set('发送')
        self.file_path.set('')

    def get_content(self):
        current = self.book.index('current')
        return self.texts[current].get('1.0', tk.END)

    def select_file(self):
        f = filedialog.askopenfilename()
        if f:
            self.file_path.set(f)
            self.file_entry.index(len(f)-10)

    def show_info(self, info, fg='#555'):
        self._infomation = info
        self.infomation.set(util.substr(info.replace('\n', ''), 30))
        self.info_label.configure(fg=fg)

    def clear_info(self):
        self.infomation.set('')

    def show_info_detail(self):
        info_detail = tk.Toplevel(self)
        info_detail.geometry('400x420+400+100')
        info_detail.title('信息详情')
        text = tk.Text(info_detail, width=400, height=400)
        text.insert(tk.END, self._infomation)
        text.pack()


def main():
    root = tk.Tk()
    root.geometry('600x720+120+50')
    root.resizable(width=False, height=False)

    templates = [Template('Temp'+str(i), 'Content  Content ContentContent ' + str(i)) for i in range(3)]

    frame = MessageFrame(root, '姜', templates, None, None)
    frame.pack(side=tk.LEFT)

    # tk.Button(root, text='获取选择的群', command=lambda:print(gframe.get_selected())).pack()
    # tk.Button(root, text='search', command=lambda:print(gframe.search(keyword='1'))).pack()

    tk.mainloop()


if __name__ == '__main__':
    main()