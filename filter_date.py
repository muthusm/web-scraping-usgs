#!/usr/bin/env python
# coding: utf-8


import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_text(site_url):    
    try:
        request=urlopen(site_url)
        html=request.read()
    except:
        html = None
    #print(site_url)
    return html


def save_to_file(begin_date, end_date, station, desired_parameters):
    parameters = ''.join(['cb_' + ele + '=on&' for ele in desired_parameters])
    site_url="https://nwis.waterdata.usgs.gov/tn/nwis/uv?" + parameters + "format=html&site_no=" + station + "&period=&begin_date="+begin_date+"&end_date="+end_date
    html = get_text(site_url)
    bsObj=BeautifulSoup(html,'lxml')
    if len(bsObj.findAll('table')) < 3:
        if " *** There are no data available on the Waterdata system for the time period specified," in str(html):
            print(" *** There are no data available on the Waterdata system for the time period specified")
        #print(str(html))
    else:
        headers_html=bsObj.findAll('table')[2].findAll('thead')[0].findAll('tr')[0].findAll('th')  
        headers=[]
        for header in headers_html:
            headers.append(header.get_text().strip().replace('- ', ''))
        with open(station+'_'+begin_date+'_'+end_date+'.csv', mode='w') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(headers)
        rows_html=bsObj.findAll('table')[2].findAll('tbody')[0].findAll('tr')
        county = ""
        for row_html in rows_html:
            td_html = row_html.findAll('td')
            row = []
            for td in td_html:
                row.append(td.get_text().strip())
            with open(station+'_'+begin_date+'_'+end_date+'.csv', mode='a') as file:
                writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(row)       

def get_stations():
    site_url = "https://nwis.waterdata.usgs.gov/tn/nwis/current/?type=quality"
    html = get_text(site_url)
    bsObj=BeautifulSoup(html,'lxml')  
    rows_html=bsObj.findAll('table')[1].findAll('tbody')[0].findAll('tr')
    stations = []
    for row_html in rows_html:
        if not row_html.find('strong'):
            td_html = row_html.findAll('td')
            if td_html[0].get_text().strip() and td_html[1].get_text().strip():
                station = (td_html[0].get_text().strip(), td_html[1].get_text().strip())
                stations.append(station)
    return stations


stations = get_stations()
available_station_numbers = [station[0] for station in stations]
print('Station Number','|', 'Station Name')
print('--------------','|', '-------------')
for station in stations:
    print(station[0],'|', station[1])
choice = input("Enter the desired station numbers (comma separated) / Enter 'all' if you want report for all stations: ")
desired_stations = choice.split(',') if not choice == 'all' else available_station_numbers
parameters = [('00060', 'Discharge'),('00065', 'Gage height'),('63680', 'Turbidity')]
print('Parameter Number','|', 'Parameter Name')
print('----------------','|', '-------------')
for parameter in parameters:
    print(parameter[0],'|',parameter[1])
choice = input("Enter the desired parameter / Enter 'all' if you want report for all parameters: ")
desired_parameters = choice.split(',') if not choice == 'all' else [parameter[0] for parameter in parameters]
#print(desired_parameters)
begin_date = input("Enter the begin date(yyyy-mm-dd): ")
end_date = input("Enter the end date(yyyy-mm-dd): ")
for station in desired_stations:
    if station in available_station_numbers:
        save_to_file(begin_date, end_date, station.strip(), desired_parameters)





