import requests
import xmltodict

try:
    with open('AppID') as f:
        id = f.read()
except:    
    with open('server/data/AppID') as f:
        id = f.read()

def getAnswer(question: str, format: list = ['plaintext'], location: str = None):
    url =  'http://api.wolframalpha.com/v2/query'
    params = {
    'input': question,
    'appid': id,
    'format': ','.join(format),
    'includepodid': 'Result',
    'location': location,
}

    r = requests.get(url, params)
    t = xmltodict.parse(r.text)['queryresult']
    return t['pod']['subpod']['plaintext']