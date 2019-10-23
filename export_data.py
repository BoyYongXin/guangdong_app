from utils.export_data import ExportData
import time
# from image_recog import *

def site_main():
    # 导出数据
    key_map = {
        'id': 'int__id',
        'APP_ID': 'int_site_id',
        'CONTENT_ID': 'int__id',
        'RELEASE_TIME': 'date_release_time',
        'TITLE': 'str_title',
        'ORIGINAL_URL': 'str_url',
        'CONTENT': 'clob_content',
        'ABSTRACT_IMAGE_URL': 'str_image_url',
        'ABSTRACT_IMAGE_LOCAL_PATH': 'str_img_stor_path',
        'VIDEO_URL': 'str_video_url',
        # 'VIDEO_LOCAL_PATH': 'str_video_local_path',
        'RECORD_TIME': 'date_record_time',
        # 'image_code': 'vint_5'
        'image_code': 'vint_5'
        # 'image_code': 'str_sexy_image_status'
    }
    export_data = ExportData()
    export_data.export_to_oracle(source_table='TIANJIN_APP_content_info', aim_table='tab_app_program_info',
                                 key_map=key_map,
                                 unique_key='ORIGINAL_URL', condition={'read_status': 0})  # , "image_pron_status": 2})


if __name__ == '__main__':
    site_main()
