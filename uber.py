import api_service
from config_api import UBER
from decouple import config

CID = config('UBR_CID')
CSEC = config('UBR_CSEC')


def getAllStoresSTATUS():
    uber_api = api_service.ApiService()
    p_data = {'client_id': CID,
              'client_secret': CSEC,
              'grant_type': 'client_credentials',
              'scope': 'eats.store'}

    auth_api_resp = uber_api.post(UBER["login_url"], d=p_data)

    all_stores_resp = uber_api.get(UBER["get_stores"],
                                   headers={"Authorisation": 'Bearer {token}'.format(token=auth_api_resp.access_token)})
    store_status = []
    for store in all_stores_resp.stores:
        s_id = store["store_id"]
        s_name = store["name"] + store["location"]["address"]
        status_resp = uber_api.get(end_point=UBER['store_status'] + '{store_id}/status'.format(store_id=s_id))
        store_status.append({"name": s_name, "status": status_resp['status']})

    return store_status


if __name__ == '__main__':
    getAllStoresSTATUS()
