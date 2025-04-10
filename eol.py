import urllib
import urllib.request
import json
from datetime import date,datetime
import pandas as pd

def eol():
    today = date.today()    # Get the current date
    result_eol = []
    url = "https://endoflife.date/api/all.json"
    response = urllib.request.urlopen(url)
    data = json.load(response)

    for item in data:
        #print('calling api....')
        url1 = "https://endoflife.date/api/"+item+".json"
        response1 = urllib.request.urlopen(url1)
        data1 = json.load(response1)

        for item1 in range(len(data1)):
            try:
                d_eol = datetime.strptime(data1[item1]['eol'], '%Y-%m-%d').date()
                if d_eol > today:  # Only include items with datetime_str > today
                    v_cycle = data1[item1]['cycle']
                    v_lts = data1[item1]['lts']
                    d_release = datetime.strptime(data1[item1]['releaseDate'], '%Y-%m-%d').date()
                    v_latest = data1[item1]['latest']
                    result_eol.append((item, d_eol, v_cycle, v_lts, d_release, v_latest))            
            except (TypeError, KeyError, ValueError):
                pass    # Skip items with missing or invalid date

    # Create a DataFrame and save to CSV
    df = pd.DataFrame(result_eol,columns=['Product','EOL date','Version','Has LTS','Release date','Latest Version'])
    df.to_csv('eol.csv')
                    #df.to_json('eol.json')
    return(result_eol)

if __name__ == '__main__':
    r_eol = []
    r_eol = eol()
