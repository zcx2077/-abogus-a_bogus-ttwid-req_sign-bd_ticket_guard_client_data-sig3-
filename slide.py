# -*- coding: utf-8 -*-
import re

from PIL import Image
import uvicorn
from fastapi import FastAPI, Response
from pydantic import BaseModel
import uuid
import httpx
import base64
import random
from PIL import Image
import json
import time
from pathlib import Path
import PIL
import cv2
import numpy as np
import requests
from Crypto.Cipher import AES
from Crypto.Hash import SHA512
import base64
import ctypes
import functools
import json
import random
import string
import time
from urllib.parse import urlencode
import ctypes
import math
import random
import time

class Dy:
    def __init__(self, ip):
        self.comment_fp_url = "https://www.douyin.com/aweme/v1/web/comment/list/"
        self.captcha_url = "https://verify.snssdk.com/captcha/get"
        self.verify_captcha_url = 'https://verify.zijieapi.com/captcha/verify'
        self.video_fp_url = "https://www.douyin.com/aweme/v1/web/aweme/post/"
        if ip != '':
            self.proxies = {
                'http://': 'http://' + ip,
                'https://': 'http://' + ip
            }
        else:
            self.proxies = None
        self.uuid = uuid.uuid4()

        self.main_filename = f"img/puzzle/{self.uuid}.jpeg"
        self.small_filename = f"img/piece/{self.uuid}.jpeg"
        self.http2 = httpx.Client(http2=True, proxies=self.proxies)


    def get_img(self, verify_data):
        headers = {
            'authority': 'p3-catpcha.byteimg.com',
            'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache-control': 'no-cache',
            'origin': 'https://rmc.bytedance.com',
            'pragma': 'no-cache',
            'referer': 'https://rmc.bytedance.com/',
            'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'image',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        }
        # params = {
        #     "lang": "zh",
        #     "app_name": "",
        #     "h5_sdk_version": "3.5.56",
        #     "sdk_version": "3.5.2",
        #     "iid": "0",
        #     "did": "0",
        #     "device_id": "0",
        #     "ch": "web_text",
        #     "aid": "6383",
        #     "os_type": "2",
        #     "mode": "",
        #     "tmp": str(int(time.time() * 1000)),
        #     "platform": "pc",
        #     "webdriver": "false",
        #     "fp": verify_data['fp'],
        #     "type": "verify",
        #     "detail": verify_data['detail'],
        #     "server_sdk_env": '{"idc":"hl","region":"CN","server_type":"whale"}',
        #     "subtype": verify_data['subtype'],
        #     "challenge_code": "99999",
        #     "os_name": "windows",
        #     "h5_check_version": "3.5.2"
        # }
        params = (
            ('aid', '6383'),
            ('lang', 'zh'),
            ('subtype', 'slide'),
            ('detail',
             verify_data['detail']),
            ('server_sdk_env', '/{"idc":"lq","region":"CN","server_type":"whale"/}'),
            ('mode', 'slide'),
            ('fp', verify_data['fp']),
            ('h5_check_version', '3.5.2'),
            ('os_name', 'windows'),
            ('platform', 'pc'),
            ('os_type', '2'),
            ('h5_sdk_version', '3.5.56'),
            ('webdriver', 'false'),
            ('tmp', str(int(time.time() * 1000))),
        )

        response = self.http2.get(self.captcha_url, headers=headers, params=params).json()
        if response['code'] == 200:
            return response['data']

    def fp(self):
        e = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        t = len(e)
        milliseconds = int(round(time.time() * 1000))
        base36 = ''
        while milliseconds > 0:
            remainder = milliseconds % 36
            if remainder < 10:
                base36 = str(remainder) + base36
            else:
                base36 = chr(ord('a') + remainder - 10) + base36
            milliseconds = int(milliseconds / 36)
        r = base36
        o = [''] * 36
        o[8] = o[13] = o[18] = o[23] = '_'
        o[14] = '4'
        for i in range(36):
            if not o[i]:
                n = 0 or int(random.random() * t)
                if i == 19:
                    n = 3 & n | 8
                o[i] = e[n]
        ret = "verify_" + r + "_" + ''.join(o)
        return ret

    # def origin(self, img):
    #     # 打开原始图片
    #     image = Image.open(io.BytesIO(img))
    #     # 定义切割参数
    #     width = 92
    #     height = 344
    #     num_slices = 6
    #     slice_order = [5, 1, 4, 6, 3, 2]
    #     # 创建一个空白的拼接图片
    #     result_image = Image.new('RGB', (width * num_slices, height))
    #     # 切割并拼接图片
    #     for i, slice_index in enumerate(slice_order):
    #         # 计算切割的起始和结束位置
    #         start_x = (slice_index - 1) * width
    #         end_x = slice_index * width
    #
    #         # 切割图片
    #         slice_image = image.crop((start_x, 0, end_x, height))
    #
    #         # 将切割后的图片拼接到结果图片上
    #         result_image.paste(slice_image, (i * width, 0))
    #     # 保存拼接后的图片
    #     buffer = io.BytesIO()
    #     result_image.save(buffer, format='JPEG')
    #     binary_data = buffer.getvalue()
    #     # 返回二进制数据
    #     return binary_data
        # return result_image




    def verify(self, captcha_body, verify_data, data):
        headers = {
            'authority': 'verify.snssdk.com',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache-control': 'no-cache',
            'content-type': 'text/plain;charset=UTF-8',
            'origin': 'https://rmc.bytedance.com',
            'pragma': 'no-cache',
            'referer': 'https://rmc.bytedance.com/',
            'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        }
        # params = {
        #     "lang": "zh",
        #     # "app_name": "",
        #     "h5_sdk_version": "3.5.56",
        #     # "sdk_version": "3.8.6",
        #     # "iid": "0",
        #     # "did": "0",
        #     # "device_id": "0",
        #     "ch": "web_text",
        #     "aid": "6383",
        #     "os_type": "2",
        #     "mode": data['mode'],
        #     "tmp": str(int(time.time() * 1000)),
        #     "platform": "pc",
        #     "webdriver": "false",
        #     "type": "verify",
        #     "detail": verify_data['detail'],
        #     "server_sdk_env": '{"idc":"lq","region":"CN","server_type":"whale"}',
        #     "subtype": verify_data['subtype'],
        #     # "challenge_code": '99999',
        #     'fp':verify_data['fp'],
        #     "os_name": "windows",
        #     "h5_check_version": "3.8.6",
        #     "xx-tt-dd": "qJI7ttpVdGKKbSBvYqmaf0aPo"
        # }
        url=f"aid=6383&lang=zh&subtype={verify_data['subtype']}&detail={verify_data['detail']}&server_sdk_env=%7B%22idc%22%3A%22lq%22%2C%22region%22%3A%22CN%22%2C%22server_type%22%3A%22whale%22%7D&mode=slide&fp={verify_data['fp']}&h5_check_version=3.5.2&os_name=windows&platform=pc&os_type=2&h5_sdk_version=3.5.56&webdriver=false&tmp={str(int(time.time() * 1000))}&xx-tt-dd=qJI7ttpVdGKKbSBvYqmaf0aPo&msToken=Nw0F5oHRzu1F0BxQ48AtLQSNQuqGmn6qxREhWNZwIHXPt1biYVTB2xnOEm_WVjQ4U2bPFjRvo7NnLg5gy7RtDiF92g2nIj8igiXODlA_o6P4Nar8HMKi-ZLn9zDNVOjk"
        # ab = ABogus().getABogus(
        #     user_agent=headers['user-agent'], param=url
        #     , data=None)
        ab = getABogus(url, '', headers['user-agent'])

        params = (
            ('aid', '6383'),
            ('lang', 'zh'),
            ('subtype', verify_data['subtype']),
            ('detail',
             verify_data['detail']),
            ('server_sdk_env', '{"idc":"lq","region":"CN","server_type":"whale"}'),
            ('mode', 'slide'),
            ('fp', verify_data['fp']),
            ('h5_check_version', '3.5.2'),
            ('os_name', 'windows'),
            ('platform', 'pc'),
            ('os_type', '2'),
            ('h5_sdk_version', '3.5.56'),
            ('webdriver', 'false'),
            ('tmp', str(int(time.time() * 1000))),
            ('xx-tt-dd', 'qJI7ttpVdGKKbSBvYqmaf0aPo'),
            ('msToken',
             'Nw0F5oHRzu1F0BxQ48AtLQSNQuqGmn6qxREhWNZwIHXPt1biYVTB2xnOEm_WVjQ4U2bPFjRvo7NnLg5gy7RtDiF92g2nIj8igiXODlA_o6P4Nar8HMKi-ZLn9zDNVOjk'),
            ('a_bogus', ab),
        )
        # params = (
        #     ('aid', '6383'),
        #     ('lang', 'zh'),
        #     # ('repoId', '579047'),
        #     ('subtype', 'slide'),
        #     ('detail',
        #      verify_data['detail']),
        #     ('server_sdk_env', '{"idc":"lq","region":"CN","server_type":"whale"}'),
        #     ('mode', 'slide'),
        #     ("fp", verify_data['fp']),
        #     ('h5_check_version', '3.8.6'),
        #     ('os_name', 'windows'),
        #     ('platform', 'pc'),
        #     ('os_type', '2'),
        #     ('h5_sdk_version', '3.5.56'),
        #     ('webdriver', 'false'),
        #     ('tmp', str(int(time.time()*1000))),
        #     ('xx-tt-dd', 'qJI7ttpVdGKKbSBvYqmaf0aPo'),
        #     # ('msToken',
        #     #  'jwnLUS-q2c1lvCnVlNjP4SwWQhydOtEiAoIZNLMaM1cuFaz_A1XoUz950pX6mQvvnt24AboHAe67YwVvflzSArs_pyHUEtxElW9xC_zUKyeFpFp5s8BsKOJJgnuJNKk='),
        #     # ('a_bogus', 'D7BEfO26Msm16MVlm7kz9CK/h8y0YWR7gZEPJiPRf0oQ'),
        # )
        data = {
            "captchaBody": captcha_body
        }
        response = self.http2.post(self.verify_captcha_url, headers=headers, json=data, params=params)
        print(response.text)
        if response.json()['code']==200 and response.json()['message']=='验证通过':
            return True

    def run(self, detail, fp, subtype):

        verify_data = {'detail': detail, 'fp': fp, 'subtype': subtype}
        fp = verify_data['fp']
        data = self.get_img(verify_data)
        if subtype == "slide":
            time.sleep(3)
            value = get_distance(
                bg=requests.get(data['question']['url1']).content,
                tp=requests.get(data['question']['url2']).content,
                im_show=False,
                save_path=None
            )
            y = data['question']['tip_y']

            tt = get_track(int(value / 552 * 340), data['id'], y)
            captcha_body = captcha_encrypt(tt)

        result = self.verify(captcha_body, verify_data, data)
        if result:
            return fp



# app = FastAPI()
#
#
# class Item(BaseModel):
#     ip: str = None
#     detail: str = None
#     fp: str = None
#
#
# @app.post("/douyin")
# async def index20(item: Item):
#     item_dict = item.dict()
#     ip = item_dict['ip']
#     detail = item_dict['detail']
#     fp = item_dict['fp']
#     result = Dy(ip).run(detail, fp, 'slide')
#     return result
#
# if __name__ == '__main__':
#     config = uvicorn.config.Config(app, host="0.0.0.0", port=8866, loop="asyncio", workers=64)
#     server = uvicorn.Server(config)
#     server.run()
# result = Dy('').run(
#
# 'y80mbaoQH4zupIiI14CrOkvgVTXEvnJZkgfSLmFaQZtP8PIB2pqZixTAwibpRFVMzudgJW1uJK3F7Hl-UKX1bfwqwx6LZnsvcsTDdNi-pr*hYFNQTE*Mj4Cal9*Y8N3SZiX5HsJ5-NpWuF0ac4rh2W57Gafn3NP7JTcQJjjta2P*IwacDEfW2XsL1hGvuRBGmlJpb58vpeT26OwGqL1AMNbMD-o4oIhEeabzK5GD3fUBYe1riLk61F-9ZY4eTjTPAA5KceCAxoO4YKLqEI2E6RBQYfW-P4n0LZ2kN*2xGw*dpRjjPLK4nk9sDc6thNRSvqPds-ry-bqZfGQgnN*SOnjkWpVwWA1HZBVXmIEKtmXa7lvS3ylx7T0IjOXIYxSJBw4Hc0jdOJSzLpBGE4Bzk9kRYkwzlN2CAiY.'
#                     ,'3620033887498343', 'slide')

while 1:
    import requests
    headers = {
        'authority': 'www.douyin.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'cookie': ' __ac_referer=https://www.douyin.com/video/7379445613236079884; __ac_nonce=06669a9f400ce1f28e533; ttwid=1%7C9Nz_KEuk-HKcdjb9PLTwePqzYubKPZXb_GfFU3HJ81U%7C1718200820%7C731492e777335f70a2978690c9a94a5094483538894c6d260748c00bc767bc04; s_v_web_id=; dy_swidth=1536;',
        'pragma': 'no-cache',
        'referer': 'https://www.douyin.com/video/7379445613236079884',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    response = requests.get('https://www.douyin.com/video/7379445613236079884', headers=headers).text

    # print(response.text)
    # print(response.headers)
    # exit()
    # base64_data = response.headers.get('x-vc-bdturing-parameters')
    # dd=json.loads(base64.b64decode(base64_data).decode())
    # detail=dd['detail']
    # fp=dd['fp']
    detail = re.findall('"detail":"(.*?)"', response)[0]
    fp = re.findall('"fp":"(.*?)"', response)[0]
    result = Dy('').run(
detail,fp, 'slide')
    print(result)



