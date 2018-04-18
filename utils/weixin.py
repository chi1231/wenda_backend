# coding=utf-8

import hashlib
import json
import random
import time
from urllib import quote
from xml.dom import minidom

import requests
from base_info.models import Restaurant
from django.conf import settings
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError


class WechatExt(object):
    def __init__(self, restaurant_id):
        self.restaurant_id = restaurant_id

    def get_articls_message(self, media_id):
        """ 获取图文素材"""

        try:
            r = Restaurant.objects.get(pk=self.restaurant_id)
        except Restaurant.DoesNotExist:
            return None

        wechat = get_wechat(r)
        if wechat is None:
            return None
        requests_url = (
            "https://api.weixin.qq.com/cgi-bin/material/get_material?access_token=" + wechat.get_access_token()[
                "access_token"])
        data = {
            "media_id": media_id
        }

        ret = requests.post(requests_url, data=json.dumps(data))

        return json.loads(ret.content)

    def create_material(self, type, media):

        """ 创建其他类型的素材 """

        try:
            r = Restaurant.objects.get(pk=self.restaurant_id)
        except Restaurant.DoesNotExist:
            return None

        wechat = get_wechat(r)
        if wechat is None:
            return None
        url = "https://api.weixin.qq.com/cgi-bin/material/add_material"
        ret = requests.post(
            url=url,
            params={
                'access_token': wechat.get_access_token()['access_token'],
                'type': type
            },
            files={
                'media': media
            })

        return json.loads(ret.content)

    def delete_material(self, media_id):

        """ 删除素材 """

        try:
            r = Restaurant.objects.get(pk=self.restaurant_id)
        except Restaurant.DoesNotExist:
            return None

        wechat = get_wechat(r)
        if wechat is None:
            return None
        url = "https://api.weixin.qq.com/cgi-bin/material/del_material?access_token=" + wechat.get_access_token()[
            'access_token']
        ret = requests.post(
            url=url,
            data=json.dumps({
                'media_id': media_id
            }))

        return json.loads(ret.content)

    def send_article_message(self, user_list, media_id):
        """ 发送文章信息"""
        try:
            r = Restaurant.objects.get(pk=self.restaurant_id)
        except Restaurant.DoesNotExist:
            return None
        wechat = get_wechat(r)

        if wechat is None:
            return None
        requests_url = (
            "https://api.weixin.qq.com/cgi-bin/message/mass/send?access_token=" + wechat.get_access_token()[
                "access_token"])
        data = {
            "touser": user_list,
            "mpnews": {
                "media_id": media_id
            },
            "msgtype": "mpnews"
        }

        ret = requests.post(requests_url,
                            data=json.dumps(data, ensure_ascii=False).encode('utf-8'))

        return json.loads(ret.content)

    def create_article_message(self, thumb_media_id, title, content,
                               content_url="", author="", digest=""):

        """ 创建文章信息"""

        try:
            r = Restaurant.objects.get(pk=self.restaurant_id)
        except Restaurant.DoesNotExist:
            return None

        wechat = get_wechat(r)
        if wechat is None:
            return None

        requests_url = ("https://api.weixin.qq.com/cgi-bin/material/add_news?access_token=" +
                        wechat.get_access_token()["access_token"])

        data = {
            "articles": [{
                "title": title,
                "thumb_media_id": thumb_media_id,
                "author": author,
                "content_source_url": content_url,
                "content": content,
                "digest": digest,
                "show_cover_pic": "0"
            }]
        }
        ret = requests.post(requests_url,
                            data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
        return json.loads(ret.content)

    def create_order(self, customer_ip, open_id, out_trade_no, goods_name,
                     total_fee):

        try:
            r = Restaurant.objects.get(pk=self.restaurant_id)
        except Restaurant.DoesNotExist:
            return None

        url = "https://api.mch.weixin.qq.com/pay/unifiedorder"

        params = {
            'appid': 'wx655d30911dfc889c',  # 微信appid
            'body': goods_name,  # 商品描述
            'mch_id': '1245241702',  # 商户号
            'nonce_str': create_noncestr(32),  # 随机字符串
            'notify_url': settings.WEIXIN_URL + '/api/pay/callback/',  # 回调地址,
            'out_trade_no': out_trade_no,  # 商户订单号
            'spbill_create_ip': '112.226.140.172',  # 用户ip
            'total_fee': str(int(float(total_fee) * 100)),  # 总金额
            'trade_type': 'JSAPI',  # 交易类型
            'openid': open_id
        }
        params['sign'] = get_sign(params, r.mch_key)
        headers = {'Content-Type': 'application/xml'}
        params_str = dict_to_xml(params)

        return requests.post(url, params_str, headers=headers).text

    def get_open_id(self, code):
        try:
            r = Restaurant.objects.get(pk=self.restaurant_id)
        except Restaurant.DoesNotExist:
            return None

        requests_url = "https://api.weixin.qq.com/sns/oauth2/access_token?"
        data = {
            "appid": r.app_id,
            "secret": r.app_secret,
            "code": code,
            "grant_type": "authorization_code",
        }
        ret = requests.get(requests_url, params=data)
        return json.loads(ret.content)


def get_wechat(restaurant):
    # 判断access token是否过期
    if (restaurant.weixin_access_token is None or
                restaurant.weixin_access_token_expires_at < int(time.time()) - 1000):
        wechat = WechatBasic(token=restaurant.token,
                             appid=restaurant.app_id,
                             appsecret=restaurant.app_secret)
        r = wechat.get_access_token()
        restaurant.weixin_access_token = r["access_token"]
        restaurant.weixin_access_token_expires_at = r["access_token_expires_at"]
        restaurant.save()

    wechat = WechatBasic(token=restaurant.token,
                         appid=restaurant.app_id,
                         appsecret=restaurant.app_secret,
                         access_token=restaurant.weixin_access_token,
                         access_token_expires_at=
                         restaurant.weixin_access_token_expires_at)
    return wechat


def format_params_dict(params_dict, urlencode):
    """ 格式化参数，签名过程需要使用,
        将字典按照ascii升序排序，然后组成url的格式"""

    slist = sorted(params_dict)
    buff = []

    for k in slist:
        v = quote(params_dict[k]) if urlencode else params_dict[k]
        buff.append("{0}={1}".format(k.encode('utf8'), v.encode('utf8')))

    return "&".join(buff)


def create_noncestr(length=32):
    """产生随机字符串，不长于32位"""

    chars = "abcdefghipqrstuvwxyz0123456789"
    strs = []
    for x in range(length):
        strs.append(chars[random.randrange(0, len(chars))])

    return "".join(strs)


def get_sign(obj, key):
    # 一: 字典排序
    result = format_params_dict(obj, False)
    # 二: 加入key
    result = "{0}&key={1}".format(result, key)
    # 三: md5加密
    result = hashlib.md5(result).hexdigest()
    # 四: 转为大写
    return result.upper()


def dict_to_xml(obj):
    """array转xml"""

    xml = ["<xml>"]
    slist = sorted(obj)
    for k in slist:
        xml.append("<{0}>{1}</{0}>".format(k.encode('utf8'), obj[k].encode('utf8')))
    xml.append("</xml>")

    return "".join(xml)


def xml_to_dict(data):
    result = {}

    if type(data) == unicode:
        data = data.encode('utf-8')
    elif type(data) == str:
        pass
    else:
        raise ParseError

    try:
        doc = minidom.parseString(data)
    except Exception:
        raise ParseError()

    params = [ele for ele in doc.childNodes[0].childNodes
              if isinstance(ele, minidom.Element)]
    for param in params:
        if param.childNodes:
            text = param.childNodes[0]
            result[param.tagName] = text.data

    return result
