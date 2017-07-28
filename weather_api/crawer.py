import urllib2
import json
import mysql.connector
from datetime import datetime
from datetime import timedelta

conn = mysql.connector.connect(user='root', password='root', database='currency', use_unicode=True)
cursor = conn.cursor()

# return json dict from api url
# exsample url: http://api.fixer.io/2001-01-01?base=USD
def getJson(url):
  request = urllib2.Request(url)
  opener = urllib2.build_opener()
  try:
    response = opener.open(request)
    content = response.read()
    return json.loads(content)

  except urllib2.URLError, e:
    print 'getJson Exception: ' + str(e)

def saveCurrency(json_data):
  try:
    date = json_data['date']
    rates = json_data['rates']
    for key in rates:
      country = getCodeFromCountryName(key)
      rate = str(rates[key])
      if not country == 0:
        cursor.execute('''insert into rates(rate_id, date, currency_code, rate, base)
          VALUES (%s, %s, %s, %s, %s)''', [None, date, country, rate, None])
      conn.commit()
  except Exception, e:
    print 'saveCurrency Exception: ' + str(e)

def getCodeFromCountryName(country_name):
  country_dict = {
    'AUD': 1,
    'CAD': 2,
    'CHF': 3,
    'CYP': 4,
    'CZK': 5,
    'DKK': 6,
    'EEK': 7,
    'GBP': 8,
    'HKD': 9,
    'HUF': 10,
    'ISK': 11,
    'JPY': 12,
    'KRW': 13,
    'LTL': 14,
    'LVL': 15,
    'MTL': 16,
    'NOK': 17,
    'NZD': 18,
    'PLN': 19,
    'ROL': 20,
    'SEK': 21,
    'SGD': 22,
    'SIT': 23,
    'SKK': 24,
    'TRL': 25,
    'USD': 26,
    'ZAR': 27,
    'EUR': 28
  }
  try:
    return country_dict[country_name]
  except Exception, e:
    print 'getCodeFromCountryName Exception: ' + str(e)
    return 0

base_day = datetime(2000, 2, 1, 0, 0)
for i in range(1, 10):
  current_day = base_day + timedelta(days=i)
  param_date = current_day.strftime("%Y-%m-%d")
  print param_date
  url = 'http://api.fixer.io/' + param_date + '?base=USD'
  json_data =  getJson(url)
  saveCurrency(json_data)

cursor.close()
conn.close()


'''
def getCountryFromCode(country_code):
  country_dict = {
    1: 'AUD',
    2: 'CAD',
    3: 'CHF',
    4: 'CYP',
    5: 'CZK',
    6: 'DKK',
    7: 'EEK',
    8: 'GBP',
    9: 'HKD',
    10: 'HUF',
    11: 'ISK',
    12: 'JPY',
    13: 'KRW',
    14: 'LTL',
    15: 'LVL',
    16: 'MTL',
    17: 'NOK',
    18: 'NZD',
    19: 'PLN',
    20: 'ROL',
    21: 'SEK',
    22: 'SGD',
    23: 'SIT',
    24: 'SKK',
    25: 'TRL',
    26: 'USD',
    27: 'ZAR',
    28: 'EUR'
  }
  try:
    return country_dict[country_code]
  except Exception, e:
    return ''
'''
