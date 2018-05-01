# coding=utf-8
import os
import util

class Template:
    """
    消息模版
    """
    def __init__(self, name, content):
        self.name = name
        self.content = content


def parse_template():
    """
    从文件中解析模板
    """
    templates = [Template('新建', '')]
    for fname in os.listdir(util.template_path):
        templates.append(Template(name=fname[:fname.rfind('.')] if '.' in fname else fname, content=util.read_text('data/templates/'+fname)))
    return templates


def test_parse_template():
    for t in parse_template():
        print()
        print('-' * 100)
        print(t.name)
        print(t.content)


if __name__ == '__main__':
    test_parse_template()