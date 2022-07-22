'''
Author: iptoday wangdong1221@outlook.com
Date: 2022-07-21 19:42:48
LastEditors: iptoday wangdong1221@outlook.com
LastEditTime: 2022-07-21 23:53:17
FilePath: /i18n/main.py

Copyright (c) 2022 by iptoday wangdong1221@outlook.com, All Rights Reserved. 
'''


import json
import os
import sys
from time import sleep
from googletrans import Translator


def main():
    print('开始')
    config = sys.argv[1]
    output = sys.argv[2]
    original = output+'/strings_zh-CN.i18n.json'
    print('配置文件路径: %s' % config)
    print('输出文件夹路径: %s' % output)
    with open(config, 'r') as f:
        config_json = json.load(f)
        f.close()
    with open(original, 'r') as f:
        original_json = json.load(f)
        f.close()
    for cj_item in config_json:
        print('当前正在处理: %s' % cj_item['zh'])
        path = output+'/strings_'+cj_item['locale']+'.i18n.json'
        if cj_item['locale'] == 'en' or os.path.exists(path):
            print('%s已存在' % cj_item['zh'])
            continue
        result = {}
        for oj_key in original_json:
            result[oj_key] = translation(
                original_json[oj_key],
                cj_item['locale']
            )
        with open(path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(result, ensure_ascii=False))
            f.close()
    print('翻译结束')


def translation(value, dest, index=1):
    '''
    翻译单元
    '''
    if type(value) == str:
        print('当前处理内容: %s' % value)
        # sleep(5)
        try:
            translator = Translator()
            return translator.translate(value, src='zh-CN', dest=dest).text
        except:
            sleep(index*5)
            return translation(value, dest, index+1)
    elif type(value) == dict:
        d = {}
        for key in value:
            d[key] = translation(value[key], dest)
        return d
    elif type(value) == list:
        l = []
        for element in value:
            l.append(translation(element, dest))
        return l


if __name__ == "__main__":
    main()
