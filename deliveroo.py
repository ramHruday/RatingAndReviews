import base64
from decouple import config
import api_service
from config_api import DELIVEROO

USRNAME = config('DLVRO_USERNAME')
UPWD = config('DLVRO_PWD')


def getAllStoresSTATUS(brand_id):
    deliveroo = api_service.ApiService()

    string = USRNAME + ":" + UPWD
    token = base64.b64encode(string.encode('utf-8'))
    headers = {
        "accept": "application/json",
        "authorization": "Basic {token}".format(token=token)
    }

    # get stores for brand_id
    stores_url = DELIVEROO['store_url'] + f'{brand_id}/sites'
    stores_resp = deliveroo.get(stores_url, headers)

    # get status for each store for brand_id
    store_status = []
    for store in stores_resp.sites:
        status_url = DELIVEROO['store_status'] + '{b_id}/sites/{s_id}/status'.format(b_id=brand_id,
                                                                                     s_id=store['location_id'])
        status_resp = deliveroo.get(status_url, headers=headers)
        store_status.append({"name": store['name'], "status": status_resp['status']})


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    getAllStoresSTATUS(280021)
