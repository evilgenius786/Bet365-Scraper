import json
import os.path
from datetime import datetime

import requests


def fetchSport(sport):
    params = (
        ('prematch', '1'),
        ('live', '0'),
        ('temporalFilter', 'TEMPORAL_FILTER_OGGI_DOMANI'),
    )
    print(f'Getting {sport}...')
    response = requests.get(f'https://www.eurobet.it/detail-service/sport-schedule/services/discipline/{sport}',
                            headers=getHeaders(), params=params)
    data = response.json()
    rows = []
    for dataGroup in data['result']['dataGroupList']:
        for item in dataGroup['itemList']:
            event = item['eventInfo']
            row = {
                "Date": datetime.fromtimestamp(event['eventData'] / 1000).strftime('%d/%m/%Y'),
                "Time": datetime.fromtimestamp(event['eventData'] / 1000).strftime('%H:%M'),
                "Championship": event['countryDescription'] + ' > ' + event['meetingDescription'],
                "Casa": event['teamHome']['description'],
                "Ospite": event['teamAway']['description'],
                "URL": f"https://www.eurobet.it/it/scommesse/#!/{item['breadCrumbInfo']['fullUrl']}"
            }
            rows.append(row)
    with open(f'./eurobet/{sport}.json', 'w') as f:
        json.dump(rows, f, indent=4)
    print(f'Got {sport} ({len(rows)} events)!')


def main():
    logo()
    if not os.path.isdir('./eurobet'):
        os.mkdir('./eurobet')

    sports = [
        'pallamano',
        'calcio',
        'tennis',
        'basket',
        'volley',
        'baseball',
        'tennis-tavolo',
        'hockey-ghiaccio',
        'rugby'
    ]
    for sport in sports:
        try:
            fetchSport(sport)
        except:
            print(f'Error getting {sport}!')


def getHeaders():
    return {
        'authority': 'www.eurobet.it',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': '__cflb=02DiuH88gCYcfmbdqvQhGqhnknhEjFBPospZxEccb4WFE; showSplash=false; OptanonAlertBoxClosed=2023-02-28T09:18:57.140Z; at_check=true; AMCVS_45F10C3A53DAEC9F0A490D4D%40AdobeOrg=1; __cf_bm=Pebk0cZLx4zEIeMD2vpzpzy4n2vUGweylpo1bXZjN5I-1677576314-0-AaKbN/o6OIK34AXuhLb4c2bCzR29zTfpZbCD7vAT65JXuYd/SgzKaTynNarZfKw47vmB954+XwCff02yBuD8ZuI=; AMCV_45F10C3A53DAEC9F0A490D4D%40AdobeOrg=-1124106680%7CMCIDTS%7C19417%7CMCMID%7C16783468318286138329204055167178225103%7CMCAID%7CNONE%7CMCOPTOUT-1677583941s%7CNONE%7CvVersion%7C5.2.0; OptanonConsent=isIABGlobal=false&datestamp=Tue+Feb+28+2023+14%3A32%3A22+GMT%2B0500+(Pakistan+Standard+Time)&version=6.31.0&consentId=1652708f-ac1d-4654-8759-990adeeb0c02&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0004%3A1%2CBG143%3A1%2CC0002%3A1%2CBG144%3A1%2CC0003%3A1&hosts=H644%3A1%2CH67%3A1%2CH600%3A1%2CH621%3A1%2CH622%3A1%2CH601%3A1%2CH624%3A1%2CH243%3A1%2CH625%3A1%2CH572%3A1%2CH627%3A1%2CH645%3A1%2CH330%3A1%2CH628%3A1%2CH9%3A1%2CH29%3A1%2CH43%3A1%2CH44%3A1%2CH61%3A1%2CH65%3A1%2CH66%3A1%2CH76%3A1%2CH464%3A1%2CH81%3A1%2CH100%3A1%2CH106%3A1%2CH114%3A1%2CH115%3A1%2CH134%3A1%2CH142%3A1%2CH158%3A1%2CH164%3A1%2CH422%3A1%2CH169%3A1%2CH171%3A1%2CH623%3A1%2CH181%3A1%2CH184%3A1%2CH189%3A1%2CH191%3A1%2CH208%3A1%2CH222%3A1%2CH225%3A1%2CH386%3A1%2CH238%3A1%2CH571%3A1%2CH263%3A1%2CH264%3A1%2CH268%3A1%2CH413%3A1%2CH279%3A1%2CH298%3A1%2CH300%3A1%2CH301%3A1%2CH302%3A1%2CH304%3A1%2CH573%3A1%2CH308%3A1%2CH312%3A1%2CH325%3A1%2CH331%3A1%2CH340%3A1%2CH351%3A1%2CH353%3A1%2CH355%3A1%2CH569%3A1%2CH297%3A1%2CH620%3A1%2CH570%3A1%2CH626%3A1%2CH629%3A1&genVendors=V1%3A0%2C&geolocation=IT%3B78&AwaitingReconsent=false; mbox=session#25ab08841df840e8a8cbe0357455602a#1677577798|PC#25ab08841df840e8a8cbe0357455602a.38_0#1740821543',
        'dnt': '1',
        'if-modified-since': 'Tue, 28 Feb 2023 09:32:09 GMT',
        'referer': 'https://www.eurobet.it/it/scommesse/',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'x-eb-accept-language': 'it_IT',
        'x-eb-marketid': '5',
        'x-eb-platformid': '1',
    }


def logo():
    print(r"""
___________                  __________        __   
\_   _____/__ _________  ____\______   \ _____/  |_ 
 |    __)_|  |  \_  __ \/  _ \|    |  _// __ \   __\
 |        \  |  /|  | \(  <_> )    |   \  ___/|  |  
/_______  /____/ |__|   \____/|______  /\___  >__|  
        \/                           \/     \/      
===================================================
        EuroBet scrapr by @evilgenius786
===================================================
[+] API based
[+] No need to login
[+] Browserless
[+] Fast
___________________________________________________
""")


if __name__ == '__main__':
    main()
