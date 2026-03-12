import requests
import configuration
import data

def create_order(order_body):
    """Создание нового заказа"""
    return requests.post(configuration.BASE_URL + configuration.CREATE_ORDER_PATH,
                         json=order_body)

def get_order_by_track(track_id):
    """Получение заказа по его треку"""
    params = {"t": track_id}
    return requests.get(configuration.BASE_URL + configuration.GET_ORDER_BY_TRACK_PATH,
                        params=params)