import datetime
import re
from covidrequests import *


def countryallstatus():
    today = datetime.datetime.now()

    yesterday = today.day - 1
    daybefore = today.day - 2

    datey = datetime.datetime(today.year, today.month, yesterday)
    dateb = datetime.datetime(today.year, today.month, daybefore, 23, 59)

    temp = CountryAllStatus("https://api.covid19api.com/country/ireland", dateb, datey)
    r = CountryAllStatus.request(temp)
    response = urlcleanup(r)

    print(response["Active"])


def urlcleanup(r):
    mydict = {}
    strR = str(r)
    newstring = (strR.replace('"', '').replace(' ', '').replace("'", '').replace('{', '').replace('}',
                   '').replace('[', '').replace(']', ''))
    new = re.split(",", newstring)
    for item in range(len(new)):
        temp = new[item].split(":", 1)
        for i in range(len(temp)):
            mydict.update({temp[0]: temp[1]})

    return mydict


countryallstatus()
