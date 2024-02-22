import pygsheets
import api_kawalpemilu
from api import get_city_list, get_district_list, get_tps_list, get_tps_detail,get_village_list
import time
import json
import os
from datetime import datetime
import pandas as pd
import csv
import sys
import traceback

def get_candidate():
    candidate_json_file = open('data/candidates.json')
    candidate = json.load(candidate_json_file)
    return candidate

def get_province_list():
    province_file = open('data/province.json')
    province_json = json.load(province_file)
    return province_json

def create_file(city):
    global create_file_time 
    create_file_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    city_name = city['nama']
    global result_file
    result_file = 'result/result-' + city_name + '-' + create_file_time + '.csv'
    if not os.path.exists('result'):
        os.makedirs('result')
    with open(result_file, 'w') as f:
        f.write('ID TPS,KODE TPS,Tanggal Pendataan,Kecamatan,Kelurahan,TPS,Seluruh Paslon,Paslon 01,Paslon 02,Paslon 03,Seluruh Paslon,Paslon 01,Paslon 02,Paslon 03,Link Web KPU,Link Foto C1,Link Kawal Pemilu,Notes Sistem\n')

def setup():
    gc = pygsheets.authorize(service_file='kpu2024-dca0549f3753.json')
    id_test = '129h_iw2er5z5CXF3sN-XVQ1of3bZDv2uqwcCcRSuwaY'
    id_sheet = '1fC2mEHpnY_pH_vzWrNBRasD4OpHU-8Fs2RvKa-xG0E0'

    sh = gc.open_by_key(id_test)
    return sh

def loop_city(province):
    province_code = province['kode']
    list_city = get_city_list(province_code)
    for city in list_city:
        create_file(city)
        city_code = city['kode']
        list_district = get_district_list(province_code, city_code)
        loop_district(list_district, province, city)
    # with ThreadPool() as pool:
    #     items = [(districts, province, city) for city in list_city for districts in [get_district_list(province_code, city['kode'])]]
    #     pool.starmap(loop_district, items)
        city_name = city['nama']
        data = 'result/result-' + city_name + '-' + create_file_time + '.csv'
        update_spreadsheet(city, data)
        # TODO:Remove this break
        # break

def loop_district(districts, province, city):
    province_code = province['kode']
    city_code = city['kode']
    for district in districts:
        district_code = district['kode']
        list_village = get_village_list(province_code, city_code, district_code)
        loop_village(list_village, province, city, district)
        # TODO:Remove this break
        # break

def loop_village(villages, province, city, district):
    province_code = province['kode']
    city_code = city['kode']
    district_code = district['kode']
    for village in villages:
        village_code = village['kode']
        list_tps = get_tps_list(province_code, city_code, district_code, village_code)
        loop_tps(list_tps, province, city, district, village)

        # TODO:Remove this break
        # break

