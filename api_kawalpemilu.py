import requests

api_url = 'https://kp24-fd486.et.r.appspot.com/h'

def get_detail_village(village_code):
    try:
        url = api_url
        response = requests.get(
            url,
            params={
                'id': village_code
            },
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print('error get_detail_village: ' + str(e))
        raise e
    