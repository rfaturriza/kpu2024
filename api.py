import requests
import traceback
import json

url = 'https://pemilu2024.kpu.go.id/'
api_url = 'https://sirekap-obj-data.kpu.go.id/'
enpoint_ppwp = 'wilayah/pemilu/ppwp/'
enpoint_hhcw_ppwp = 'pemilu/hhcw/ppwp/'
api_enpoint_list_province = 'wilayah/pemilu/ppwp/0.json'
endpoint_candidate = 'pemilu/ppwp.json'

# Example fetch url Kabupaten/Kota 'wilayah/pemilu/ppwp/11.json'
# wilayah/pemilu/ppwp/${province_code}.json

# Example fetch url Kecamatan 'wilayah/pemilu/ppwp/11/1105.json'
# wilayah/pemilu/ppwp/${province_code}/${city_code}.json

# Example fetch url Kelurahan/Desa 'wilayah/pemilu/ppwp/11/1105/110507.json'
# wilayah/pemilu/ppwp/${province_code}/${city_code}/${district_code}.json

# Example fetch url TPS 'pemilu/hhcw/ppwp/11/1105/110507/1105072002.json'
# pemilu/hhcw/ppwp/${province_code}/${city_code}/${district_code}/${village_code}/${tps_code}.json

# Example fetch url TPS Detail 'pemilu/hhcw/ppwp/11/1105/110507/1105072002/1105072002002.json'
# pemilu/hhcw/ppwp/${province_code}/${city_code}/${district_code}/${village_code}/${tps_code}/${tps_code}.json

def get_province_list():
    try:
        url = api_url + api_enpoint_list_province
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            get_province_list()
    except:
        print(f'Error get_province_list: {url}, {traceback.format_exc()}')
        get_province_list()

def get_city_list(province_id):
    json_file = f'data/{province_id}.json'
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
            return data
    except:
        pass
    url = api_url + enpoint_ppwp + province_id + '.json'
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            with open(json_file, 'w') as f:
                json.dump(response.json(), f)
            return response.json()
        else:
            get_city_list(province_id)
    except:
        print(f'Error get_city_list: {url}, {traceback.format_exc()}')
        get_city_list(province_id)

def get_district_list(province_id, city_id):
    url = api_url + enpoint_ppwp + province_id + '/' + city_id + '.json'
    json_file = f'data/{city_id}.json'
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
            return data
    except:
        pass
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            with open(json_file, 'w') as f:
                json.dump(response.json(), f)
            return response.json()
        else:
            get_district_list(province_id, city_id)
    except:
        print(f'Error get_district_list: {url}, {traceback.format_exc()}')
        get_district_list(province_id, city_id)

def get_village_list(province_id, city_id, district_id):
    json_file = f'data/{district_id}.json'
    url = api_url + enpoint_ppwp + province_id + '/' + city_id + '/' + district_id + '.json'
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
            return data
    except:
        pass
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            with open(json_file, 'w') as f:
                json.dump(response.json(), f)
            return response.json()
        else:
            get_village_list(province_id, city_id, district_id)
    except:
        print(f'Error get_village_list: {url}, {traceback.format_exc()}')
        get_village_list(province_id, city_id, district_id)

def get_tps_list(province_id, city_id, district_id, village_id):
    json_file = f'data/{village_id}.json'
    url = api_url + enpoint_ppwp + province_id + '/' + city_id + '/' + district_id + '/' + village_id + '.json'
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
            return data
    except:
        pass
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            with open(json_file, 'w') as f:
                json.dump(response.json(), f)
            return response.json()
        else:
            get_tps_list(province_id, city_id, district_id, village_id)
    except:
        print(f'Error get_tps_list: {url}, {traceback.format_exc()}')
        get_tps_list(province_id, city_id, district_id, village_id)

def get_tps_detail(province_id, city_id, district_id, village_id, tps_id):
    url = api_url + enpoint_hhcw_ppwp + province_id + '/' + city_id + '/' + district_id + '/' + village_id + '/' + tps_id + '.json'
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            get_tps_detail(province_id, city_id, district_id, village_id, tps_id)
    except:
        print(f'Error get_tps_detail: {url}, {traceback.format_exc()}')
        get_tps_detail(province_id, city_id, district_id, village_id, tps_id)

def get_kelurahan_detail(province_id, city_id, district_id, village_id):
    url = api_url + enpoint_hhcw_ppwp + province_id + '/' + city_id + '/' + district_id + '/' + village_id + '.json'
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            get_kelurahan_detail(province_id, city_id, district_id, village_id)
    except:
        print(f'Error get_kelurahan_detail: {url}, {traceback.format_exc()}')
        get_kelurahan_detail(province_id, city_id, district_id, village_id)

def get_kecamatan_detail(province_id, city_id, district_id):
    url = api_url + enpoint_hhcw_ppwp + province_id + '/' + city_id + '/' + district_id + '.json'
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            get_kecamatan_detail(province_id, city_id, district_id)
    except:
        print(f'Error get_kelurahan_detail: {url}, {traceback.format_exc()}')
        get_kecamatan_detail(province_id, city_id, district_id)

def get_candidate_list():
    url = api_url + endpoint_candidate
    response = requests.get(url, timeout=30)
    if response.status_code == 200:
        return response.json()
    else:
        get_candidate_list()
    