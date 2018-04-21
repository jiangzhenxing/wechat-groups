"""
消息发送界面
"""

import tkinter as tk
from tkinter import ttk

from template import Template

class MessageFrame(tk.Frame):
    def __init__(self, master, templates):
        tk.Frame.__init__(self, master)
        sticky = tk.N + tk.E + tk.S + tk.W
        book = ttk.Notebook(self, width=300, height=400)
        texts = [tk.Text(book) for _ in templates]
        for text,template in zip(texts,templates):
            text.insert(tk.END, template.content)
            book.add(text, text=template.name, sticky=sticky)
        book.pack(side=tk.TOP)
        self.texts = texts
        self.book = book
        tk.Button(self, text='发送', command=self.send, width=8, bg='#DDD').pack(side=tk.RIGHT, pady=5)

    def send(self):
        message = self.get_content()
        print(message)

    def get_content(self):
        current = self.book.index('current')
        return self.texts[current].get('1.0', tk.END)


def main():
    root = tk.Tk()
    root.geometry('600x720+120+50')
    root.resizable(width=False, height=False)

    templates = [Template('Temp'+str(i), 'Content  Content ContentContent ' + str(i)) for i in range(3)]

    frame = MessageFrame(root, templates)
    frame.pack(side=tk.LEFT)

    # tk.Button(root, text='获取选择的群', command=lambda:print(gframe.get_selected())).pack()
    # tk.Button(root, text='search', command=lambda:print(gframe.search(keyword='1'))).pack()

    tk.mainloop()


if __name__ == '__main__':
    main()