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
    try:
        templates = [Template('停电信息', util.read_text(util.DEFAULT_TD_INFO))]
        for fname in os.listdir(util.TEMPLATE_PATH):
            try:
                templates.append(Template(name=fname[:fname.rfind('.')] if '.' in fname else fname, content=util.read_text(util.TEMPLATE_PATH+os.path.sep+fname)))
            except Exception as ee:
                raise Exception('解析模板信息出现异常，请检查: ' + fname, ee)
        templates.append(Template('新建', ''))
        return templates
    except Exception as e:
        raise Exception('解析模板信息出现异常', e)


def test_parse_template():
    for t in parse_template():
        print()
        print('-' * 100)
        print(t.name)
        print(t.content)


if __name__ == '__main__':
    test_parse_template()