'''
Created on Apr 12, 2013

@author: helenho
'''

from bs4 import BeautifulSoup
import urllib2
import re
from collections import namedtuple
city = namedtuple("city", "index ch en")
station = namedtuple("station", "stationindex ch en")




trcity = "^TRCity.push"
trstation = '^TRStation.push'
cityList = []
firstTime = True

def findCityIncityList(index):
    for city in cityList:
        if index ==city.index:
            return city


pattern = re.compile(trcity)
pattern2 = re.compile(trstation)
url = urllib2.urlopen('http://twtraffic.tra.gov.tw/twrail/')
frames = url.read()
soup = BeautifulSoup(frames)
lists = soup.findAll('script')
for item in lists:
    content = item.text
    result = pattern.search(content)
    if result:
        print "prcocessing City List***********"
        citiesString = re.split(';',content)
        index = 0
        while index <= len(citiesString)-3:
            if citiesString[index] and citiesString[index+1] and citiesString[index+2]:
                city_raw = re.split('\'', citiesString[index])
                if city_raw[1].isdigit():
                    aindex = int(city_raw[1])
                    print aindex
                    city_raw = re.split('\'', citiesString[index+1])
                    city_ch = city_raw[1];
                    print city_ch
                    city_raw = re.split('\'', citiesString[index+2])
                    city_en = city_raw[1];
                    print city_en
                    newcity = city(aindex, city_ch, city_en)
                    cityList.append(newcity)
            index +=3
    result = pattern2.search(content)
    if result:
        print "processing Station List**********"
        plist = open('station.plist','w')
        plist.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        plist.write("<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">\n")
        plist.write("<plist version=\"1.0\">\n")
        plist.write("<dict>\n")
        if result:
            stationsString = re.split(';',content)
            index = 0
            cityNumber = 0
            prevcityNumber = 0
            while index <= len(stationsString)-4:
#                print "index = "+ str(index)
                if stationsString[index] and stationsString[index+1] and stationsString[index+2] and stationsString[index+3]:
#                    print "index = "+str(index)+"tuples exist"
                    station_raw = re.split('\'', stationsString[index])
                    if station_raw[1].isdigit():
                        print station_raw[1]
                        cityNumber = int(station_raw[1])
                        currentCity = findCityIncityList(cityNumber)
                        if cityNumber==0 and prevcityNumber==0 and firstTime==True:
                            prevcityNumber = cityNumber
                            firstTime=False;
                            line = "<key>"+currentCity.ch+"</key>\n"+"<array>\n"
                            print line
                            plist.write(line)
                        if prevcityNumber == cityNumber:
#                            station_raw = re.split('\'', stationsString[index+1])
#                            station_index = int(station_raw[1]);                            
                            station_raw = re.split('\'', stationsString[index+2])
#                            station_ch = station_raw[1];
#                            station_raw = re.split('\'', stationsString[index+3])
#                           station_en = station_raw[1];
                            line = "<string>"+station_raw[1]+"</string>\n"
                            line.decode('utf8')
                            print line
                            plist.write(line)
                            index +=4;
                        else:
                            plist.write("</array>\n")
                            prevcityNumber = cityNumber;
                            currentCity = findCityIncityList(cityNumber)
                            line = "<key>"+currentCity.ch+"</key>\n<array>\n"
                            line.decode('utf8')
                            print line
                            plist.write(line)
        plist.write("</dict>\n")
        plist.write("</plist>\n")
        plist.close()
        print "file closed"
            
'''      
for city in cityList:
    print city.index
    print city.en
    print city.ch
'''


                 
'''
response = mechanize.urlopen('http://twtraffic.tra.gov.tw/twrail/');
forms = mechanize.ParseResponse(response)
for form in forms:
    control = form.find_control("FromCity", type="select")
    control
    print control.name, control.value, control.type

'''
'''
browser.open('http://twtraffic.tra.gov.tw/twrail/quicksearch.aspx');
pg = urllib2.urlopen('http://twtraffic.tra.gov.tw/twrail/quicksearch.aspx')
soup = BeautifulSoup(pg)

select_node = soup.findAll('select', attrs={'name': 'FromCity'})

if select_node:
    for option in select_node[0].findAll('option'):
        print option
'''



