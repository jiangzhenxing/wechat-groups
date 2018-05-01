import os
import logging.config

WORDS1 = set(list('`1234567890-=qwertyuiop[]\\asdfghjkl;\'zxcvbnm,./~!@#$%^&*()_+{}|:"<>?'))

def substr(string, width):
    """
    截取固定显示宽度的字符，WORDS1中的字符宽度为1，汉字宽度为1.3
    """
    w = 0
    i = 0
    for i,c in enumerate(string):
        w += 1 if c in WORDS1 else 1.3
        if w > width:
            i -= 1
            break
    # print(w, width, i)
    return string[:i+1]

def read_text(file):
    with open(file) as f:
        return f.read(os.path.getsize(file))

def init():
    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.exists(template_path):
        os.mkdir(template_path)
    if not os.path.exists('logs'):
        os.mkdir('logs')

def init_user(wxbot):
    path = user_path(wxbot)
    if not os.path.exists(path):
        os.mkdir(path)

user_path = lambda wxbot: 'data/' + wxbot.self.puid
template_path = 'data/templates'

help_message = \
"""
1. 第一次登录本系统时，会把你的所有群列表保存在'data/@puid(名称后面括号里的字母)/groups.csv'中，

   可以使用excel打开编辑，输入变电站等信息，保存时重新导出并覆盖原'groups.csv'文件。
   
2. 消息模板在 'data/templates/' 文件夹中，一个txt文件即一个模版，可以直接用记事本打开编辑。

3. 要发送消息的群请在手机微信群设置中，选中'保存到通讯录'，否则本系统可能获取不到。

4. 如果刚打开群管理应用时，发现某个群背景为红色，刚说明该群找不到。

   请确认该群名称正确且已经保存到了通讯录中，如果不需要可以在'groups.csv'中将其删除。

5. 为了避免因消息发送过快导致的问题，所以本应用每发送一条消息需要等待1~2秒的时间。
"""

def main():
    pass

if __name__ == '__main__':
    main()