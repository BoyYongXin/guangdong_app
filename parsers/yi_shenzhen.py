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
SITE_ID = 1
# 必须定义 网站名
NAME = '壹深圳'
PAGES = 5
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
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
    #添加文章链接方法
    def add_article_url():
        channel_url = 'https://api.scms.sztv.com.cn/api/com/catalog/getCatalogList?types=2 \
        &uid=KeL5dDCnfEBKSjY&isTree=0&appCode=20&tenantid=ysz&tenantId=ysz'
        response = requests.get(channel_url)
        response.encoding = 'utf-8'
        html = response.json()
        channel_ids = jsonpath.jsonpath(html, '$..id')
        for channel_id in channel_ids:
            channel_url_son = 'https://api.scms.sztv.com.cn/api/com/catalog/getCatalogList?parentId={}&types=2 \
        &uid=v7bXtg86cABXyVp&isTree=0&appCode=21&tenantid=ysz&tenantId=ysz'.format(channel_id)
            html = tools.get_json_by_requests(channel_url_son, headers=headers)
            if "returnData" in html.keys() and html["returnData"]:
                channel_url_son_ids = jsonpath.jsonpath(html, "$..id")
                for id in channel_url_son_ids:
                    for page in range(1, PAGES):
                        info_url = 'https://api.scms.sztv.com.cn/api/com/article/getArticleList?uid=v7bXtg86cABXyVp&specialtype=1&tenantid=ysz&page={}&tenantId=ysz&pageSize=6&catalogId={}'.format(
                            page, id)
                        base_parser.add_url('urls', SITE_ID, info_url,remark={},depth=0)
    add_article_url()

# 必须定义 解析网址
def parser(url_info):
    url_info['_id'] = str(url_info['_id'])
    root_url = url_info['url']
    depth = url_info['depth']
    site_id = url_info['site_id']
    remark = url_info['remark']
    data = tools.get_json_by_requests(root_url)
    data_info = data.get("returnData").get('news')
    for info in data_info:
        # print(info)
        url = info['url']
        release_time = info['publishDate']
        title = info['title']
        video_url = jsonpath.jsonpath(info['video'], '$..relativeUrl')[0]
        img_url = info['logo']

        if video_url !='':
            info_type = 1
        else:
            info_type = 2

        base_parser.save_info('content_info', site_id=SITE_ID, url=url, title=title,site_name=NAME,
                                          content='', release_time=release_time, image_url=img_url,
                                          video_url=video_url, is_out_link=1, download_image=False, is_debug=False,
                                          info_type=info_type)

    base_parser.update_url('urls', root_url, Constance.DONE)



