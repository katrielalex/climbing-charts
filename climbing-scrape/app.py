# -*- coding: utf-8 -*-
import json
import re
import time

import boto3
import bs4
import requests
import yaml

ROCKGYMPRO = 'https://portal.rockgympro.com/portal/public/a67951f8b19504c3fd14ef92ef27454d/occupancy'


def lambda_handler(_event, _context):
    source = bs4.BeautifulSoup(
        requests.get(
            ROCKGYMPRO,
        ).text,
        features='html.parser',
    ).findAll('script')[2].string

    # Use YAML not JSON because it uses single-quote keys which are invalid JSON
    data = yaml.safe_load(re.search(
        'var data = (.*?);',
        source, re.DOTALL,
    ).group(1))

    boto3.resource('dynamodb').Table('climbing-capacity-info').put_item(
        TableName='climbing-capacity-info',
        Item={
            'timestamp': int(time.time()),
            'data': {'M': data},
        },
    )

    return {
        'statusCode': 200,
        'body': json.dumps({int(time.time()): data}),
    }
