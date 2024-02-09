import json

APPLICATION_JSON = 'application/json'


def test_list_items_by_purchase_order_id(test_client, get_headers, purchase_items_on_db):
    purchase_order_id = purchase_items_on_db['purchase_order']['id']
    url = f'/purchase_orders/{purchase_order_id}/items'

    response = test_client.get(path=url, headers=get_headers)

    assert response.status_code == 200
    assert len(response.json) == 2


def test_post_items_by_purchase_order_id(test_client, get_headers, purchase_on_db):
    purchase_order_id = purchase_on_db.id
    url = f'/purchase_orders/{purchase_order_id}/items'

    item_obj = {
        'description': 'Item teste1',
        'price': 10.0,
        'quantity': 5
    }

    response = test_client.post(
        path=url,
        headers=get_headers,
        data=json.dumps(item_obj),
        content_type=APPLICATION_JSON
    )

    assert response.status_code == 200
    assert len(response.json) == 5
    assert response.json['id'] is not None
    assert response.json['description'] == item_obj['description']
    assert response.json['price'] == item_obj['price']
    assert response.json['quantity'] == item_obj['quantity']


def test_get_items_by_purchase_order_id_not_found(test_client, get_headers):
    _id = 9999
    message = f'Purchase order id {_id} not found'
    url = f'/purchase_orders/{_id}/items'

    response = test_client.get(path=url, headers=get_headers)

    assert response.status_code == 200
    assert response.json['message'] == message


def test_post_purchase_order_item_invalid_quantity(test_client, get_headers, purchase_items_on_db):
    purchase_order_id = purchase_items_on_db['purchase_order']['id']
    url = f'/purchase_orders/{purchase_order_id}/items'

    obj = {
        'description': 'Item teste2',
        'price': 10.0,
        'quantity': 250
    }

    message = 'You can add only 100 more items'

    response = test_client.post(
        path=url,
        headers=get_headers,
        data=json.dumps(obj),
        content_type=APPLICATION_JSON,
    )

    assert response.status_code == 400
    assert response.json['message'] == message


def test_post_invalid_quantity(test_client, get_headers, purchase_on_db):
    purchase_order_id = purchase_on_db.id
    url = f'/purchase_orders/{purchase_order_id}/items'

    obj = {
        'price': 10.0,
        'description': 'Teste invalid quantity'
    }

    response = test_client.post(
        path=url,
        headers=get_headers,
        data=json.dumps(obj),
        content_type=APPLICATION_JSON,
    )

    assert response.status_code == 400
    assert response.json['message']['quantity'] == 'Inform a valid quantity'


def test_post_invalid_description(test_client, get_headers, purchase_on_db):
    purchase_order_id = purchase_on_db.id
    url = f'/purchase_orders/{purchase_order_id}/items'

    obj = {
        'price': 10.0,
        'quantity': 5
    }

    response = test_client.post(
        path=url,
        headers=get_headers,
        data=json.dumps(obj),
        content_type=APPLICATION_JSON,
    )

    assert response.status_code == 400
    assert response.json['message']['description'] == 'Inform a valid description'


def test_post_invalid_price(test_client, get_headers, purchase_on_db):
    purchase_order_id = purchase_on_db.id
    url = f'/purchase_orders/{purchase_order_id}/items'

    obj = {
        'description': 'Item teste',
        'quantity': 10
    }

    response = test_client.post(
        path=url,
        headers=get_headers,
        data=json.dumps(obj),
        content_type=APPLICATION_JSON,
    )

    assert response.status_code == 400
    assert response.json['message']['price'] == 'Inform a valid price'


def test_post_purchase_order_invalid(test_client, get_headers):
    _id = 99999
    message = f'Order id {_id} not found'
    url = f'/purchase_orders/{_id}/items'

    obj = {
        'description': 'Item teste',
        'price': 10.0,
        'quantity': 5
    }

    response = test_client.post(
        path=url,
        headers=get_headers,
        data=json.dumps(obj),
        content_type=APPLICATION_JSON,
    )

    assert response.json['message'] == message


def test_delete_order_item(test_client, get_headers, purchase_items_on_db):
    first_item = 0
    item_order_id = purchase_items_on_db['items'][first_item]['id']
    purchase_order_id = purchase_items_on_db['purchase_order']['id']

    url = f'/purchase_orders/{purchase_order_id}/items/{item_order_id}'

    response = test_client.delete(path=url, headers=get_headers)

    check_item_on_db_after_deleted = test_client.delete(path=url, headers=get_headers)

    assert response.status_code == 200  # Item Deleted
    assert check_item_on_db_after_deleted.json['message'] == f'Item id {item_order_id} not found'
