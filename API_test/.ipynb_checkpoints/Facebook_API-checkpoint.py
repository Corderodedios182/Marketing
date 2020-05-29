#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 12:42:22 2019

@author: carlos
"""

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

#Claves de acceso
my_app_id = '276686046355294'
my_app_secret = '888a472886359feee3c0c0e45b414c00'
my_access_token = 'EAAD7pP2B314BAMKHIBTjpPQqXKYOZArD5v7ZBvGbuZAgNNE1YKsqj3iYZAYm2LowacK8NkHOh2eEZCXhhafRvBXk20Um4ZBMn26DVXA5hDoBhQSXn6xJjWhnA9jm85q7sih7sT7WokUI2fLzUm4Xa6n5hpipZASZAF1BwEp8BXCY6PJzdnWoK6ZB1DkT6fBqzyZBmZBvyzINaFgowZDZD'

#Iniciar API
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)

#Llamadas
my_account = AdAccount('act_754103418273978')
campaigns = my_account.get_campaigns()

print(campaigns)

import requests

a = requests.get("https://graph.facebook.com/276686046355294/720786428006108/adnetworkanalytics/?metrics=['fb_ad_network_imp']&access_token=EAAD7pP2B314BAMKHIBTjpPQqXKYOZArD5v7ZBvGbuZAgNNE1YKsqj3iYZAYm2LowacK8NkHOh2eEZCXhhafRvBXk20Um4ZBMn26DVXA5hDoBhQSXn6xJjWhnA9jm85q7sih7sT7WokUI2fLzUm4Xa6n5hpipZASZAF1BwEp8BXCY6PJzdnWoK6ZB1DkT6fBqzyZBmZBvyzINaFgowZDZD")
a 
base = a.content

type(base)

#Llamadas Interesess

####
from facebookads.api import FacebookAdsApi
from facebookads.adobjects.targetingsearch import TargetingSearch

FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)

params = {
    'q': 'veganos',
    'type': 'adinterest',
    'limit' : 80,
}

resp = TargetingSearch.search(params=params)
print(resp)

import pandas as pd

Intereses = pd.DataFrame(resp)
Intereses.columns
Intereses = Intereses.sort_values(by = 'audience_size', ascending =  False)


####
results = TargetingSearch.search(params={
    'q': 'United States',
    'type': TargetingSearch.TargetingSearchTypes.country,
    'limit': 2,
})


#Llamadas Fan Page con Graph

import requests
t = "EAAD7pP2B314BAIimmmwZAKODzLiUKJZCpYSTkSyWxhZCMp5ZAyDa7orpFS1txP3Sm1m2ZC6rrbEjWLs7wuJ845mmJFn1Qr91mjuPQDvyhamJhpAtLOQVNGSTNXSxIqyE5Gi3bA1sQABRxo844ntNdxDZABZAanfOLZA74fVefLLqh9LLVySZAKnZBBWeKeZBU6YLAl3gbSqQMguLuexWbGoSwJ8gGkC9W5sGkpLMsEiWXJLkt3u2JNkZASoG"

a = requests.get(str("https://graph.facebook.com/v4.0/104806722889108/insights/page_actions_post_reactions_like_total?access_token=") + str(t))
a 
base = a.content

type(base)














