def loop_tps(list_tps, province, city, district, village):
    province_code = province['kode']
    city_code = city['kode']
    district_code = district['kode']
    village_code = village['kode']
    try:
        data_kawal_pemilu = api_kawalpemilu.get_detail_village(village_code)
    except Exception as e:
        print('error get_detail_village: ' + str(e))
        data_kawal_pemilu = None

    for index, tps in enumerate(list_tps):
        # Prevent rate limit connection
        # global count_loop
        # count_loop += 1
        # if (count_loop) % 100 == 0:
        #     time.sleep(30)

        identifier = [str(tps['id']) , tps['kode'] , time.strftime('%Y-%m-%d %H:%M:%S') , district['nama'] , village['nama'],tps['nama']]
        try:
            tps_code = tps['kode']
            tps_detail = get_tps_detail(province_code, city_code, district_code, village_code, tps_code)
            note_sistem = ''

            try:
                key_01 = list(candidate.keys())[0]
                key_02 = list(candidate.keys())[1]
                key_03 = list(candidate.keys())[2]

                polling_result = tps_detail['chart']
                pas1_kpu = polling_result[key_01]
                pas2_kpu = polling_result[key_02]              
                pas3_kpu = polling_result[key_03]
                total_kpu = pas1_kpu + pas2_kpu + pas3_kpu
            except:
                pas1_kpu = ''
                pas2_kpu = ''
                pas3_kpu = ''
                total_kpu = ''

            try:
                if pas1_kpu == '' and pas2_kpu == '' and pas3_kpu == '':
                    raise Exception('Data KPU Kosong')
                
                if data_kawal_pemilu is None:
                    tps_detail_kawal_pemilu_main = {'pas1': '', 'pas2': '', 'pas3': ''}
                    note_sistem = 'Data Kawal Pemilu Gagal Diambil'
                else:
                    try:
                        tps_number = int(tps['nama'].split(' ')[1])
                    except:
                        tps_number = index + 1
                    list_tps_detail_kawal_pemilu = data_kawal_pemilu['result']['aggregated'][str(tps_number)]
                    len_kawal_pemilu = len(list_tps_detail_kawal_pemilu)
                    tps_detail_kawal_pemilu_main = list_tps_detail_kawal_pemilu[0]

                pas1_kawal_pemilu = tps_detail_kawal_pemilu_main['pas1']
                pas2_kawal_pemilu = tps_detail_kawal_pemilu_main['pas2']
                pas3_kawal_pemilu = tps_detail_kawal_pemilu_main['pas3']
                total_kawal_pemilu = pas1_kawal_pemilu + pas2_kawal_pemilu + pas3_kawal_pemilu

                totalCompletedTPS = 0
                totalJagaTPS = 0
                totalErrorTPS = 0
                updateTS = 0
                if 'totalCompletedTps' in tps_detail_kawal_pemilu_main:
                    totalCompletedTPS = tps_detail_kawal_pemilu_main['totalCompletedTps']
                if 'totalJagaTps' in tps_detail_kawal_pemilu_main:
                    totalJagaTPS = tps_detail_kawal_pemilu_main['totalJagaTps']
                if 'totalErrorTps' in tps_detail_kawal_pemilu_main:
                    totalErrorTPS = tps_detail_kawal_pemilu_main['totalErrorTps']
                if 'updateTs' in tps_detail_kawal_pemilu_main:
                    updateTS = tps_detail_kawal_pemilu_main['updateTs']

                # 1. Data ada, sudah benar dan valid
                # KU Nilai Semua Paslon >=0
                # TotalCompletedTPS= 1
                # TotalJagaTPS = 1
                # TotalErrorTPS = 0 
                # Update TS >0
                # Objek list >1
                is1Fullfilled = total_kawal_pemilu >= 0 and totalCompletedTPS >= 1 and totalJagaTPS >= 1 and totalErrorTPS == 0 and updateTS > 0 and len_kawal_pemilu > 1

                # 2. Data ada, sudah benar namun ada kejanggalan antara Web KPU dan Kawal Pemilu
                # KU Nilai Semua Paslon >=0
                # TotalCompletedTPS= 1
                # TotalJagaTPS = 1
                # TotalErrorTPS >0 
                # Update TS >0
                # Objek list >1
                is2Fullfilled = total_kawal_pemilu >= 0 and totalCompletedTPS >= 1 and totalJagaTPS >= 1 and totalErrorTPS > 0 and updateTS > 0 and len_kawal_pemilu > 1
                    
                # 3. Data ada, sudah benar namun belum tentu valid
                # KU Nilai Semua Paslon >=0
                # TotalCompletedTPS= 1
                # TotalJagaTPS = 0
                # TotalErrorTPS = 0 
                # Update TS >0
                # Objek list >1
                is3Fullfilled = total_kawal_pemilu >= 0 and totalCompletedTPS >= 1 and totalJagaTPS == 0 and totalErrorTPS == 0 and updateTS > 0 and len_kawal_pemilu > 1

                # 4. Data Kawal Pemilu belum Ada = Tidak ada data C1
                # KU Nilai Semua Paslon = 0
                # TotalCompletedTPS= 0
                # TotalJagaTPS = 0
                # TotalErrorTPS = 0 
                # Update TS =0
                # Objek list =1
                is4Fullfilled = total_kawal_pemilu == 0 and totalCompletedTPS == 0 and totalJagaTPS == 0 and totalErrorTPS == 0 and updateTS == 0 and len_kawal_pemilu == 1
                if is4Fullfilled:
                    raise Exception('Data Kawal Pemilu Kosong')

                # 5. Website Kawal Pemilu Bug, .Foto C1 Gaada, Data pun masih 0, tapi status dibuat terjaga 
                # Baik data KPU atau data Kawal Pemilu belum ada
                # KU Nilai Semua Paslon = 0
                # TotalCompletedTPS= 0
                # TotalJagaTPS = 1
                # TotalErrorTPS = 0 
                # Update TS > 0
                # Objek list =1
                is5Fullfilled = total_kawal_pemilu == 0 and totalCompletedTPS == 0 and totalJagaTPS >= 1 and totalErrorTPS ==0 and updateTS > 0 and len_kawal_pemilu == 1
                if is5Fullfilled:
                    raise Exception('Data Kawal Pemilu Kosong')

                # 6. Data kawal pemilu masih 0, padahal c1 nya udah ada
                # KU Nilai Semua Paslon >=0
                # TotalCompletedTPS= 0
                # TotalJagaTPS >= 0
                # TotalErrorTPS >= 0 
                # Update TS >0
                # Objek list >1
                is6Fullfilled = total_kawal_pemilu >= 0 and totalCompletedTPS == 0 and totalJagaTPS >= 0 and totalErrorTPS >= 0 and updateTS > 0 and len_kawal_pemilu > 1

                # 7. di webiste kawal pemilu sudah ada foto C1, namun di website kawal pemilu belum ada data C1 yang bisa diambil.. jadi harus input manual
                # KU Nilai Semua Paslon >=0
                # TotalCompletedTPS= 0
                # TotalJagaTPS >= 0
                # TotalErrorTPS >= 0 
                # Update TS >0
                # Objek list >1
                is7Fullfilled = total_kawal_pemilu >= 0 and totalCompletedTPS == 0 and totalJagaTPS >= 0 and totalErrorTPS >= 0 and updateTS > 0 and len_kawal_pemilu > 1

                if is1Fullfilled or is2Fullfilled or is3Fullfilled or is6Fullfilled or is7Fullfilled:
                    if total_kawal_pemilu == 0:
                        for i in range(1, len_kawal_pemilu):
                            pas1_kawal_pemilu = list_tps_detail_kawal_pemilu[i]['pas1']
                            pas2_kawal_pemilu = list_tps_detail_kawal_pemilu[i]['pas2']
                            pas3_kawal_pemilu = list_tps_detail_kawal_pemilu[i]['pas3']
                            total_kawal_pemilu = pas1_kawal_pemilu + pas2_kawal_pemilu + pas3_kawal_pemilu
                            if total_kawal_pemilu > 0:
                                break
                        note_sistem = 'Admin Perlu Mengecek Kesesuaian Data C1'
                    else:
                        for i in range(1, len_kawal_pemilu):
                            pas1_kawal_pemilu_temp = list_tps_detail_kawal_pemilu[i]['pas1']
                            pas2_kawal_pemilu_temp = list_tps_detail_kawal_pemilu[i]['pas2']
                            pas3_kawal_pemilu_temp = list_tps_detail_kawal_pemilu[i]['pas3']
                            if pas1_kawal_pemilu != pas1_kawal_pemilu_temp or pas2_kawal_pemilu != pas2_kawal_pemilu_temp or pas3_kawal_pemilu != pas3_kawal_pemilu_temp:
                                note_sistem = 'Admin Perlu Mengecek Kesesuaian Data C1'
                                break


            except Exception as e:
                pas1_kawal_pemilu = ''
                pas2_kawal_pemilu = ''
                pas3_kawal_pemilu = ''
                total_kawal_pemilu = ''
                if (str(e) == 'Data Kawal Pemilu Kosong'):
                    note_sistem = 'Data C1 Kawal Pemilu Kosong'

                if str(e) != 'Data KPU Kosong' and str(e) != 'Data Kawal Pemilu Kosong':
                    print('error: ' + ', '.join(identifier) + ' ' + str(traceback.format_exc()))
            
            kpu = [str(total_kpu), str(pas1_kpu), str(pas2_kpu), str(pas3_kpu)]
            kawal_pemilu = [str(total_kawal_pemilu), str(pas1_kawal_pemilu), str(pas2_kawal_pemilu), str(pas3_kawal_pemilu)]
            to_link_kpu = 'https://pemilu2024.kpu.go.id/pilpres/hitung-suara/' + province_code + '/' + city_code + '/' + district_code + '/' + village_code + '/' + tps_code
            to_link_kpu = '=HYPERLINK("' + to_link_kpu + '","Link KPU")'
            to_link_kawal_pemilu = 'https://kawalpemilu.org/h/' + str(village_code)
            to_link_kawal_pemilu = '=HYPERLINK("' + to_link_kawal_pemilu + '","Link Kawal Pemilu")'
            try:
                to_link_c1 = tps_detail['images'][1]
                to_link_c1 = '=HYPERLINK("' + to_link_c1 + '","Link Foto C1")'
            except:
                to_link_c1 = ''
            link = [to_link_kpu, to_link_c1, to_link_kawal_pemilu]
            write_data = identifier + kpu + kawal_pemilu + link + [note_sistem]

            with open(result_file, 'a') as f:
                writer = csv.writer(f)
                writer.writerow(write_data)

        except Exception as e:
            print('error: ' + ', '.join(identifier) + ' ' + str(e))
            continue

