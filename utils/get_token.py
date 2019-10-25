# *_*coding:utf-8 *_*
from urllib import request
from http import cookiejar
#跳过SSL验证证书
import ssl

def  get_cookies(url:str):

    #设置忽略SSL验证
    ssl._create_default_https_context = ssl._create_unverified_context
    #声明一个CookieJar对象实例来保存cookie
    cookie = cookiejar.CookieJar()
    #利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    handler=request.HTTPCookieProcessor(cookie)
    #通过CookieHandler创建opener
    opener = request.build_opener(handler)
    #此处的open方法打开网页
    response = opener.open(url)
    #response = opener.open('https://mparticle.uc.cn/video.html?app=uc-iflow&uc_biz_str=S%3Acustom%7CC%3Aiflow_video_hide&btifl=10016&uc_param_str=frdnsnpfvecpntnwprdssskt&wm_aid=6f29ae044edb43dfad1ee1f18b6e6a06&wm_id=7737909731c141798153300adca85262&admincptm=1571824662374&pagetype=share&tab=video&source=share-back')
    #打印cookie信息
    for item in cookie:
        # print('Name = %s' % item.name)
        # print('Value = %s' % item.value)
        return item.value

# token = get_cookies()

