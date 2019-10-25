import sys
sys.path.append('../../')
import base.base_parser as base_parser
import base.constance as Constance
import utils.tools as tools
from utils.log import log
import requests
import jsonpath
from glom import glom
import re
import utils.get_token as get_token
import time

headers = {
    'Host': 'iflow.uczzd.cn',
    'Proxy-Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; TRT-AL00A Build/HUAWEITRT-AL00A; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/64.0.3282.137 Mobile Safari/537.36 iThunder',

}

# 必须定义 网站id
SITE_ID = 5
# 必须定义 网站名
NAME = '手机UC游览器'
_PAGES = 10

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
        urls = [
            'http://iflow.uczzd.net/iflow/api/v1/channel/10016?method=new&ftime=1571901210002&recoid=2467839182609073066&count=20&content_ratio=100',
            'http://iflow.uczzd.net/iflow/api/v1/channel/10301?method=new&ftime=0&recoid=&count=8&content_ratio=100',
            'http://iflow.uczzd.net/iflow/api/v1/channel/622769673?method=new&ftime=0&recoid=&count=20&content_ratio=100',
            'http://iflow.uczzd.net/iflow/api/v1/channel/622336449?method=new&ftime=0&recoid=&count=20&content_ratio=100',
            'http://iflow.uczzd.net/iflow/api/v1/channel/10461?method=new&ftime=0&recoid=&count=20&content_ratio=100',
            'http://iflow.uczzd.net/iflow/api/v1/channel/10365?method=new&ftime=0&recoid=&count=20&content_ratio=100',
            'http://iflow.uczzd.net/iflow/api/v1/channel/622736331?method=new&ftime=0&recoid=&count=20&content_ratio=100',
            'http://iflow.uczzd.net/iflow/api/v1/channel/10259?method=new&ftime=0&recoid=&count=20&content_ratio=100',
            'http://iflow.uczzd.net/iflow/api/v1/channel/10051?method=new&ftime=0&recoid=&count=20&content_ratio=100',
            'http://iflow.uczzd.net/iflow/api/v1/channel/10116?method=new&ftime=0&recoid=&count=20&content_ratio=100',
            'http://iflow.uczzd.net/iflow/api/v1/channel/10139?method=new&ftime=0&recoid=&count=20&content_ratio=100',
            'http://iflow.uczzd.net/iflow/api/v1/channel/10049?method=new&ftime=0&recoid=&count=20&content_ratio=100',
        'http://iflow.uczzd.cn/iflow/api/v1/channel/622810092?method=new&ftime=1571902273506&recoid=6995844991074725827&count=20&content_ratio=100']
        for root_url in urls:

            #root_url = f'http://iflow.uczzd.cn/iflow/api/v1/channel/622810092?method=new&ftime=1571902273506&recoid=6995844991074725827&count=20&content_ratio=100#{page}'

            base_parser.add_url('urls', SITE_ID, root_url,remark={},depth=0)
# 必须定义 解析网址
def parser(url_info):
    url_info['_id'] = str(url_info['_id'])
    root_url = url_info['url']
    depth = url_info['depth']
    site_id = url_info['site_id']
    remark = url_info['remark']
    response = requests.get(root_url, headers=headers, verify=False)
    time.sleep(1)
    response.encoding = 'utf-8'
    html = response.json()
    data_info = jsonpath.jsonpath(html, "$..articles")
    for datas in data_info:
        for key, data in datas.items():
            title = data.get('title')
            url = data.get('url')
            ums_id_url = data.get("zzd_url")
            img_url = glom(data, "videos")[0]['poster']['url']
            release_time = glom(data, 'grab_time')
            release_time = stamp_to_date(release_time)

            ums_id = ''.join(re.findall('ums_id=(.*?)&', ums_id_url))
            wm_id = ''.join(jsonpath.jsonpath(data, '$..wm_id'))
            wm_cid = ''.join(jsonpath.jsonpath(data, '$..outer_id'))
            share_url = glom(data, "share_url")

            token = get_token.get_cookies(url)
            headers2 = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
               # "Cookie": "cna=jfAyFgS8dngCAXt/00SmKeKX; isg=BLi417M0EasPYH0vvOczKR61iWaKiUzQuZOVr_IoEPOpDVj3mjJ0O81swUUYXdSD; _pk_ref.070b5f1f4053.1564=%5B%22%22%2C%22%22%2C1571910457%2C%22http%3A%2F%2Fiflow.uczzd.cn%2Fiflow%2Fapi%2Fv1%2Fchannel%2F622810092%3Fmethod%3Dnew%26ftime%3D1571902273506%26recoid%3D6995844991074725827%26count%3D20%26content_ratio%3D100%22%5D; _pk_id.070b5f1f4053.1564=5136a990-361d-4dc8-9cdd-2a4c4ffa6748.1571901120.3.1571910528.1571908320.",
                "Host": "mparticle.uc.cn",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            }
            video_url_info_url = f'https://mparticle.uc.cn/api/vps?token={token}&ums_id={ums_id}&wm_cid={wm_cid}&wm_id={wm_id}&resolution=high'
            video_url_info = tools.get_json_by_requests(video_url_info_url,headers=headers2)
            # print(video_url_info_url)
            # print(video_url_info)
            time.sleep(1)
            video_url = glom(video_url_info, 'data.url')

            if video_url !='':
                info_type = 1
            else:
                info_type = 2

            base_parser.save_info('content_info', site_id=SITE_ID, url=url, title=title,site_name=NAME,
                                              content='', release_time=release_time, image_url=img_url,
                                              video_url=video_url, is_out_link=1, download_image=False, is_debug=False,
                                              info_type=info_type)

    base_parser.update_url('urls', root_url, Constance.DONE)



