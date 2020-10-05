import datetime
import re
from covidrequests import *


def countryallstatus():
    today = datetime.datetime.now()
    datey = datetime.datetime(today.year, today.month, today.day-1)
    dateb = datetime.datetime(today.year, today.month, today.day-2, 23, 59, 59)
    date2daysago = datetime.datetime(today.year, today.month, today.day - 3, 23, 59, 59)

    temp = CountryAllStatus("https://api.covid19api.com/country/ireland", dateb, datey)
    r = CountryAllStatus.request(temp)
    response = urlcleanup(r)

    casesyest = response["Confirmed"]

    temp = CountryAllStatus("https://api.covid19api.com/country/ireland", date2daysago, dateb)
    r = CountryAllStatus.request(temp)
    response = urlcleanup(r)

    cases2days = response["Confirmed"]

    print("Cases Confirmed Yesterday:\t", int(casesyest) - int(cases2days))


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
