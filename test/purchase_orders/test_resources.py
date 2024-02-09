import json


PURCHASE_ORDERS_URL = '/purchase_orders'
APPLICATION_JSON = 'application/json'


def test_get_purchase_orders(test_client, get_headers, purchase_on_db):

    response = test_client.get(PURCHASE_ORDERS_URL, headers=get_headers)

    assert response.status_code == 200
    assert response.json[0]['id'] == purchase_on_db[0].id
    assert response.json[0]['description'] == purchase_on_db[0].description
    assert response.json[0]['quantity'] == purchase_on_db[0].quantity


def test_get_purchase_orders_by_id(test_client, get_headers, purchase_on_db):
    url = f'/purchase_orders/{(purchase_on_db[0].id)}'

    response = test_client.get(url, headers=get_headers)

    assert response.status_code == 200
    assert response.json['id'] == purchase_on_db[0].id
    assert response.json['description'] == purchase_on_db[0].description
    assert response.json['quantity'] == purchase_on_db[0].quantity


def test_post_purchase_order(test_client):
    obj = {'description': 'Purchase Order id 2', 'quantity': 150}

    response = test_client.post(
        path=PURCHASE_ORDERS_URL,
        data=json.dumps(obj),
        content_type=APPLICATION_JSON
    )

    assert response.status_code == 200
    assert response.status == '200 OK'


def test_purchase_orders_with_invalid_quantity(test_client):
    obj = {'description': 'Purchase Order id 2', 'quantity': 25}

    response = test_client.post(
        path=PURCHASE_ORDERS_URL,
        data=json.dumps(obj),
        content_type=APPLICATION_JSON
    )

    assert response.status_code == 400
    assert response.status == '400 BAD REQUEST'


def test_purchase_orders_with_invalid_description(test_client):
    obj = {'quantity': 125}

    response = test_client.post(
        path=PURCHASE_ORDERS_URL,
        data=json.dumps(obj),
        content_type=APPLICATION_JSON
    )

    assert response.status_code == 400
    assert response.status == '400 BAD REQUEST'
