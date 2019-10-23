# import re
# st = "https://pacaio.match.qq.com/vlike/category?cid=6&num=10&page=200"
# a = ''.join(re.findall('page=(\d+)',st,re.M|re.M))
# st = re.sub(a,"wereew",st)
# print(st)

import re
# 将匹配的数字乘于 2
# def double(matched):
#     value = int(matched.group('value'))
#     return str(value * 2)

# s = 'A23G4HFD567'
# print(re.sub('(?P<value>\d+)', double, s))
'''
def double(matched):
    value = int(matched.group('value'))
    return 'page=' + str(55324234)
st = "https://pacaio.match.qq.com/vlike/category?cid=6&num=10&page=200"
st = re.sub('page=(?P<value>\d+)',double,st)
print(st)
'''

def repl_num(strs):
    num = strs.group("ps")
    new_page = int(num) + 1
    new_str = str(new_page)
    return new_str

root_url = 'https://pacaio.match.qq.com/vlike/category?cid=6&num=10&page=200'
category_url = re.sub('page=(?P<ps>\d+)', repl_num, root_url)
print(category_url)