def update_spreadsheet(city, data_csv):
    try:
        sh = setup()
        city_name = city['nama']
        wks = sh.worksheet_by_title(city_name.upper())
        work_cell = (22, 3)
        read_data = pd.read_csv(data_csv, skiprows=1, header=None) 
        read_data.fillna('', inplace=True)
        wks.set_dataframe(read_data, work_cell, copy_head=False)
    except Exception as e:
        print('error update_spreadsheet: ' + str(traceback.format_exc()))
        
def is_spreadsheet_exist(city_name):
    try:
        sh = setup()
        wks = sh.worksheet_by_title(city_name.upper())
        return True
    except:
        return False
    
def process_by_city(province_code, city_code):
    global candidate, count_loop
    candidate = get_candidate()
    count_loop = 0
    city = None
    for c in get_city_list(province_code):
        if c['kode'] == city_code:
            city = c
            break
    province_json = get_province_list()
    province = None
    for p in province_json:
        if p['kode'] == province_code:
            province = p
            break
    city_name = city['nama']
    create_file(city)
    if is_spreadsheet_exist(city_name) == False:
        print('Sheet not exist')
        return
    
    list_district = get_district_list(province_code, city_code)
    loop_district(list_district, province, city)
    try:
        data = 'result/result-' + city_name + '-' + create_file_time + '.csv'
        update_spreadsheet(city, data)
    except Exception as e:
        print('error update_spreadsheet: ' + str(e))

