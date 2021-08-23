import requests
import json
from itertools import islice
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

URL = "https://covid-api.mmediagroup.fr/v1/"

def avarage_confirmed_per_sqm():
    api = 'cases'
    request = requests.get(f'{URL}/{api}')
    input_dict = json.loads(request.text)
    avarage_per_country = {}
    result_array = {}
    result_array['Countries'] = []
    for country,v in input_dict.items():
        size = 0
        avg_cases = 0
        total_cases = input_dict[country]['All']['confirmed']
        total_deaths = input_dict[country]['All']['deaths']
        total_recovered = input_dict[country]['All']['recovered']
        active_cases = total_cases - total_recovered - total_deaths
        #for some reason some countries have no area at all
        if 'sq_km_area' in input_dict[country]['All']:
          size = input_dict[country]['All']['sq_km_area']/100
          # return the avarage cases per country
          avg_cases = active_cases/size
          #only first decimal point
          avg_cases = round(avg_cases,1)
          country_array = {}
          country_array['country'] = country
          country_array['avg_cases'] = avg_cases
        #return rge entire array
        result_array["Countries"].append(country_array)
    return result_array

def top_ten():
    api = 'history'
    parameters = {'status':'Confirmed'}
    request = requests.get(f'{URL}/{api}', params=parameters)
    result_array = {}
    result_array['Countries'] = []
    input_dict = json.loads(request.text)
    for country,v in input_dict.items():
        confirmed =  0
        dates = input_dict[country]['All']['dates']
        #select only the first 7 elements from the given dates
        last_week = dict(islice(dates.items(), 7))
        val = list(last_week.values())
        #confirmed cases in the last week
        confirmed = val[0] - val[6]
        
        country_array = {}
        country_array['country'] = country
        country_array['cases'] = confirmed 
        # #add country to our country dict
        result_array["Countries"].append(country_array)
        
    #sort by value and Return first 10 countries not including global cases#
    result_array["Countries"] = sorted(result_array['Countries'], key=lambda x: x['cases'], reverse=True)[1:11]
    return result_array

def greatest_cases_increment():
    api = 'history'
    parameters = {'status':'Confirmed'}
    request = requests.get(f'{URL}/{api}', params=parameters)
    result_array = {}
    result_array['Countries'] = []
    input_dict = json.loads(request.text)
    for country,v in input_dict.items():
        confirmed =  0
        dates = input_dict[country]['All']['dates']
        #last 10 days of confirmed cases in a country
        last_ten_days = dict(islice(dates.items(), 10))
        val = list(last_ten_days.values())
        #total confirmed cases in the last 10 days
        confirmed = val[0] - val[9]
        
        country_array = {}
        country_array['country'] = country
        country_array['confirmed'] = confirmed 
        result_array["Countries"].append(country_array)
        # #add country to our country dict
    #sort by value and Return first 5 countries not including global cases#
    result_array["Countries"] = sorted(result_array['Countries'], key=lambda x: x['confirmed'], reverse=True)[1:6]

    return result_array

def lambda_handler(event, context):
    if not event['queryStringParameters']:
         return {
        'statusCode': 401,
        'body': json.dumps('invoking this function without parameters is not allowed')
    }
    params = event['queryStringParameters']
    if not "action" in params:
        return {
        'statusCode': 401,
        'body': json.dumps('action key must be specified to use this function')
    }
    action = params['action']
    response = ["this action is not autorized, autorized actions are : avg_cases, most_infected, top_ten "]
    statusCode = 400
    if action == 'avg_cases':
        response = avarage_confirmed_per_sqm()
        statusCode = 200
    
    if action == 'top_ten':
        response = top_ten()
        statusCode = 200
        
    if action == 'most_infected':
        response = greatest_cases_increment()
        statusCode = 200
    #used only by grafana
    logger.info(response)
    return {
        'statusCode': statusCode,
        'body': json.dumps(response)
    }   
    
