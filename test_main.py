# *_*coding:utf-8 *_*
import requests
import jsonpath
from glom import glom
import re
import utils.get_token as get_token
import utils.tools as tools
import time
headers = {
    'Host': 'iflow.uczzd.cn',
    'Proxy-Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; TRT-AL00A Build/HUAWEITRT-AL00A; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/64.0.3282.137 Mobile Safari/537.36 iThunder',

}
url = '''http://iflow.uczzd.cn/iflow/api/v1/channel/622810092?method=new&ftime=1571902273506&recoid=6995844991074725827&count=20&content_ratio=100'''

response = requests.get(url,headers=headers,verify=False)
time.sleep(1)
response.encoding = 'utf-8'
html = response.json()
data_info = jsonpath.jsonpath(html,"$..articles")
for datas in data_info:
    for key,data in datas.items():
        title = data.get('title')
        url = data.get('url')
        ums_id_url = data.get("zzd_url")
        img_url = glom(data,"videos")[0]['poster']['url']
        release_time = glom(data,'grab_time')
        print(title)
        print(url)
        print(img_url)
        print(release_time)

        ums_id =''.join(re.findall('ums_id=(.*?)&',ums_id_url))
        wm_id = ''.join(jsonpath.jsonpath(data, '$..wm_id'))
        wm_cid = ''.join(jsonpath.jsonpath(data, '$..outer_id'))
        share_url = glom(data,"share_url")

        token = get_token.get_cookies(share_url)
        video_url_info_url = f'https://mparticle.uc.cn/api/vps?token={token}&ums_id={ums_id}&wm_cid={wm_cid}&wm_id={wm_id}&resolution=high'
        video_url_info = tools.get_json_by_requests(video_url_info_url)
        time.sleep(1)
        video_url = glom(video_url_info,'data.url')
        print(video_url)
        break