def process_by_province(province_code):
    global candidate, count_loop
    candidate = get_candidate()
    count_loop = 0
    provinces = get_province_list()
    province = None
    for p in provinces:
        if p['kode'] == province_code:
            province = p
            break
    loop_city(province)

def process_all():
    global candidate
    candidate = get_candidate()
    provinces = get_province_list()
    for province in provinces:
        process_by_province(province['kode'])

def ask_input():
    print('Choose Process:')
    print('1. All')
    print('2. By Province')
    print('3. By City')
    print('00. Exit')
    process = input()
    if process == '1':
        print('Processing All')
        process_all()
    elif process == '2':
        print('Input Province Code:')
        province_code = input()
        print('Processing By Province')
        process_by_province(province_code)
    elif process == '3':
        print('Input Province Code:')
        province_code = input()
        print('Input City Code:')
        city_code = input()
        print('Processing By City')
        process_by_city(province_code, city_code)
    elif process == '00':
        print('Exit')
        sys.exit()
    else:
        print('Invalid Input')
        ask_input()

if __name__ == '__main__':
    # Measure time
    start = time.time()
    print('Starting at:', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # Process
    ask_input()
    
    # Measure time
    end = time.time()
    time_executed_minutes = (end - start) / 60
    print('Time Executed:', time_executed_minutes, 'minutes')
    