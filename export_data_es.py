import base.constance as Constance
import utils.tools as tools
from utils.log import log
from db.mongodb import MongoDB
from db.elastic_search import ES
import pymongo
es = ES()
db = MongoDB()
# client = pymongo.MongoClient("localhost:27017")
# db = client.tianjin_app
# info=db.TIANJIN_APP_content_info
def save_es():

    while True:
        content_infos=db.find('TIANJIN_APP_content_info', {'es_read_status': 0}, limit=40000)
        #print(content_infos)
        if not content_infos:
            break
        for content_info in content_infos:
            mongo_id = content_info['_id']
            mongo_id = int(str(mongo_id)[-6:], 16)
            uuid = str(mongo_id) + '_4'
            # site_name = content_info['site_name']
            if not content_info['release_time']:
                content_info['release_time'] = tools.get_current_date()
            site_find_date = '2018-09-23 00:00:00'
            es_content_info = {
                'ID': mongo_id,
                'UUID': uuid,
                'ARTICLE_URL': content_info['url'],
                'FIND_DATE': content_info['record_time'],
                'PRAISE_COUNT': 0,
               # 'IMAGE_CODE': 5,
                'IMAGE_CODE': content_info['image_pron_status'],
                'RELEASE_TIME': content_info['release_time'],
                'CONTENT': content_info['content'],
                'IMAGE_URL': content_info['image_url'],
                'SOURCE_ID': content_info['site_id'],
                'SITE_FIND_DATE': site_find_date,
                'COMMENT_COUNT': 0,
                'SOURCE_NAME':content_info['site_name'] ,
                'OUT_CHAIN_STATUS':1,
                'NAME': content_info['title'],
                'TRANSPOND_COUNT': 0,
                'TYPE_ID': '4',  # 1持证网站 2备案网站 3无证网站 4 APP 5微博 6微信 7OTT
                'TYPE_NAME': 'APP',
                'TASK_ID': '',
                'VIOLATE_LIBRARY': '',
                'ADDVIOLATE_DATE': None,
                'READ': 1,
                'CHECK_STATUS': 1,
                'VIOLATE_STATUS': 1,
                'MATERIAL_CHECK_VIOLATE_TYPE': '',
                'VIOLATE_CHECK_VIOLATE_TYPE': '',
                'FIELD_STR1': '',
                'FIELD_STR2': '',
                'MATERIAL_LIBRARY': '',
                'ADDMATERIAL_DATE': None,
            }
            # print(es_content_info['UUID'])
            es.add('tab_iimp_all_program_info', es_content_info, uuid)#{"es_read_status": "1"}
            # es.add_batch(es_content_info, uuid,'tab_iimp_all_program_info')
            # info.update({"_id":content_info['mongo_id']},{"$set": {"es_read_status": "1"}})
            db.update('TIANJIN_APP_content_info', {"_id": content_info['_id']},  {"es_read_status": 1})


if __name__ == '__main__':
    save_es()
    # from bson.objectid import ObjectId
    #
    # db.update('TIANJIN_APP_content_info', {"_id": ObjectId("5ba5e849660ffc06c8afef6a")}, {"es_read_status": "0"})