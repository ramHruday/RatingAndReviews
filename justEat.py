import api_service
from config_api import JUST_EAT
from decouple import config

CID = config('JST_ID')
CSEC = config('JST_CSEC')


def getAllStoresSTATUS():
    just_eat_api = api_service.ApiService()
    p_data = {'client_id': CID,
              'client_secret': CSEC,
              'grant_type': 'client_credentials',
              'scope': 'eats.store'}
    auth_api_resp = just_eat_api.post(JUST_EAT["login_url"], d=p_data)

    headers = {'X-JE-Requester': "RRR", "Authorisation": 'Bearer {token}'.format(
        token=auth_api_resp.access_token)}

    all_stores_resp = just_eat_api.get(JUST_EAT["get_stores"],
                                       headers=headers)
    store_status = []
    for store in all_stores_resp.stores:
        s_id = store["id"]
        s_name = store["name"]
        status_resp = just_eat_api.get(
            end_point=JUST_EAT['store_status'] + '{store_id}/availability/scheduled-unavailabilities'.format(
                store_id=s_id), headers=headers)
        store_status.append({"name": s_name, "status": status_resp['status']})

    return store_status


if __name__ == '__main__':
    getAllStoresSTATUS()
#     136452/availability/scheduled-unavailabilities
