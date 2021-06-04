# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 20:01:32 2021

@author: crf005r
"""
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
from google.cloud import bigquery

key_path = "C:/Users/crf005r/Desktop/bancoazteca-master-hub-5d75f1053d53.json"

#variables
gcp_project = 'bancoazteca-master-hub'
bq_dataset = 'appsflyer_data.appsflyer_events_data'

#connections
credentials = service_account.Credentials.from_service_account_file(key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],)

client = bigquery.Client(credentials=credentials, project=credentials.project_id)

dataset_ref = client.dataset(bq_dataset)

#result to dataframe function
def gcp2df(sql):
    query = client.query(sql)
    results = query.result()
    return results.to_dataframe()

sql = """SELECT * FROM `appsflyer_data.appsflyer_events_data` limit 10"""

df = gcp2df(sql)

