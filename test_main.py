# *_*coding:utf-8 *_*
import requests
import sys

import utils.tools as tools
headers = {

    'Host': 'iflow.uczzd.cn',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Content_Type':'text/html;charset=utf-8',

}
url = '''http://iflow.uczzd.cn/iflow/api/v1/channel/10478?method=new&ftime=0&recoid=&count=20&content_ratio=100&content_length=2048&app=uc-iflow&no_op=0&auto=1&_tm=1571797441354&tab=video_b&uc_param_str=dnnivebichfrmintcpgidsudsvmedizbssnwlobd&user_tag=bTkwBCMI9ECHLVDocw%3D%3D&sp_gz=3&enable_ad=1&ad_extra=AAPtYwIQWftB3nixavZFw3Q8&earphone=0&moving=-1&cindex=1&active_time=AAPSz1bLoxw0fekX0G4QBei8&oneid=AAN71B5Y913agsh0%2BVluCpQUBehuQJREqZgs6ktePT34jQ%3D%3D&enod=AASCI1UF50vzsp6cPoG1Ye%2FRMSSjs4w5gFEPS9OD%2FS0zV%2F0DG4Bzx6g9ekZF2fxWsDo%3D&ssign=AAM761YwTffoCdGxARwVNY62TmjF9LjSoKwc%2BGr8%2FATHldVlrOgBus1PMg3CgWGZ59U%3D&dn=40729532011-06c59295&nn=AARroYxsshvCO8B0sRlz0w9ZcCczdfQBaUwibhDZy2pKTQ%3D%3D&ve=12.7.0.1050&bi=34464&ch=yzappstore%40&fr=android&mi=TRT-AL00A&nt=2&pc=AAQToG73q5JEnWuPgTs0XDUb%2FVhv8bJYxHOubMHEhWRKnn5UMxzpCHufr9S9fSmAmtIJEANmor98uewR0IfM%2BpVW&gp=AAQTetJlylrx97EJw24rax3efHC96L0kVcZH3kMra0Ywug%3D%3D&ut=AARfL5PV8mGmROGWAeobTqxvQuLcRj3gkp7%2BNBp%2BLKFTdw%3D%3D&ai=&sv=ucrelease&me=AARX9BUwG0%2FLzAZg3EoxTKsZ&di=f9233a75e11ce136&zb=00000&ss=360x604&nw=WIFI&lo=AAQToG73q5JEnWuPgTs0XDUb%2FVhv8bJYxHOubMHEhWRKnn5UMxzpCHufr9S9fSmAmtIYK4WUa9xYhWR6jxAcii2kUed2shQwg%2FhDwsVl3T6OS3y3eW0Ag57v0YMy4ot%2F%2FVtXjkgnNUozEOp2aCIwgClFYh2mUgR4ABsca%2FgF7iyhKg%3D%3D&bd=huawei&xss_enc=31&ab_tag=2261F2;2130B2;2299A2;2342A2;1979B2;1982C2;2384D2;2154A2;2351A2;&zb=00000&puser=1&ressc=44'''

response = requests.get(url,headers=headers,verify=False)
print(response.encoding)
# response.encoding = 'Windows-1252'
response.encoding = encoding = response.apparent_encoding
html = response.text

print(html)