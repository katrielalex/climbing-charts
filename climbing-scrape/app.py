# -*- coding: utf-8 -*-
import collections
import json
import logging
import operator
import re
import time

import aws_xray_sdk.core
import boto3
import boto3.dynamodb.types
import bs4
import requests
import yaml

ROCKGYMPRO = 'https://portal.rockgympro.com/portal/public/a67951f8b19504c3fd14ef92ef27454d/occupancy'
TABLE = 'climbing-capacity-info'


logger = logging.getLogger()
logger.setLevel(logging.INFO)
aws_xray_sdk.core.patch_all()


def scrape_walls(_event, _context):
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

    boto3.resource('dynamodb').Table(TABLE).put_item(
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


def load_from_dynamo(_event, _context):
    aws_xray_sdk.core.xray_recorder.begin_subsegment('dynamodb-data-fetch')
    data = boto3.resource('dynamodb').Table(TABLE).scan()
    aws_xray_sdk.core.xray_recorder.end_subsegment()

    aws_xray_sdk.core.xray_recorder.begin_subsegment('munge')
    series = collections.defaultdict(dict)
    for datum in sorted(data['Items'], key=operator.itemgetter('timestamp')):
        ts = int(datum['timestamp'])
        for wall, values in datum['data']['M'].items():
            series[f"('{wall}', 'count')"][ts] = int(values['count'])
            series[f"('{wall}', 'capacity')"][ts] = int(values['capacity'])
    aws_xray_sdk.core.xray_recorder.end_subsegment()

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
        },
        'body': json.dumps(series),
    }
