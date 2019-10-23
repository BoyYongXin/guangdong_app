import base.constance as Constance
import utils.tools as tools
from utils.log import log
from db.mongodb import MongoDB
#from db.elastic_search import ES
#from db.oracledb import OracleDB
# from image_recog import *


#orcl = OracleDB()
#es = ES()
db = MongoDB()


def remove_table(tab_list):
    for tab in tab_list:
        db.delete(tab)


def reset_table(tab_list):
    for tab in tab_list:
        db.update(tab, {'status': 3}, {'status': 0})


def add_url(table, site_id='', url='', depth=0, remark='', status=Constance.TODO, image_url=''):
    url_dict = {'site_id': site_id, 'url': url, 'depth': depth, 'remark': remark, 'status': status,
                'record_time': tools.get_current_date(), 'image_url': image_url}
    return db.add(table, url_dict)


def update_value(table, attrs_old={}, attrs_new={}):
    db.update(table, attrs_old, attrs_new)


def update_url(table, url, status):
    db.update(table, {'url': url}, {'status': status})


def add_website_info(table, site_id, url, name, domain='', ip='', address='', video_license='', public_safety='',
                     icp='', contain_outlink=False):
    '''
    @summary: 添加网站信息
    ---------
    @param table: 表名
    @param site_id: 网站id
    @param url: 网址
    @param name: 网站名
    @param domain: 域名
    @param ip: 服务器ip
    @param address: 服务器地址
    @param video_license: 网络视听许可证|
    @param public_safety: 公安备案号
    @param icp: ICP号
    ---------
    @result:
    '''

    # 用程序获取domain,ip,address,video_license,public_safety,icp 等信息
    domain = tools.get_domain(url)

    site_info = {
        'contain_outlink': contain_outlink,
        'site_id': site_id,
        'name': name,
        'domain': domain,
        'url': url,
        'ip': ip,
        'address': address,
        'video_license': video_license,
        'public_safety': public_safety,
        'icp': icp,
        'read_status': 0,
        'record_time': tools.get_current_date()
    }
    db.add(table, site_info)

num=0
def save_info(table, site_id, site_name='', url='', title='', content='', release_time='', image_url='',
              video_url='', is_out_link=1, download_image=False, is_debug=False,es_read_status='',info_type=''):
    # global num
    # if num<2000:
    #     num+=1
    #     image_recogs=image_recog(image_url)
    # else:
    #     image_recogs=5

    if not download_image:
        sexy_image_url = image_url
        local_image_path = ''
    else:
        file_local_path = tools.get_conf_value('config.conf', 'files', 'zhejiang_app_save_path')
        if image_url:
            img_name = 'images/' + tools.get_current_date(date_format='%Y-%m-%d') + "/" + tools.get_current_date(
                date_format='%Y%m%d%H%M%S.%f') + '.jpg'
            tools.download_file(image_url, file_local_path, img_name)
            local_image_path = file_local_path + img_name
            sexy_image_url = local_image_path
        else:
            local_image_path = ''
            sexy_image_url = ''

    if len(content) > 400:
        temporary_content = content[0:400]
    else:
        temporary_content = content

    # record_time = tools.get_current_date()
    # release_time = tools.format_date(release_time)
    try:
        release_time = tools.format_date(release_time)
    except Exception as e:
        log.debug(e, release_time, url)
    record_time = tools.get_current_date()
    if release_time > record_time:
        return
    content_info = {
        'site_name':site_name,
        'video_url': video_url,
        'image_url': image_url,
        'temporary_content': temporary_content,
        'title': title,
        # 'video_local_path': local_video_path,\
        'img_stor_path': local_image_path,
        'release_time': release_time,
        'is_out_link': is_out_link,
        'url': url,
        'es_read_status': 0,
        'site_id': site_id, 'read_status': 0, 'record_time': record_time,
        # 'sexy_image_url': sexy_image_url, 'sexy_image_status': '', 'image_pron_status': image_recogs

    }
    content_info.pop('temporary_content')
    content_info['content'] = content
    if db.add(table, content_info):
        log.debug(content_info)

        # mongo_id = content_info['_id']
        # mongo_id = int(str(mongo_id)[-6:], 16)
        # uuid = str(mongo_id) + '_4'
        # # find_result_sql = 'select t.software_name, t.find_date from tab_app_info t where t.id = %s' % site_id
        # # find_result = orcl.find(find_result_sql)[0]
        # # site_name = find_result[0]
        # # site_find_date = find_result[1]
        # # if not site_find_date:
        # #     site_find_date = None
        # # else:
        # #     site_find_date = str(site_find_date)
        # site_name = site_name
        # site_find_date = '2017-11-23 00:00:00'
        # es_content_info = {
        #     'ID': mongo_id,
        #     'UUID': uuid,
        #     'ARTICLE_URL': url,
        #     'FIND_DATE': record_time,
        #     'PRAISE_COUNT': 0,
        #    # 'IMAGE_CODE': 5,
        #     'IMAGE_CODE': image_recogs,
        #     'RELEASE_TIME': release_time,
        #     'CONTENT': content,
        #     'IMAGE_URL': image_url,
        #     'SOURCE_ID': site_id,
        #     'SITE_FIND_DATE': site_find_date,
        #     'COMMENT_COUNT': 0,
        #     'SOURCE_NAME': site_name,
        #     'OUT_CHAIN_STATUS': 1,
        #     'NAME': title,
        #     'TRANSPOND_COUNT': 0,
        #     'TYPE_ID': '4',  # 1持证网站 2备案网站 3无证网站 4APP 5微博 6微信 7OTT
        #     'TYPE_NAME': 'APP',
        #
        #     'TASK_ID': '',
        #     'VIOLATE_LIBRARY': '',
        #     'ADDVIOLATE_DATE': None,
        #     'READ': 1,
        #     'CHECK_STATUS': 1,
        #     'VIOLATE_STATUS': 1,
        #     'MATERIAL_CHECK_VIOLATE_TYPE': '',
        #     'VIOLATE_CHECK_VIOLATE_TYPE': '',
        #     'FIELD_STR1': '',
        #     'FIELD_STR2': '',
        #     'MATERIAL_LIBRARY': '',
        #     'ADDMATERIAL_DATE': None,
        # }
        #
        # es.add('tab_iimp_all_program_info', es_content_info, uuid)
    # if not db.add(table, content_info):
    # content_info.pop('_id')
    # content_info.pop('sexy_image_url')
    # content_info.pop('sexy_image_status')
    # content_info.pop('image_pron_status')
    # db.update(table, old_value={'url': url}, new_value=content_info)


def is_violate(content, key1=[], key2=[], key3=[]):
    if not key1 and not key2:
        return False

    def check_key1(keys, content):
        for key in keys:
            key = key.strip() if key else ''
            if not key:
                continue

            if key not in content:
                return False
        else:
            return True

    def check_key2(keys, content):
        for key in keys:
            key = key.strip() if key else ''
            if not key:
                continue

            if key in content:
                return True
        else:
            return False

    def check_key3(keys, content):
        for key in keys:
            key = key.strip() if key else ''
            if not key:
                continue

            if key in content:
                return False
        else:
            return True

    result = True

    if key1:
        result = check_key1(key1, content)
    if key2:
        result = result and check_key2(key2, content)
    if key3:
        result = result and check_key3(key3, content)

    return result
