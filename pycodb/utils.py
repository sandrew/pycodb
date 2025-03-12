'''This module includes tools for NocoDB interactions'''
import logging
import requests
from . import noco_settings

logger = logging.getLogger(__name__)

class NocoDBRequestError(Exception):
    """
    class for RequestError from Noco, have status_code and message
    """
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(f"NocoDB request has failed {status_code}: {message}")


def create_link(table_from, link_id, id_from, id_to):
    '''Performs a request to NocoDB to link two records'''
    url = f'{noco_settings.NOCO_URL}/tables/{table_from}/links/{link_id}/records/{id_from}'
    return perform_request('post', url, { 'Id': id_to })


def find(table, view, data):
    '''Finds a record in NocoDB'''
    result = records_request('get', table, view, params = f'where={where_params(data)}&limit=1')['list']
    if len(result) > 0:
        return result[0]
    return None


def find_or_create(table, view, criteria):
    '''Find or create a record in NocoDB by specified criteria'''
    return find(table, view, criteria) or (criteria | records_request('post', table, view, data = criteria))


def where_condition(key, value, operand='eq'):
    '''Creates a condition for NocoDB'''
    if isinstance(value, list):
        value = ','.join([str(v) for v in value])
    elif value is None:
        value = 'null'
        if operand == 'eq':
            operand = 'is'
        elif operand == 'neq':
            operand = 'isnot'
    return f'({key},{operand},{value})'


def where_params(params):
    '''Creates a where clause for NocoDB'''
    conditions = []
    for key, value in params.items():
        # { 'key': { 'operand': 'value' } } -> (key,operand,value)
        if isinstance(value, dict):
            for operand, final_value in value.items():
                conditions.append(where_condition(key, final_value, operand))
        # { 'key': 'value' } -> (key,eq,value)
        else:
            conditions.append(where_condition(key, value))

    return '~and'.join(conditions)

def records_request(method, table, view, params = None, data = None):
    '''Performs a request to NocoDB records endpoint'''
    url = f'{noco_settings.NOCO_URL}/tables/{table}/records?viewId={view}'
    if params is not None:
        url = f'{url}&{params}'
    return perform_request(method, url, data)


def perform_request(method, url, data):
    '''Performs a NocoDB request'''
    result = requests.request(method  = method,
                              url     = url,
                              json    = data,
                              headers = { 'xc-token' : noco_settings.NOCO_TOKEN },
                              timeout = 5)

    return process_request_result(result, method, url)


def upload_file(file, title, path):
    url = f'{noco_settings.NOCO_URL}/storage/upload'
    result = requests.post(url     = url,
                           files   = { 'file' : (title, file) },
                           headers = { 'xc-token' : noco_settings.NOCO_TOKEN },
                           params  = { 'path' : path },
                           timeout = 10)

    return process_request_result(result, 'POST', url)


def process_request_result(result, method, url):
    if result.status_code < 200 or result.status_code > 299:
        logger.error('NocoDB %s request to %s has failed: %s', method.upper(), url, result.text)
        raise NocoDBRequestError(status_code = result.status_code,
                                 message     = result.text)

    return result.json()
