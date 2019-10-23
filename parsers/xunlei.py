import sys
sys.path.append('../../')
import base.base_parser as base_parser
import base.constance as Constance
import utils.tools as tools
from utils.log import log
import requests
import json
import jsonpath
import time

# 必须定义 网站id
SITE_ID = 4
# 必须定义 网站名
NAME = '手机迅雷'
_PAGES = 10
headers = {
    'Account-Id': '40',
    'Version-Code': '11030',
    'Peer-Id': '851c941b27d3f4e8161ded7f2044a60e',
    'Platform-Version': '7.0',
    'App-Type': 'android',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; TRT-AL00A Build/HUAWEITRT-AL00A; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/64.0.3282.137 Mobile Safari/537.36 iThunder',
    'IMEI': '864665031586774',
    'channelId': '0x10800013',
    'Device-Id': '298017440dea729188932a010da2f7e7',
    'Product-Id': '37',
    'Version-Name': '5.53.2.5300',
    'channel': '0x10800013',
    'Mobile-Type': 'android',
    'Host': 'api-shoulei-ssl.xunlei.com',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',

}
#处理时间戳的方法
def stamp_to_date(release_time):
    if len(str(release_time))>10:
        release_time = int(release_time) / 1000
        # 转换成localtime
        release_time = time.localtime(release_time)
        # 转换成新的时间格式(2016-05-05 20:28:54)
        release_time = time.strftime("%Y-%m-%d %H:%M:%S", release_time)
    else:
        release_time = int(release_time)
        # 转换成localtime
        release_time = time.localtime(release_time)
        # 转换成新的时间格式(2016-05-05 20:28:54)
        release_time = time.strftime("%Y-%m-%d %H:%M:%S", release_time)
    return release_time



@tools.run_safe_model(__name__)
# 必须定义 添加网站信息
def add_site_info():
    log.debug('添加网站信息')
    site_id = SITE_ID
    name = NAME
    table = 'site_info'
    url = 'https://dc.gog.cn/'
    base_parser.add_website_info(table, site_id, url, name)

# 必须定义 添加根url
@tools.run_safe_model(__name__)
def add_root_url(parser_params = {}):
    log.debug('''
        添加根url
        parser_params : %s
        '''%str(parser_params))
    for page in range(_PAGES):

        root_url = f'http://api-shoulei-ssl.xunlei.com/ivideo_v5/feed_list?size=6&type=firstLoad&ads_filter=0&p=1241&devicetype=1&make=HUAWEI&os=4&osv=7.0&model=TRT-AL00A&h=1208&w=720&connectiontype=0&dpid=f9233a75e11ce136&mac=02%3A00%3A00%3A00%3A00%3A00&appId=17&v=1.0&callId=1571819975104&timestamp=1571819975&nonce=-915381599&accesskey=android.m.xunlei&sig=7-zMGPgZnM5rYTWWA0dWuTGKLJM=#{page}'

        base_parser.add_url('urls', SITE_ID, root_url,remark={},depth=0)
# 必须定义 解析网址
def parser(url_info):
    url_info['_id'] = str(url_info['_id'])
    root_url = url_info['url']
    depth = url_info['depth']
    site_id = url_info['site_id']
    remark = url_info['remark']
    html = tools.get_json_by_requests(root_url, headers=headers)
    data_info = jsonpath.jsonpath(html, '$..video_info')
    for data in data_info:
        title = data.get('title')
        video_url = data.get('play_url')
        img_url = data.get('cover_url')
        release_time = stamp_to_date(data.get('upline_time'))

        if video_url !='':
            info_type = 1
        else:
            info_type = 2

        base_parser.save_info('content_info', site_id=SITE_ID, url=video_url, title=title,site_name=NAME,
                                          content='', release_time=release_time, image_url=img_url,
                                          video_url=video_url, is_out_link=1, download_image=False, is_debug=False,
                                          info_type=info_type)

    base_parser.update_url('urls', root_url, Constance.DONE)



