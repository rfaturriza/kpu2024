import pygsheets
import api_kawalpemilu
from api import get_city_list, get_district_list, get_tps_list, get_tps_detail,get_village_list
import time
import json
import os
from datetime import datetime
from multiprocessing import freeze_support
from multiprocessing.pool import ThreadPool
import pandas as pd
import csv


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
    with open(result_file, 'w') as f:
        f.write('ID TPS,KODE TPS,Tanggal Pendataan,Kecamatan,Kelurahan,TPS,Seluruh Paslon,Paslon 01,Paslon 02,Paslon 03,Seluruh Paslon,Paslon 01,Paslon 02,Paslon 03,Link Web KPU,Link Foto C1,Notes Sistem\n')

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
        break

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
        # col A - No (SkIPPED)
        # col B - ID TPS
        # col C - KODE TPS
        # col D - Tanggal Pendataan
        # col E - Kecamatan
        # col F - Kelurahan
        # col G - TPS
        # col H - Seluruh Paslon - KPU
        # col I - Paslon 01
        # col J - Paslon 02
        # col K - Paslon 03
        # col L - Seluruh Paslon - C1 (Kawal Pemilu)
        # col M - Paslon 01
        # col N - Paslon 02
        # col O - Paslon 03
        # col P - Link Web KPU
        # col Q - Link Foto C1
        # col R - Notes Sistem
        # col S - Daftar Id Perubahan Data

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
                polling_result_01 = polling_result[key_01]
                polling_result_02 = polling_result[key_02]              
                polling_result_03 = polling_result[key_03]
                total_polling = polling_result_01 + polling_result_02 + polling_result_03
            except:
                polling_result_01 = ''
                polling_result_02 = ''
                polling_result_03 = ''
                total_polling = ''

            try:
                if data_kawal_pemilu is None:
                    tps_detail_kawal_pemilu = {'pas1': '', 'pas2': '', 'pas3': ''}
                    note_sistem = 'Data Kawal Pemilu Gagal Diambil'
                else:
                    len_kawal_pemilu = len(data_kawal_pemilu['result']['aggregated'][str(index + 1)])
                    tps_detail_kawal_pemilu = data_kawal_pemilu['result']['aggregated'][str(index + 1)][0]

                pas1_kawal_pemilu = tps_detail_kawal_pemilu['pas1']
                pas2_kawal_pemilu = tps_detail_kawal_pemilu['pas2']
                pas3_kawal_pemilu = tps_detail_kawal_pemilu['pas3']
                total_kawal_pemilu = pas1_kawal_pemilu + pas2_kawal_pemilu + pas3_kawal_pemilu

                totalCompletedTPS = tps_detail_kawal_pemilu['totalCompletedTps']
                totalJagaTPS = tps_detail_kawal_pemilu['totalJagaTps']
                totalErrorTPS = tps_detail_kawal_pemilu['totalErrorTps']
                updateTS = tps_detail_kawal_pemilu['updateTs']

                # kalau di kolom utama semua paslon ada angkanya (>=0), 
                # Param TotalCompletedTPS=1
                # Param TotalJagaTPS = 1
                # Param TotalErorTPS >0
                # 2. Data ada, sudah benar namun ada kejanggalan antara Web KPU dan Kawal Pemilu
                if total_kawal_pemilu == 0 and totalCompletedTPS >= 1 and totalJagaTPS >= 1 and totalErrorTPS > 0:
                    note_sistem = 'Admin Perlu Mengecek Kesesuaian Data C1'
                    
                # kalau di kolom utama semua paslon ada angkanya (>=0), 
                # Param TotalCompletedTPS=1
                # Param TotalJagaTPS = 0
                # 3. Data ada, sudah benar namun belum tentu valid
                if total_kawal_pemilu == 0 and totalCompletedTPS >= 1 and totalJagaTPS >= 0:
                    note_sistem = 'Admin Perlu Mengecek Kesesuaian Data C1'

                # kalau di kolom utama semua paslon ada angkanya (tapi semua paslon =0), 
                # Param TotalCompletedTPS=0
                # Param TotalJagaTPS = 0 
                # Param update TS = 0"	
                # 4. Data Kawal Pemilu belum Ada = Tidak ada data C1
                if total_kawal_pemilu == 0 and totalCompletedTPS == 0 and totalJagaTPS == 0 and updateTS == 0:
                    pas1_kawal_pemilu = ''
                    pas2_kawal_pemilu = ''
                    pas3_kawal_pemilu = ''
                    total_kawal_pemilu = ''

                # kalau di kolom utama semua paslon ada angkanya (tapi semua paslon =0), 
                # Param TotalCompletedTPS=0
                # Param TotalJagaTPS = 1 
                # Param update TS > 0
                # Jumlah objek list =1
                # 5. Website Kawal Pemilu Bug, .Foto C1 Gaada, Data pun masih 0, tapi status dibuat terjaga 
                # Baik data KPU atau data Kawal Pemilu belum ada
                if total_kawal_pemilu == 0 and totalCompletedTPS == 0 and totalJagaTPS >= 1 and updateTS > 0 and len_kawal_pemilu == 1:
                    pas1_kawal_pemilu = ''
                    pas2_kawal_pemilu = ''
                    pas3_kawal_pemilu = ''
                    total_kawal_pemilu = ''

                # kalau di kolom utama semua paslon ada angkanya (tapi semua paslon =0), 
                # Param TotalCompletedTPS=0
                # Param TotalJagaTPS = 1
                # Param update TS > 0
                # Jumlah objek list>1
                # Di website KPU sudah ada foto C1, namun di website kawal pemilu belum ada data C1 yang bisa diambil.. jadi harus input manual
                if total_kawal_pemilu == 0 and totalCompletedTPS == 0 and totalJagaTPS >= 1 and updateTS > 0 and len_kawal_pemilu > 1:
                    note_sistem = 'Admin Perlu Mengecek Kesesuaian Data C1'
                    pas1_kawal_pemilu = ''
                    pas2_kawal_pemilu = ''
                    pas3_kawal_pemilu = ''
                    total_kawal_pemilu = ''

            except:
                pas1_kawal_pemilu = ''
                pas2_kawal_pemilu = ''
                pas3_kawal_pemilu = ''
                total_kawal_pemilu = ''
            
            kpu = [str(total_polling), str(polling_result_01), str(polling_result_02), str(polling_result_03)]
            kawal_pemilu = [str(total_kawal_pemilu), str(pas1_kawal_pemilu), str(pas2_kawal_pemilu), str(pas3_kawal_pemilu)]
            to_link_kpu = 'https://pemilu2024.kpu.go.id/pilpres/hitung-suara/' + province_code + '/' + city_code + '/' + district_code + '/' + village_code + '/' + tps_code
            to_link_c1 = tps_detail['images'][1]
            if to_link_c1 == None:
                to_link_c1 = ''
            link = [to_link_kpu, to_link_c1]
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
        wks = sh[1]
        city_name = city['nama']
        city_code = city['kode']
        city_id = str(city['id'])
        id_table = city_id + '/' + city_code
        cell = wks.find(id_table)
        if cell:
            cell = cell[-1]
            work_cell = (cell.row + 13, 2)
            read_data = pd.read_csv(data_csv, skiprows=1, header=None) 
            read_data.fillna('', inplace=True)
            wks.set_dataframe(read_data, work_cell, copy_head=False)
        else :
            print('Sheet: ' + city_name + ' not found')
    except Exception as e:
        print('error update_spreadsheet: ' + str(e))

def process_by_city(province_code, city_code):
    global candidate
    candidate = get_candidate()
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
    create_file(city)
    list_district = get_district_list(province_code, city_code)
    loop_district(list_district, province, city)
    city_name = city['nama']
    try:
        data = 'result/result-' + city_name + '-' + create_file_time + '.csv'
        update_spreadsheet(city, data)
    except Exception as e:
        print('error update_spreadsheet: ' + str(e))

def process_by_province(province_code):
    global candidate
    candidate = get_candidate()
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

if __name__ == '__main__':
    # Measure time
    start = time.time()

    # Process
    freeze_support()
    process_all()
    
    # Measure time
    end = time.time()
    time_executed_minutes = (end - start) / 60
    
    print('Time Executed:', time_executed_minutes, 'minutes')
    