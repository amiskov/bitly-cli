import os
from urllib.parse import urlparse

import dotenv
import requests

dotenv.load_dotenv()

BITLY_TOKEN = os.getenv('BITLY_TOKEN')
if not BITLY_TOKEN:
    print('Please, add your Bitly API token to `.env` file.',
          'See `.env.example`.')
    exit(1)


def shorten_link(token: str, long_url: str) -> str:
    """
    Returns a bitlink (short URL in form of `bit.ly/blah123`) for the `long_url`.
    """
    bitly_url = 'https://api-ssl.bitly.com/v4/shorten'
    headers = {
        "Authorization": f'Bearer {token}',
    }
    payload = {
        "long_url": long_url,
    }
    response = requests.post(bitly_url, headers=headers, json=payload)
    response.raise_for_status()
    bitlink_info = response.json()
    short_url = bitlink_info['link']
    return short_url


def strip_bitlink_scheme(bitlink: str) -> str:
    """
    Removes `http://` or `https://` from the start of the given `bitlink`.

    >>> strip_bitlink_scheme('https://bit.ly/3Qt2cAW')
    'bit.ly/3Qt2cAW'
    """
    parsed_link = urlparse(bitlink)
    return f'{parsed_link.netloc}{parsed_link.path}'


def is_bitlink(token: str, url: str) -> bool:
    """
    Returns `True` if the given `url` is valid bitlink for the given `token`.

    >>> is_bitlink(BITLY_TOKEN, 'bit.ly/3Qt2cAW')
    True
    >>> is_bitlink(BITLY_TOKEN, 'https://bit.ly/3Qt2cAW')
    True
    >>> is_bitlink(BITLY_TOKEN, 'https://hard.ly/3Qt2cAW')
    False
    """
    url_no_scheme = strip_bitlink_scheme(url)
    req_url = f'https://api-ssl.bitly.com/v4/bitlinks/{url_no_scheme}'
    headers = {
        "Authorization": f'Bearer {token}'
    }
    resp = requests.get(req_url, headers=headers)
    return resp.ok


def count_clicks(token: str, bitlink: str) -> int:
    """
    `bitlink` must be valid for the given `token`.
    """
    bitlink_no_scheme = strip_bitlink_scheme(bitlink)
    req_url = (f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink_no_scheme}/'
               'clicks/summary')
    headers = {
        "Authorization": f'Bearer {token}'
    }
    params = (
        ('units', '-1'),
    )
    resp = requests.get(req_url, headers=headers, params=params)
    resp.raise_for_status()
    clicks_info = resp.json()
    return clicks_info['total_clicks']


if __name__ == '__main__':
    user_url = input('Enter a URL: ')
    try:
        if is_bitlink(BITLY_TOKEN, user_url):
            print(count_clicks(BITLY_TOKEN, user_url))
        else:
            print(f'Битлинк: {shorten_link(BITLY_TOKEN, user_url)}')
    except requests.exceptions.HTTPError as e:
        print(e)
