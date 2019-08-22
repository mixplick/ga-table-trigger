# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

import pandas
import pandas_gbq

def date_sub(date_time: datetime, interval: int):
    return str((date_time + timedelta(interval * -1)).strftime('%Y-%m-%d'))


def handler(event, context):
    START_DATE = date_sub(datetime.now(), 1)
    END_DATE = date_sub(datetime.now(),  1)
    PROJECT_ID = '<PROJECT ID>'
    DIALECT = 'standard'
    DESTINATION_TABLE = '<TABELA DE DESTINO>'
    QUERY_CONFIG = {
        'query': {
            'parameterMode': 'NAMED',
            'queryParameters': [
                {
                    'name': 'start_date',
                    'parameterType': {'type': 'STRING'},
                    'parameterValue': {'value': START_DATE}
                },
                {
                    'name': 'end_date',
                    'parameterType': {'type': 'STRING'},
                    'parameterValue': {'value': END_DATE}
                }
            ]
        }
    }
    QUERY = """
    
    """
    result = pandas.read_gbq(QUERY, PROJECT_ID,  dialect=DIALECT,  configuration=QUERY_CONFIG)
    result['date'] = result['date'].astype('str')
    result['last_update'] = result['last_update'].astype('str')

''' Alterar abaixo para o esquema da tabela que vai receber os dados, sempre seguindo o padrão:
    {'name': '<nome da columa>', 'type': '<tipo do dado>' },
    {'name': '<nome da columa 2>', 'type': '<tipo do dado 2>' }
'''
pandas_gbq.to_gbq(result, DESTINATION_TABLE, PROJECT_ID, if_exists='append', table_schema=[
        {'name': 'date', 'type': 'DATE'}
     ])
