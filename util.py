# coding=utf-8

import os
import io
import requests
from PIL import Image

DATA_PATH = 'data/'
TEMPLATE_PATH = DATA_PATH + 'templates/'
THUMBNAIL_PATH = DATA_PATH + 'thumbnail/'
LOG_PATH = DATA_PATH + 'logs/'
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
    with open(file, encoding='utf-8') as f:
        return f.read(os.path.getsize(file))

def init():
    if not os.path.exists(DATA_PATH):
        os.mkdir(DATA_PATH)
    if not os.path.exists(TEMPLATE_PATH):
        os.mkdir(TEMPLATE_PATH)
    if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)
    if not os.path.exists(THUMBNAIL_PATH):
        os.mkdir(THUMBNAIL_PATH)
    clear_thumbnail()

def init_user(wxbot):
    path = user_path(wxbot)
    if not os.path.exists(path):
        os.mkdir(path)

def user_path(wxbot):
    return DATA_PATH + wxbot.self.puid


def suffix(filename):
    return filename[filename.rfind('.')+1:].lower()

def get_net_time():
    return requests.get('http://cgi.im.qq.com/cgi-bin/cgi_svrtime').text.strip()

def valid_licence():
    return os.path.exists('data/__licence__')

def thumbnail(img_path):
    target_size = 500 * 1000
    filesize = os.path.getsize(img_path)
    if filesize > target_size:
        img = Image.open(img_path)
        while True:
            x,y = img.size
            x,y = int(0.9 * x), int(0.9 * y)
            img.thumbnail((x,y))
            bytes = io.BytesIO()
            img.save(bytes, 'jpeg')
            data_len = len(bytes.getvalue())
            bytes.close()
            if data_len < target_size:
                break
        img_path = THUMBNAIL_PATH + os.path.basename(img_path)
        img.save(img_path, 'jpeg', exif=img.info['exif'])
    print(img_path)
    return img_path

def remove_thumbnail(filepath):
    if filepath.startswith(THUMBNAIL_PATH):
        os.remove(filepath)

def clear_thumbnail():
    for f in os.listdir(THUMBNAIL_PATH):
        os.removedirs(THUMBNAIL_PATH + os.path.sep + f)

help_message = \
"""
1. 第一次登录本系统时，会把你的所有群列表保存在'data/@puid(名称后面括号里的字母)/groups.csv'中，

   可以使用excel 或WPS打开，输入变电站等信息，保存时重新导出CSV格式的文件并覆盖原'groups.csv'。
   
2. 消息模板在 'data/templates/' 文件夹中，一个txt文件即一个模版，可以直接用记事本打开编辑。

3. 要发送消息的群请在手机微信群设置中，选中'保存到通讯录'，否则本系统可能获取不到。

4. 如果刚打开群管理应用时，发现某个群背景为红色，刚说明该群找不到。

   请确认该群名称正确且已经保存到了通讯录中，如果不需要可以在'groups.csv'中将其删除。

5. 为了避免因消息发送过快导致的问题，所以每发送一条消息需要等待几秒钟时间。

6. 发送图片的格式为: 'jpeg','jpg','gif','png'，视频格式为：mp4

7. 受限于微信WEB接口，目前只能发送小于500K的图片或文件，发送大文件很可能失败。
"""

def main():
    print(suffix('aajpg'))

if __name__ == '__main__':
    main()