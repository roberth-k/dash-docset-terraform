#!/usr/bin/env python3
from typing import Tuple

import requests

REGISTRY_URL = 'https://registry.terraform.io'
EXCLUDED_PROVIDERS = [
    'hashicorp/google-beta',
    'hashicorp/kubernetes-alpha',
]


def main():
    page_number = '1'
    results = []

    while page_number:
        response = requests.get(
            url=REGISTRY_URL+'/v2/providers',
            params={
                'filter[namespace]': 'hashicorp',
                'filter[moved]': 'false',
                'filter[unlisted]': 'false',
                'filter[without-versions]': 'false',
                'page[size]': '50',
                'page[number]': page_number,
            })

        response.raise_for_status()

        data = response.json()
        results.extend(data['data'])
        page_number = data['meta']['pagination']['next-page']

    for datum in data['data']:
        source = datum['attributes']['source']
        full_name = datum['attributes']['full-name']
        link = datum['links']['self']

        if full_name in EXCLUDED_PROVIDERS:
            continue

        latest_version, latest_version_tag = get_latest_version_tag(link)
        print(f'{full_name} {source} {latest_version_tag}')


def get_latest_version_tag(link: str) -> Tuple[str, str]:
    response = requests.get(
        url=REGISTRY_URL+'/'+link,
        params={
            'include': 'provider-versions',
        })
    response.raise_for_status()
    data = response.json()

    latest_version_id = data['data']['relationships']['provider-versions']['data'][-1]['id']

    response = requests.get(url='https://registry.terraform.io/v2/provider-versions/'+latest_version_id)
    response.raise_for_status()
    data = response.json()

    latest_version = data['data']['attributes']['version']
    latest_version_tag = data['data']['attributes']['tag']

    return latest_version, latest_version_tag


if __name__ == '__main__':
    main()
