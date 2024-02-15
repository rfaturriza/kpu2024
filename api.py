import requests

url = 'https://pemilu2024.kpu.go.id/'
api_url = 'https://sirekap-obj-data.kpu.go.id/'
api_ppwp = 'wilayah/pemilu/ppwp/'
api_hhcw_ppwp = 'pemilu/hhcw/ppwp/'
api_enpoint_list_province = 'wilayah/pemilu/ppwp/0.json'
# https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/11.json
# [
#     {
#         "nama": "ACEH BARAT",
#         "id": 191126,
#         "kode": "1105",
#         "tingkat": 2
#     },
api_enpoint_list_city = 'wilayah/pemilu/ppwp/11.json'
# https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/11/1105.json
# [
#     {
#         "nama": "ARONGAN LAMBALEK",
#         "id": 101710,
#         "kode": "110507",
#         "tingkat": 3
#     },
api_enpoint_list_district = 'wilayah/pemilu/ppwp/11/1105.json'
# https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/11/1105/110507.json
# [
#     {
#         "nama": "ALUE BAGOK",
#         "id": 101712,
#         "kode": "1105072002",
#         "tingkat": 4
#     },
api_enpoint_list_village = 'wilayah/pemilu/ppwp/11/1105/110507.json'
# https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/11/1105/110507/1105072002.json
# [
#     {
#         "nama": "TPS 001",
#         "id": 9459001,
#         "kode": "1105072002001",
#         "tingkat": 5
#     },
api_enpoint_list_tps = 'wilayah/pemilu/ppwp/11/1105/110507/1105072002.json'
# https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/ppwp/11/1105/110507/1105072002/1105072002002.json
# {
#     "chart": {
#         "null": null,
#         "100025": 17,
#         "100026": 124,
#         "100027": 9
#     },
#     "images": [
#         "https://sirekap-obj-formc.kpu.go.id/5282/pemilu/ppwp/92/03/01/10/02/9203011002010-20240214-131814--5a6f829e-0c68-4943-9e56-c320d652a807.jpg",
#         "https://sirekap-obj-formc.kpu.go.id/5282/pemilu/ppwp/92/03/01/10/02/9203011002010-20240214-132020--c7ad754d-e88c-4599-bef6-df83dc8080c9.jpg",
#         "https://sirekap-obj-formc.kpu.go.id/5282/pemilu/ppwp/92/03/01/10/02/9203011002010-20240214-132305--5f5fe6c1-6241-4b8d-bca1-ef3b6d5893aa.jpg"
#     ],
#     "administrasi": {
#         "suara_sah": 150,
#         "suara_total": 151,
#         "pemilih_dpt_j": 201,
#         "pemilih_dpt_l": 103,
#         "pemilih_dpt_p": 98,
#         "pengguna_dpt_j": 135,
#         "pengguna_dpt_l": 62,
#         "pengguna_dpt_p": 73,
#         "pengguna_dptb_j": 0,
#         "pengguna_dptb_l": 0,
#         "pengguna_dptb_p": 0,
#         "suara_tidak_sah": 1,
#         "pengguna_total_j": 151,
#         "pengguna_total_l": 73,
#         "pengguna_total_p": 78,
#         "pengguna_non_dpt_j": 16,
#         "pengguna_non_dpt_l": 11,
#         "pengguna_non_dpt_p": 5
#     },
#     "psu": null,
#     "ts": "2024-02-14 21:46:01",
#     "status_suara": true,
#     "status_adm": true
# }
api_enpoint_list_tps_detail = 'pemilu/hhcw/ppwp/11/1105/110507/1105072002/1105072002002.json'
# https://sirekap-obj-data.kpu.go.id/pemilu/ppwp.json
# {
#     "100025": {
#         "ts": "2024-02-14 18:44:00",
#         "nama": "H. ANIES RASYID BASWEDAN, Ph.D. - Dr. (H.C.) H. A. MUHAIMIN ISKANDAR",
#         "warna": "#8CB9BD",
#         "nomor_urut": 1
#     },
#     "100026": {
#         "ts": "2024-02-14 18:44:00",
#         "nama": "H. PRABOWO SUBIANTO - GIBRAN RAKABUMING RAKA",
#         "warna": "#C7B7A3",
#         "nomor_urut": 2
#     },
#     "100027": {
#         "ts": "2024-02-14 18:44:00",
#         "nama": "H. GANJAR PRANOWO, S.H., M.I.P. - Prof. Dr. H. M. MAHFUD MD",
#         "warna": "#B67352",
#         "nomor_urut": 3
#     }
# }
api_candidate = 'pemilu/ppwp.json'

def get_province_list():
    url = api_url + api_enpoint_list_province
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_city_list(province_id):
    url = api_url + api_ppwp + province_id + '.json'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_district_list(province_id, city_id):
    url = api_url + api_ppwp + province_id + '/' + city_id + '.json'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_village_list(province_id, city_id, district_id):
    url = api_url + api_ppwp + province_id + '/' + city_id + '/' + district_id + '.json'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_tps_list(province_id, city_id, district_id, village_id):
    url = api_url + api_ppwp + province_id + '/' + city_id + '/' + district_id + '/' + village_id + '.json'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_tps_detail(province_id, city_id, district_id, village_id, tps_id):
    url = api_url + api_hhcw_ppwp + province_id + '/' + city_id + '/' + district_id + '/' + village_id + '/' + tps_id + '.json'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_candidate_list():
    url = api_url + api_candidate
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    