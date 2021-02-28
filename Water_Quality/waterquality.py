import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_text(state):
    site_url="https://nwis.waterdata.usgs.gov/" + state + "/nwis/current/?type=quality"
    try:
        request=urlopen(site_url)
        html=request.read()
    except:
        html = None
    return html
    
def save_to_file(html, state):
    bsObj=BeautifulSoup(html,'lxml')
    headers_html=bsObj.findAll('table')[1].findAll('thead')[0].findAll('tr')[0].findAll('th')   
    headers=[]
    for header in headers_html:
        headers.append(header.get_text().strip().replace('- ', ''))
    headers.append('county')
    with open('data_' + state + '.csv', mode='w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
    rows_html=bsObj.findAll('table')[1].findAll('tbody')[0].findAll('tr')
    county = ""
    for row_html in rows_html:
        if row_html.find('strong'):
            county = row_html.get_text().strip()
        else:
            td_html = row_html.findAll('td')
            row = []
            for td in td_html:
                row.append(td.get_text().strip())
            row.append(county)
            with open('data_' + state + '.csv', mode='a') as file:
                writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(row)


for state in ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
"HI", "ID", "IL", "IN", "IA", "KS", "LA", "ME", "MD",
"MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NM", "NC", "ND", "OH", "OK", "OR", "SC", "TN", "TX"]:
    html = get_text(state)
    if html:
        save_to_file(html, state)
    else:
        print(state,'State code is invalid')
