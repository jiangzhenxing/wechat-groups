# coding=utf-8

import os
import io
import logging.config
import requests
from PIL import Image
from os import path

logger = logging.getLogger('app')

DATA_PATH = 'data'
USER_PATH = DATA_PATH + path.sep + 'user'
TEMPLATE_PATH = DATA_PATH + path.sep + 'templates'
THUMBNAIL_PATH = DATA_PATH + path.sep+ 'thumbnail'
LOG_PATH = DATA_PATH + path.sep + 'logs'
WORDS1 = set(list('`1234567890-=qwertyuiop[]\\asdfghjkl;\'zxcvbnm,./~!@#$%^&*()_+{}|:"<>?'))

encoding = 'utf-8'

def filter_unicode(s):
    return ''.join(filter(lambda x: u'\u0000' < x < '\uffff', s))

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
    logger.info(encoding)
    with open(file, encoding=encoding) as f:
        return f.read(os.path.getsize(file))

def init():
    if not os.path.exists(DATA_PATH):
        os.mkdir(DATA_PATH)
    if not os.path.exists(USER_PATH):
        os.mkdir(USER_PATH)
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
    return USER_PATH + path.sep + filter_unicode(wxbot.self.name)

def suffix(filename):
    return filename[filename.rfind('.')+1:].lower()

def get_net_time():
    return requests.get('http://cgi.im.qq.com/cgi-bin/cgi_svrtime').text.strip()

def valid_licence():
    return os.path.exists('data/__licence__')

def thumbnail(img_path):
    target_size = 500 * 1000
    quality = 95
    filesize = os.path.getsize(img_path)
    if filesize > target_size:
        img = Image.open(img_path)
        while True:
            x,y = img.size
            logger.info('img size: %d,%d', x, y)
            if x > 2000 or y > 2000:
                x = min(x, 2000)
                y = min(y, 2000)
            else:
                x,y = int(0.8 * x), int(0.8 * y)
            img.thumbnail((x,y))
            with io.BytesIO() as buffer:
                img.save(buffer, 'jpeg', exif=img.info['exif'], quality=quality)
                if len(buffer.getvalue()) < target_size:
                    img_path = THUMBNAIL_PATH + path.sep + os.path.basename(img_path)
                    with open(img_path, 'wb') as f:
                        f.write(buffer.getvalue())
                    break
    logger.info(img_path)
    return img_path

def clear_thumbnail():
    for f in os.listdir(THUMBNAIL_PATH):
        os.remove(THUMBNAIL_PATH + path.sep + f)

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

def test_thumbnail():
    pictures = ['20160507_154045.jpg', '20160915_133444.jpg', '20160916_085707.jpg', '20151004_133144.jpg']
    for pic in pictures:
        thumbnail('/Users/jiangzhenxing/Pictures/' + pic)

def main():
    logging.config.fileConfig('config/logging.conf')
    test_thumbnail()

if __name__ == '__main__':
    main()