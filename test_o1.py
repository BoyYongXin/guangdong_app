import utils.tools as tools
from glom import glom
import jsonpath
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



root_url = 'http://api-shoulei-ssl.xunlei.com/ivideo_v5/feed_list?size=6&type=firstLoad&ads_filter=0&p=1241&devicetype=1&make=HUAWEI&os=4&osv=7.0&model=TRT-AL00A&h=1208&w=720&connectiontype=0&dpid=f9233a75e11ce136&mac=02%3A00%3A00%3A00%3A00%3A00&appId=17&v=1.0&callId=1571819975104&timestamp=1571819975&nonce=-915381599&accesskey=android.m.xunlei&sig=7-zMGPgZnM5rYTWWA0dWuTGKLJM='
html = tools.get_json_by_requests(root_url,headers=headers)
# print(html)
data_info = jsonpath.jsonpath(html,'$..video_info')
for data in data_info:
    print(data)
    title = data.get('title')
    video_url = data.get('play_url')
    img_url = data.get('cover_url')
    print(title)
    print(video_url)
    print(img_url)
