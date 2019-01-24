# _*_ coding: utf-8 _*_
__author__ = 'ife'
__date__ = '2019-01-24 21:47'

import json
import requests


class YunPian(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):
        parmas = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "【电商网】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }

        response = requests.post(self.single_send_url, data=parmas)
        re_dirc = json.loads(response.text)
        return re_dirc


if __name__ == "__main__":
    yun_pian = YunPian("")
    yun_pian.send_sms("2019", "")
