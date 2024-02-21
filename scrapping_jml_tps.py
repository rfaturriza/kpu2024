import time
import json
import os
from datetime import datetime
from api_kawalpemilu import api_url
from api import get_city_list
import requests

def create_file():
    global create_file_time 
    create_file_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    global result_file
    result_file = 'result/result_total_tps.csv'
    if not os.path.exists('result'):
        os.makedirs('result')
    with open(result_file, 'w') as f:
        f.write('NAMA PROVINSI,NAMA KABUPATEN,JUMLAH TPS,ID KABUPATEN,KODE KABUPATEN\n')

def get_province_list():
    province_file = open('data/province.json')
    province_json = json.load(province_file)
    return province_json

# {
#     "result": {
#         "names": [
#             "ACEH"
#         ],
#         "id": "11",
#         "aggregated": {
#             "1101": [
#                 {
#                     "totalKpuTps": 488,
#                     "totalLaporTps": 24,
#                     "idLokasi": "1101",
#                     "pas2": 14665,
#                     "totalTps": 697,
        # https://kp24-fd486.et.r.appspot.com/h?id=11
        # https://kp24-fd486.et.r.appspot.com/h?id=${code_province}

def get_total_tps_by_province(province_code):
    try:
        url = api_url
        response = requests.get(
            url,
            params={
                'id': province_code
            },
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print('error get_total_tps_by_province: ' + str(e))
        raise e

def process_all():
    try:
        create_file()
        province_list = get_province_list()
        for province in province_list:
            if province['nama'] == 'Luar Negeri':
                continue
            province_code = province['kode']
            total_tps = get_total_tps_by_province(province_code)
            cities = get_city_list(province_code)
            for city in cities:
                city_code = city['kode']
                city_id = str(city['id'])
                city_name = city['nama']
                total_tps_city = total_tps['result']['aggregated'][city_code]
                print('Processing Province: ' + province['nama'] + ', City: ' + city_name + ', Total TPS: ' + str(total_tps_city[0]['totalTps']))
                with open(result_file, 'a') as f:
                    f.write(province['nama'] + ',' + city_name + ',' + str(total_tps_city[0]['totalTps']) + ',' + city_id + ',' + city_code + '\n')
    except Exception as e:
        print('error process_all: ' + str(e))

if __name__ == '__main__':
    start = time.time()
    print('Start: ' + str(start))
    process_all()
    print('Done: ' + str(time.time() - start))