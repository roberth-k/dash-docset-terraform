#!/usr/bin/env python3
from typing import Tuple

import requests

REGISTRY_URL = 'https://registry.terraform.io'

EXCLUDED_PROVIDERS = [
    'hashicorp/google-beta',
    'hashicorp/kubernetes-alpha',
]

PROVIDER_FILTERS = [
    'hashicorp',
    'cloudflare/cloudflare',
    'digitalocean/digitalocean',
    'fastly/fastly',
    'gitlabhq/gitlab',
    'heroku/heroku',
    'integrations/github',
    'PagerDuty/pagerduty',
    'splunk/splunk',
    'splunk/victorops',
]


def main():
    for provider_filter in PROVIDER_FILTERS:
        if '/' in provider_filter:
            namespace, name = provider_filter.split('/')
        else:
            namespace = provider_filter
            name = ''

        page_number = '1'

        while page_number:
            params = {
                'filter[namespace]': namespace,
                'filter[moved]': 'false',
                'filter[unlisted]': 'false',
                'filter[without-versions]': 'false',
                'page[size]': '50',
                'page[number]': str(page_number),
            }

            response = requests.get(
                url=REGISTRY_URL+'/v2/providers',
                params=params)

            response.raise_for_status()

            data = response.json()
            page_number = data['meta']['pagination']['next-page']

        for datum in data['data']:
            source = datum['attributes']['source']
            full_name = datum['attributes']['full-name']
            link = datum['links']['self']

            if full_name in EXCLUDED_PROVIDERS:
                continue

            if name and full_name != provider_filter:
                continue

            latest_version, latest_version_tag = get_latest_version_tag(link)
            print(f'{full_name} {source} {latest_version_tag}')


def get_latest_version_tag(link: str) -> Tuple[str, str]:
    response = requests.get(
        url=REGISTRY_URL+'/'+link.lstrip('/'),
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
