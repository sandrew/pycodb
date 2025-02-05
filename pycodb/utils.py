'''This module includes tools for NocoDB interactions'''
import os

import requests
from pycodb.config import settings

AUTH_HEADER = {'xc-token': settings.NOCO_TOKEN}


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
    url = f'{settings.NOCO_URL}/tables/{table_from}/links/{link_id}/records/{id_from}'
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


def delete(table, view, data):
    '''Delete a record in NocoDB by id'''
    result = records_request('delete', table, view, data=data)
    return result

def where_params(params):
    '''Creates a where clause for NocoDB'''
    return '~and'.join([f'({key},eq,{value})' for key, value in params.items()])


def records_request(method, table, view, params = None, data = None):
    '''Performs a request to NocoDB records endpoint'''
    url = f'{settings.NOCO_URL}/tables/{table}/records?viewId={view}'
    if params is not None:
        url = f'{url}&{params}'
    return perform_request(method, url, data)


def perform_request(method, url, data):
    '''Performs a NocoDB request'''
    result = requests.request(method  = method,
                              url     = url,
                              json    = data,
                              headers = AUTH_HEADER,
                              timeout = 5)

    if result.status_code < 200 or result.status_code > 299:
        raise NocoDBRequestError(status_code= result.status_code,
                                 message=result.text)

    return result.json()
