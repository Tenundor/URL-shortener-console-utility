import argparse
import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(token, url):
    bitly_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    long_url = {'long_url': url}
    api_key = {
        'Authorization': 'Bearer {}'.format(token)
    }
    response = requests.post(bitly_url, headers=api_key, json=long_url)
    response.raise_for_status()
    return response.json()["link"]


def count_clicks(token, link):
    parsed_url = urlparse(link)
    bitlink = parsed_url.netloc + parsed_url.path
    api_key = {
        'Authorization': 'Bearer {}'.format(token)
    }
    bitly_host = 'https://api-ssl.bitly.com'
    bitly_url = '{host}/v4/bitlinks/{bitlink}/clicks/summary'.format(
        host=bitly_host, bitlink=bitlink
    )
    response = requests.get(bitly_url, headers=api_key)
    response.raise_for_status()
    return response.json()["total_clicks"]


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("BITLY_TOKEN")
    parser = argparse.ArgumentParser(
      description='Утилита сокращает ссылки и считает суммарное количество кликов по ним'
    )
    parser.add_argument('url', help='Адрес ссылки для сокращения или битлинк')
    user_url = parser.parse_args().url
    try:
        print('Количество кликов:', count_clicks(token, user_url))
    except requests.exceptions.HTTPError:
        try:
            print('Битлинк', shorten_link(token, user_url))
        except requests.exceptions.HTTPError:
            print('Некорректная ссылка.')
