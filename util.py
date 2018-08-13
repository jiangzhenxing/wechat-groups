# coding=utf-8

import os
import io
import logging.config
import requests
import time
import configparser
from PIL import Image
from os import path

logger = logging.getLogger('app')

GROUP_PATH = '微信群信息'
TEMPLATE_PATH = '信息模版'
TD_PATH = '停电信息'
DEFAULT_TD_INFO = TD_PATH + path.sep + '默认.txt'

DATA_PATH = 'data'
USER_PATH = DATA_PATH + path.sep + 'user'
THUMBNAIL_PATH = DATA_PATH + path.sep+ 'thumbnail'
LOG_PATH = DATA_PATH + path.sep + 'logs'
TMP_PATH = DATA_PATH + path.sep + 'tmp'

WORDS1 = set(list('`1234567890-=qwertyuiop[]\\asdfghjkl;\'zxcvbnm,./~!@#$%^&*()_+{}|:"<>?'))

encoding = 'gbk'
thumbnail_target = 500000

def filter_unicode(s):
    return ''.join(filter(lambda x: u'\u0000' < x < '\uffff', s))

def has_not_unicode(s):
    for x in s:
        if not u'\u0000' < x < '\uffff':
            return True
    return False

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
    if not path.exists(file):
        logger.info('%s not exist', file)
        return ""
    with open(file, encoding=encoding) as f:
        return f.read(os.path.getsize(file))

def init():
    global encoding, thumbnail_target
    config = configparser.ConfigParser()
    config.read('config/app.ini')
    encoding = config.get('basic', 'encoding', fallback=None)
    thumbnail_target = config.getint('basic', 'thumbnail.target', fallback=500000)

    create_dir(GROUP_PATH)
    create_dir(TEMPLATE_PATH)
    create_dir(TD_PATH)

    create_dir(DATA_PATH)
    create_dir(USER_PATH)
    create_dir(LOG_PATH)
    create_dir(THUMBNAIL_PATH)
    create_dir(TMP_PATH)

    clear()

def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

def init_user(wxbot):
    userpath = user_path(wxbot)
    create_dir(userpath)

def user_path(wxbot):
    return USER_PATH + path.sep + filter_unicode(wxbot.self.name)

def suffix(filename):
    return filename[filename.rfind('.')+1:].lower()

def basename(filename):
    end = filename.rfind('.')
    if end < 0:
        return filename
    return filename[0:end]

def get_net_time():
    return requests.get('http://cgi.im.qq.com/cgi-bin/cgi_svrtime').text.strip()

def check_licence():
    return os.path.exists('data/__licence__')

def thumbnail(img_path):
    target_size = thumbnail_target
    logger.info('target_size: %s', target_size)
    quality = 95
    filesize = os.path.getsize(img_path)
    if filesize > target_size:
        img = Image.open(img_path)
        while True:
            x,y = img.size
            logger.info('img size: %d,%d', x, y)
            if x > 1600 or y > 1600:
                x = min(x, 1600)
                y = min(y, 1600)
            else:
                x,y = int(0.8 * x), int(0.8 * y)
            img.thumbnail((x,y))
            with io.BytesIO() as buffer:
                img.save(buffer, 'jpeg', exif=img.info['exif'], quality=quality)
                if len(buffer.getvalue()) < target_size:
                    img_path = THUMBNAIL_PATH + path.sep + str(int(time.time() * 1000)) + '.jpeg'
                    with open(img_path, 'wb') as f:
                        f.write(buffer.getvalue())
                    break
    logger.info(img_path)
    return img_path

def clear():
    for f in os.listdir(THUMBNAIL_PATH):
        os.remove(THUMBNAIL_PATH + path.sep + f)
    for f in os.listdir(TMP_PATH):
        os.remove(TMP_PATH + path.sep + f)

help_message = \
"""
1. 第一次登录本系统时，会把你的所有群列表保存在'微信群信息/你的微信名.csv'中，

   可以使用 WPS 编辑，输入变电站等信息，然后保存。
   
2. 停电信息在'停电信息'文件夹中，txt 格式，文件名与分支线路相同，

   搜索微信群时会自动找到相应分支线路的停电信息。

3. 消息模板在 '信息模版' 文件夹中，一个txt文件即一个模版，可以直接用记事本打开编辑。

4. 要发送消息的群请在手机微信群设置中，选中'保存到通讯录'，否则本系统可能获取不到。

5. 如果刚打开群管理应用时，发现某个群背景为红色，刚说明该群找不到。

   请确认该群名称正确且已经保存到了通讯录中，如果不需要可以在'groups.csv'中将其删除。

6. 为了避免因消息发送过快导致的问题，所以每发送一条消息需要等待几秒钟时间。

7. 发送图片的格式为: 'jpeg','jpg','gif','png'

8. 受限于微信WEB接口，目前只能发送小于500K的图片或文件，发送大文件很可能失败。

9. 发送消息时优先发送文件，没有选择文件时发送文本消息。
"""

def test_thumbnail():
    pictures = ['20160507_154045.jpg', '20160915_133444.jpg', '20160916_085707.jpg', '20151004_133144.jpg']
    for pic in pictures:
        thumbnail('/Users/jiangzhenxing/Pictures/' + pic)

def main():
    # logging.config.fileConfig('config/logging.conf')
    # test_thumbnail()
    print(check_licence())

if __name__ == '__main__':
    main()