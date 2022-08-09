from urllib.request import urlopen
import urllib.error
import twurl
import json
import ssl
import pandas as pd

TWITTER_URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

df = pd.DataFrame(columns = ['id', 'nombre', 'texto','mencion', 'fecha'])


while True:
    acct = input('Enter a Twitter account, or quit: ')
    if (acct == 'quit'): break

    url = twurl.augment(TWITTER_URL, {'screen_name': acct, 'count': '100'})
    print('Retrieving', url)
    connection = urlopen(url, context=ctx)
    data = connection.read().decode()
    headers = dict(connection.getheaders())

    print('Remaining', headers['x-rate-limit-remaining'])
    js = json.loads(data)


    # Debugging
    # print(json.dumps(js, indent=4))

    # Itera a través de la lista de diccionarios de JSON
    # y captura los datos que buscamos

    for u in js:
        info = ({
            'id' : [u['id']],
            'nombre' : [u["user"]["screen_name"]],
            'texto' : [u["text"]],
            'fecha' : [u["created_at"]]
        })
        try :
            mencion = u["entities"]["user_mentions"][0]["screen_name"],
            info['mencion'] = [mencion]
        except:
            info['mencion'] = ["Sin menciones"]
            # Debugging
            #print(info)
        info = pd.Series(info)
        df = df.append(info, ignore_index=True)


df.to_csv('tweets.csv', index=False)
