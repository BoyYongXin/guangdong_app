# *_*coding:utf-8 *_*
import requests
from jsonpath import jsonpath
from glom import glom
import base.base_parser as base_parser
import utils.tools as tools
from utils.log import log
import base.constance as Constance
import json
import time
import datetime
SITE_ID = 2
# 必须定义 网站名
NAME = '触电新闻'
import json
import os
import time

def get_channel_info():
    with open('channels.json', "r", encoding="utf-8") as f:
        json_infos = json.loads(f.read())
        json_channel_infos = json_infos["list"]
        for channel_infos in json_channel_infos:
            channelId, channelName, md5hash, signature, ts, timestamp = channel_infos["channelId"], channel_infos["channelName"], channel_infos["md5hash"], channel_infos["signature"], channel_infos["ts"], channel_infos["timestamp"]
            yield channelId, channelName, md5hash, signature, ts, timestamp
# 必须定义 添加网站信息
@tools.run_safe_model(__name__)
# 必须定义 添加网站信息
def add_site_info():
    log.debug('添加网站信息')
    site_id = SITE_ID
    name = NAME
    table = 'site_info'
    url = 'https://www.itouchtv.cn/'
    base_parser.add_website_info(table, site_id, url, name)
# 必须定义 添加根url
@tools.run_safe_model(__name__)
def add_root_url(parser_params = {}):
    log.debug('''
        添加根url
        parser_params : %s
        '''%str(parser_params))

    result_info = get_channel_info()
    for index, result in enumerate(result_info):
        c_id, c_name, md5, sign, ts, timestamp = result
        para_template = {
            "installChannel": "TengXun",
            "ac": 1,
            "cCode": 1101,
            "oldestTime": 0,
            "romVersion": "Xiaomi",
            "snapshotNumber": "0",
            "latitude": "40.095976",
            "channelType": 0,
            "language": "zh",
            "devicePlatform": "android",
            "pageNum": 0,
            "md5Hash": md5,  # MD5哈希加密
            "osVersion": "8.0.0",
            "pCode": 11,
            "aCode": "110114",
            "refreshType": 1,  # 是否刷新0没有，1有
            "deviceModel": "MIX 2",
            "channelId": c_id,  # 类别id
            "deviceBrand": "Xiaomi",
            "longitude": 116.392007,
        }
        header_template = {
        "X-ITOUCHTV-Ca-Signature":sign,
        "X-ITOUCHTV-INSTALL-CHANNEL":"TengXun",
        "X-ITOUCHTV-CONN-TYPE":"WIFI",
        "X-ITOUCHTV-DEVICE-IMSI":"460013332104390",
        "X-ITOUCHTV-PCODE":"11",
        "X-ITOUCHTV-ACODE":"110114",
        "X-ITOUCHTV-CLIENT":"NEWS_APP",
        "X-ITOUCHTV-OSVS":"8.0.0",
        "X-ITOUCHTV-ICCID":"84652312995149660086",
        "X-ITOUCHTV-Ca-Key":"04039368653554864194910691389924",
        "X-ITOUCHTV-APP-VERSION":"2.3.7",
        "X-ITOUCHTV-WEBVIEW-UA":"Mozilla/5.0 (Linux; Android 8.0.0; MIX 2 Build/OPR1.170623.027; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.92 Mobile Safari/537.36",
        "X-ITOUCHTV-CARRIER-CODE":"46001",
        "X-ITOUCHTV-MAC":"81:ba:e1:1e:8e:89",
        "X-ITOUCHTV-TERM":"MIX 2",
        "X-ITOUCHTV-MEID":"99001085363443",
        "X-ITOUCHTV-RESOLUTION":"2160,1080",
        "X-ITOUCHTV-DEVICE-SERIAL-NUM2":"d897167c",
        "X-ITOUCHTV-TS":ts,
        "X-ITOUCHTV-ANDROIDID":"220240afd2e0e640",
        "X-ITOUCHTV-CCODE":"1101",
        "X-ITOUCHTV-DEVICE-SERIAL-NUM":"MIX 2",
        "X-ITOUCHTV-IDFA":"",
        "X-ITOUCHTV-DEVICE-ID":"IMEI_780493075490198",
        "X-ITOUCHTV-Ca-Timestamp":timestamp,
        "User-Agent":"Dalvik/2.1.0 (Linux; U; Android 8.0.0; MIX 2 MIUI/V10.3.1.0.ODECNXM)",
        "Host":"api.itouchtv.cn",
        "Connection":"Keep-Alive",
        "Accept-Encoding":"gzip"
        }
        for times in range(10):
            url = f'https://api.itouchtv.cn/newsservice/v3/uniteChannelNews#{index}#{times}'
            base_parser.add_url('urls', SITE_ID, url, remark={"cate_name":c_name, "para_template":para_template, "header_template":header_template}, depth=0)

# 必须定义 解析网址
def parser(url_info):
    root_url = url_info['url']
    para = url_info["remark"]["para_template"]
    headers = url_info["remark"]["header_template"]
    response = requests.get(root_url, params=para, headers=headers)
    time.sleep(2)
    json_info = response.json()
    cate = url_info["remark"]["cate_name"]
    data_jsons = jsonpath(json_info, "$..items..data")
    if cate != '':
        for data_info in data_jsons:
            data_json = json.loads(data_info)
            title = jsonpath(data_json, "$..title")[0]
            img_str = glom(data_json, "coverUrl")
            img_json = json.loads(img_str)
            img_url = img_json["L"][0]
            content = jsonpath(data_json, "$..summary")[0]
            updateTime = jsonpath(data_json, "$..updateTime")[0]
            video_str = glom(data_json, "videoUrl")
            video_json = json.loads(video_str)
            video_url = video_json["source"]["hd"]
            release_time = tools.timestamp_to_date(str(updateTime)[:-3])
            base_parser.save_info('content_info', site_id=SITE_ID, url=video_url, title=title, site_name=NAME,
                                  content=content, release_time=release_time, image_url=img_url,
                                  video_url=video_url, is_out_link=1, download_image=False, is_debug=False,
                                  )


    base_parser.update_url('urls', root_url, Constance.DONE)