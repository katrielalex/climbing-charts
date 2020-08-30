# -*- coding: utf-8 -*-
import json
import re

import bs4
import requests
import yaml

ROCKGYMPRO = 'https://portal.rockgympro.com/portal/public/a67951f8b19504c3fd14ef92ef27454d/occupancy'


def lambda_handler(_event, _context):
    source = bs4.BeautifulSoup(
        requests.get(
            ROCKGYMPRO,
        ).text,
    ).findAll('script')[2].string

    # Use YAML not JSON because it uses single-quote keys which are invalid JSON
    data = yaml.load(re.search(
        'var data = (.*?);',
        source, re.DOTALL,
    ).group(1))

    print(data)

    return {
        'statusCode': 200,
        'body': json.dumps(data),
    }
