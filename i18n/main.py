'''
Author: iptoday wangdong1221@outlook.com
Date: 2022-07-21 19:42:48
LastEditors: iptoday wangdong1221@outlook.com
LastEditTime: 2022-12-22 14:25:55
FilePath: /i18n/main.py

Copyright (c) 2022 by iptoday wangdong1221@outlook.com, All Rights Reserved. 
'''


import operator
import json
import os
import sys
from googletrans import Translator

errors = []


def main():
    print('开始')
    config = sys.argv[1]
    output = sys.argv[2]
    original = output+'/strings.json'
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
        path = output+'/'+cj_item['locale']+'.json'
        ignore = ['en']
        if cj_item['locale'] in ignore or os.path.exists(path):
            print('%s已存在' % cj_item['zh'])
            continue
        result = {}
        for oj_key in original_json:
            val = ''
            if oj_key == 'title':
                val = original_json[oj_key]
            elif oj_key == 'locale':
                val = cj_item['locale']
            elif oj_key == 'raw':
                val = cj_item['title']
            elif oj_key == 'chinese':
                val = cj_item['zh']
            else:
                val = translation(
                    original_json['locale'],
                    original_json[oj_key],
                    cj_item['locale']
                )
            result[oj_key] = val
        with open(path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(result, ensure_ascii=False))
            f.close()
    print('翻译结束')


def translation(src, value, dest):
    '''
    翻译单元
    '''
    print(type(value))
    if type(value) == str:
        print('当前处理内容: %s' % value)
        if value == "" or value == "/":
            return value
        try:
            contains = operator.contains(value, '$value')
            if contains:
                value = value.replace('$value', '3')
            translator = Translator()
            result = translator.translate(value, src=src, dest=dest).text
            if contains:
                print('当前内容存在变量')
                result = result.replace('3', '$value')
            return result
        except:
            errors.append({'value': value, 'code': dest})
            print('翻译失败: %s des:%s' % (value, dest))
            return value
    elif type(value) == dict:
        d = {}
        for key in value:
            d[key] = translation(src, value[key], dest)
        return d
    elif type(value) == list:
        l = []
        for element in value:
            l.append(translation(src, element, dest))
        return l


if __name__ == "__main__":
    main()
    print('翻译失败的内容: %s' % errors)
