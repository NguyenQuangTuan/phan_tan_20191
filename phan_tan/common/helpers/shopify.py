import os
import hmac
import hashlib
import requests
import shopify
import json


def get_shop_info(domain, access_token):
    url = f'https://{domain}/admin/shop.json'
    headers = {
        'Authorization' if 'Basic' in access_token
        else 'X-Shopify-Access-Token': access_token
    }

    response = requests.get(url, headers=headers)
    return {
        'status': response.status_code,
        'body': response.json()
    }


def shopify_permission_url(domain, redirect_uri='', scopes=[]):
    api_key = os.getenv('SHOPIFY_API_KEY')
    secret_key = os.getenv('SHOPIFY_SECRET_KEY')
    scopes = scopes
    redirect_uri = redirect_uri or os.getenv('SHOPIFY_REDIRECT_URI')

    shopify.Session.setup(api_key=api_key, secret=secret_key)
    shopify_session = shopify.Session(domain)
    permission_url = shopify_session.create_permission_url(
        scopes, redirect_uri)

    return permission_url


def verify_hmac(code, shop, timestamp, hmac_code, locale='en'):
    msg = f'locale={locale}&shop={shop}&timestamp={timestamp}'
    if code:
        msg = f'code={code}&{msg}'

    my_hmac = hmac.new(
        key=os.getenv('SHOPIFY_SECRET_KEY').encode(),
        msg=msg.encode(),
        digestmod=hashlib.sha256
    )

    return hmac.compare_digest(my_hmac.hexdigest(), hmac_code)


def get_scopes():
    scopes = os.getenv('SHOPIFY_SCOPES')
    return scopes


def get_shopify_collection(current_shop):
    domain = current_shop.get('domain')
    shop_info = json.loads(current_shop.get('shop_info_json'))
    shop_key = shop_info.get('shopKey')
    shop_url = f'https://{ domain }'
    collections = os.getenv('SHOPIFY_API_URL_COLLECTIONS')
    type_and_tags = os.getenv('SHOPIFY_API_URL_TYPE_AND_TAGS')
    collections_url = f'{ shop_url }{ collections }'
    type_and_tags_url = f'{ shop_url }{ type_and_tags }'

    header_shop = {
        'X-Shopify-Access-Token': shop_key
    }

    collection_response = requests.get(collections_url, headers=header_shop)
    collections = collection_response.json().get('custom_collections')

    type_and_tags_response = requests.get(type_and_tags_url,
                                          headers=header_shop)
    types_and_tags = type_and_tags_response.json().get('products')

    list_types = []
    list_tags = []
    shopify_types = []
    shopify_tags = []

    for type_and_tag in types_and_tags:
        type = type_and_tag.get('product_type')
        tags = type_and_tag.get('tags').split(',')
        if type and type not in list_types:
            list_types.append(type)
            shopify_types.append({'value': type})

        for tag in tags:
            if tag and tag not in list_tags:
                list_tags.append(tag)
                shopify_tags.append({'value': tag})

    return collections, shopify_types, shopify_tags


def __create_request(path, method='GET'):
    request_info = {}
    request_info['headers'] = {
        'User-Agent': '{} {} {}'.format(
            'Mozilla/5.0 (Windows NT 5.1; rv:10.0.1)',
            'Gecko/20100101',
            'Firefox/10.0.1'
        ),
        'Content-Type': 'application/json'
    }
    request_info['url'] = path
    request_info['verb'] = method
    return request_info


def __open_request(data=None, request_info=None):
    result = {}
    response = requests.request(
        request_info['verb'],
        request_info['url'],
        headers=request_info['headers'],
        json=data
    )

    if response.status_code == 200:
        result = {
            'error': True,
            'status': response.status_code,
            'data': response.json(),
            'header': response.headers
        }
    else:
        result = {
            'error': False,
            'status': response.status_code,
            'header': response.headers,
            'message': response.reason,
            'request': request_info,
            'data': data
        }

    return result


def get_shop_token(domain, authorization_code):
    request_info = __create_request(
        f'https://{domain}.myshopify.com/admin/oauth/access_token',
        'POST'
    )

    data = {
        'client_id': os.getenv('SHOPIFY_API_KEY'),
        'client_secret': os.getenv('SHOPIFY_SECRET_KEY'),
        'code': authorization_code
    }

    response = __open_request(data, request_info=request_info)
    if response.get('error'):
        return response.get('data').get('access_token')
    else:
        return None


def create_webhook(domain, topic, address, access_token):
    request_info = __create_request(
        f'https://{domain}.myshopify.com/admin/webhooks.json', 'POST')
    request_info['headers']['X-Shopify-Access-Token'] = access_token
    data = {
        'webhook': {
            'topic': topic,
            'address': address,
            'format': 'json'
        }
    }
    result = __open_request(data, request_info)
    return result


def get_list_transactions(shop_domain, order_id, access_token):
    request_info = __create_request(
        f'https://{shop_domain}/admin/orders/{order_id}/transactions.json',
        'GET'
    )
    request_info['headers']['X-Shopify-Access-Token'] = access_token
    return __open_request(request_info=request_info)


def get_list_webhook(domain, access_token):
    request_info = __create_request(
        f'https://{domain}.myshopify.com/admin/webhooks.json', 'GET')
    request_info['headers']['X-Shopify-Access-Token'] = access_token
    return __open_request(request_info=request_info)


def delete_webhook(domain, access_token, webhook_id):
    request_info = __create_request(
        f'https://{domain}.myshopify.com/admin/webhooks/{webhook_id}.json',
        'DELETE'
    )
    request_info['headers']['X-Shopify-Access-Token'] = access_token
    return __open_request(request_info=request_info)
