import base.base_parser as base_parser
from base.spider import Spider
from parsers import *
import export_data
from utils.log import log

tab_list = ['urls', 'site_info', 'content_info']  # 配置表(第一个须为url表)
tab_unique_key_list = ['url', 'site_id', 'url']  # 唯一索引
tab_ensure_index_list = [['depth', 'status'], ['read_status'], ['read_status']]  # 配置索引(加快查找速度)

parser_list = [yi_shenzhen,touchtv,quanming_tv]
parser_list = [xunlei]
parser_siteid_list = []  # 对应parser的site_id
for parser in parser_list:
    site_id = parser.SITE_ID
    parser_siteid_list.append(site_id)


def main():
    def begin_callback():
        # mongo_db = MongoDB()
        # mongo_db.update('ZHEJIANG_APP_urls', {'depth': 0}, {'status': 0})
        log.info('\n********** spider_main begin **********')

    def end_callback():
        log.info('\n********** spider_main end **********')

    # 配置spider
    spider = Spider(tab_list, tab_unique_key_list, tab_ensure_index_list, parser_count=1,
                    site_parsers=parser_siteid_list, begin_callback=begin_callback, end_callback=end_callback,
                    parser_params={})

    # 添加parser
    for parser in parser_list:
        spider.add_parser(parser)

    spider.start()


if __name__ == '__main__':
    base_parser.remove_table(['urls'])
    main()
