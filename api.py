import requests

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
            return None
    except requests.exceptions.Timeout:
        get_province_list()
    except Exception as e:
        raise e

def get_city_list(province_id):
    url = api_url + enpoint_ppwp + province_id + '.json'
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.Timeout:
        get_city_list(province_id)
    except Exception as e:
        raise e

def get_district_list(province_id, city_id):
    url = api_url + enpoint_ppwp + province_id + '/' + city_id + '.json'
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.Timeout:
        get_district_list(province_id, city_id)
    except Exception as e:
        raise e

def get_village_list(province_id, city_id, district_id):
    url = api_url + enpoint_ppwp + province_id + '/' + city_id + '/' + district_id + '.json'
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.Timeout:
        get_village_list(province_id, city_id, district_id)
    except Exception as e:
        raise e

def get_tps_list(province_id, city_id, district_id, village_id):
    url = api_url + enpoint_ppwp + province_id + '/' + city_id + '/' + district_id + '/' + village_id + '.json'
    try:
        
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.Timeout:
        get_tps_list(province_id, city_id, district_id, village_id)
    except Exception as e:
        raise e

def get_tps_detail(province_id, city_id, district_id, village_id, tps_id):
    url = api_url + enpoint_hhcw_ppwp + province_id + '/' + city_id + '/' + district_id + '/' + village_id + '/' + tps_id + '.json'
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.Timeout:
        get_tps_detail(province_id, city_id, district_id, village_id, tps_id)
    except Exception as e:
        raise e

def get_candidate_list():
    url = api_url + endpoint_candidate
    response = requests.get(url, timeout=30)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    