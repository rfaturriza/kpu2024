from multiprocessing.pool import ThreadPool
import time
from bs4 import BeautifulSoup
import requests
import math
from multiprocessing import Pool
from multiprocessing import freeze_support
from api import get_province_list, get_city_list, get_district_list, get_village_list, get_tps_list, get_tps_detail, get_candidate_list
import json

candidate = get_candidate_list()

# CREATE FILE RESULT AND ERROR RESULT CSV
timestamp = str(int(time.time()))
result_file = 'result' + timestamp + '.csv'
error_result_file = 'error_result' + timestamp + '.csv'

def create_file():
    with open(result_file, 'w') as f:
        f.write('Provinsi,Kabupaten/Kota,Kecamatan,Kelurahan,No TPS,Keterangan\n')
    with open(error_result_file, 'w') as f:
        f.write('Provinsi,Kabupaten/Kota,Kecamatan,Kelurahan,No TPS,Keterangan\n')

def loop_city(province):
    province_code = province['kode']
    list_city = get_city_list(province_code)
    for city in list_city:
        city_code = city['kode']
        list_district = get_district_list(province_code, city_code)
        loop_district(list_district)

def loop_district(districts, province, city):
    province_code = province['kode']
    city_code = city['kode']
    for district in districts:
        district_code = district['kode']
        list_village = get_village_list(province_code, city_code, district_code)
        loop_village(list_village)

def loop_village(villages, province, city, district):
    province_code = province['kode']
    city_code = city['kode']
    district_code = district['kode']
    for village in villages:
        village_code = village['kode']
        list_tps = get_tps_list(province_code, city_code, district_code, village_code)
        loop_tps(list_tps)

def loop_tps(list_tps, province, city, district, village):
    province_code = province['kode']
    city_code = city['kode']
    district_code = district['kode']
    village_code = village['kode']

    for tps in list_tps:
        print_text = province['nama'] + ',' + city['nama'] + ',' + district['nama'] + ',' + village['nama'] + ',' + tps['nama']
        try:
            tps_code = tps['kode']
            tps_detail = get_tps_detail(province_code, city_code, district_code, village_code, tps_code)

            key_01 = list(candidate.keys())[0]
            key_02 = list(candidate.keys())[1]
            key_03 = list(candidate.keys())[2]

            polling_result = tps_detail['chart']
            polling_result_01 = polling_result[key_01]
            polling_result_02 = polling_result[key_02]              
            polling_result_03 = polling_result[key_03]

            total_polling = polling_result_01 + polling_result_02 + polling_result_03
            administation = tps_detail['administrasi']
            total_valid_polling = administation['suara_sah']
            
            # CHECK VALIDATION
            if total_polling != total_valid_polling:
                note = ''
                if total_polling > total_valid_polling:
                    note = 'Suara Paslon LEBIH dari suara sah'
                else:
                    note = 'Suara Paslon KURANG dari suara sah'
                f = open(result_file, 'a')
                f.write(print_text + ', ' + note + ' [Total Suara Paslon:' + str(total_polling) + '] [Total Suara Sah:' + str(total_valid_polling) + ']' + '\n')
        except:
            f = open(error_result_file, 'a')
            f.write(print_text + ', ' + 'Data Belum Lengkap' + '\n')
            continue

def main():
    start = time.clock()
    provinces_json_file = open('province.json')
    provinces = json.load(provinces_json_file)

    # create a thread pool for multi processing
    with ThreadPool() as pool:
        # call the function for each item concurrently
        pool.map(loop_city, provinces)

    print("processing time: {}mins\n".format((time.clock()-start)/60))
                        
if __name__ == "__main__":
    freeze_support()   # required to use multiprocessing
    create_file()
    main()
