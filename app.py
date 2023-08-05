import os
from urllib.parse import urlparse

import dotenv
import requests


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
    return response.json()['link']


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

    Examples:
    is_bitlink('your-bitly-token', 'bit.ly/3Qt2cAW') # True
    is_bitlink('your-bitly-token', 'https://es.pn/45gfogQ') # True (custom domain)
    is_bitlink('your-bitly-token', 'https://hard.ly/3Qt2cAW') # False
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
    return resp.json()['total_clicks']


def main(token: str) -> None:
    user_url = input('Enter a URL: ')
    try:
        if is_bitlink(token, user_url):
            print(count_clicks(token, user_url))
        else:
            print(f'Битлинк: {shorten_link(token, user_url)}')
    except requests.exceptions.HTTPError as e:
        print(e)


if __name__ == '__main__':
    dotenv.load_dotenv()
    main(os.environ['BITLY_TOKEN'])
