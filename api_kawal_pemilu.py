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
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.Timeout:
        get_detail_village(village_code)
    except Exception as e:
        raise e
    