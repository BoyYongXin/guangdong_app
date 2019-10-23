# *_*coding:utf-8 *_*
# 必须定义 添加网站信息
import requests
from urllib.parse import urlencode
from jsonpath import jsonpath
from glom import glom
import utils.tools as tools
import base.base_parser as base_parser
from utils.log import log
import base.constance as Constance
import json
import time
import datetime
import json

SITE_ID = 3
# 必须定义 网站名
NAME = '全民电视直播'
def get_md5_sign(ts):
    base_str = 'fungolive'
    key = base_str + str(ts)
    result = tools.get_md5(key)
    return result

@tools.run_safe_model(__name__)
# 必须定义 添加网站信息
def add_site_info():
    log.debug('添加网站信息')
    site_id = SITE_ID
    name = NAME
    table = 'site_info'
    url = 'https://www.wandoujia.com/app/org.fungo.fungolive'
    base_parser.add_website_info(table, site_id, url, name)
# 必须定义 添加根url
@tools.run_safe_model(__name__)
def add_root_url(parser_params = {}):
    log.debug('''
        添加根url
        parser_params : %s
        '''%str(parser_params))
    category_infos = [(-1, "推荐"), (10, "体育"), (11, "资讯"), (12, "影视"), (13, "娱乐"), (17,"社会")]
    for cid, cname in category_infos:
        nwtime = tools.get_current_timestamp()
        #推荐模块
        sign = get_md5_sign(nwtime)
        tj_base_url = 'http://user.xiaoyouzb.net/v3/vod/small_recommend?'
        para = {
            "nwtime": "{}".format(nwtime),
            "sign": "{}".format(sign),
            "type": "1",
            "cateId": "{}".format(cid),
            "pageNum": "0",
            "isFirst": "N",
            "_u": "edac2c15598946bd9ba7bda78a83489c",
            "version": "4.7.0",
            "platform": "android",
            "appx": "yuntu",
            "apppn": "org.fungo.fungolive",
            "enterprise": "0",
            "channel": "tencent",
            "market": "32",
            "os_version": "8.0.0",
            "device_model": "MIX%202",
            "device_code": "780493075490198",
            "udid": "77e2cb72797f20afdcaaa6265872cea9",
            "androidId": "220240afd2e0e640",
            "source": "android",
        }
        tj_url = tj_base_url + urlencode(para)

        base_parser.add_url('urls', SITE_ID, tj_url, remark={"category_name": cname}, depth=0)

        url = tj_url.replace("pageNum=0", "pageNum={}")
        url_pages = [url.format(page) for page in range(1, 61)]
        for url_page in url_pages:
            base_parser.add_url('urls', SITE_ID, url_page, remark={"category_name": cname}, depth=0)
# 必须定义 解析网址
def parser(url_info):
    # url  = 'http://user.xiaoyouzb.net/v3/vod/small_recommend?nwtime=1571816563&sign=883f96aee2655d8885e7815de3423df7&type=1&cateId=13&pageNum=0&isFirst=N&_u=edac2c15598946bd9ba7bda78a83489c&version=4.7.0&platform=android&appx=yuntu&apppn=org.fungo.fungolive&enterprise=0&channel=tencent&market=32&os_version=8.0.0&device_model=MIX%25202&device_code=780493075490198&udid=77e2cb72797f20afdcaaa6265872cea9&androidId=220240afd2e0e640&source=android'
    root_url = url_info['url']
    cname = url_info['remark']["category_name"]
    headers = {
        "User-Agent": "yuntutv/4.7.0 (Android 8.0.0)",
        "Host": "user.xiaoyouzb.net"
    }
    json_data = tools.get_json_by_requests(root_url, headers=headers)
    data_infos = json_data["data"]
    for data_info in data_infos:
        publishTime = data_info["publishTime"]
        release_time = tools.timestamp_to_date(str(publishTime)[:-3])
        title = data_info["content"]
        content = data_info["content"]
        video_url = data_info["videoUrl"]
        img_url = data_info["coverUrl"]
        base_parser.save_info('content_info', site_id=SITE_ID, url=video_url, title=title, site_name=NAME,
                              content=content, release_time=release_time, image_url=img_url,
                              video_url=video_url, is_out_link=1, download_image=False, is_debug=False,
                              )
    base_parser.update_url('urls', root_url, Constance.DONE)