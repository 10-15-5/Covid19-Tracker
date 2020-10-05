import datetime
import re
import pycountry
from covidrequests import *


def welcomescreen():
    print("Welcome to the Covid-19 Tracker App")

    ans = input("What would you like to see?\n1) Confirmed Cases\t*N/A\n2) Recovered\t*N/A\n3) Deaths\n"
                "4) Days since first confirmed case\t*N/A\n5) Today's Confirmed Cases\n6) World Cases\n")
    if ans != "6":
        print("Please enter the country you would like to see (Using their 3 letter country codes)")
        country = input("eg. IRL = Ireland, GBR = United Kingdom, WOR = World\n").upper()
        if country != "WOR":
            c = pycountry.countries.get(alpha_3=country).name

        for i in range(len(c)):
            if c[i] == ' ':
                country = c.replace(c[i], '-')

        if ans == "1":
            print("Not available yet! Sorry")
        elif ans == "2":
            print("Not available yet! Sorry")
        elif ans == "3":
            deaths(country)
        elif ans == "4":
            print("Not available yet! Sorry")
        elif ans == "5":
            countrytotal(c)
    else:
        worldcases()


def countrytotal(country):
    today = datetime.datetime.now()
    datey = datetime.datetime(today.year, today.month, today.day-1)
    dateb = datetime.datetime(today.year, today.month, today.day-2, 23, 59, 59)
    date2daysago = datetime.datetime(today.year, today.month, today.day - 3, 23, 59, 59)

    temp = ByCountryTotal(country, dateb, datey)
    r = ByCountryTotal.request(temp)
    response = urlcleanup(r)

    casesyest = response["Cases"]

    temp = ByCountryTotal(country, date2daysago, dateb)
    r = ByCountryTotal.request(temp)
    response = urlcleanup(r)

    cases2days = response["Cases"]

    print("Cases Confirmed Yesterday:\t", int(casesyest) - int(cases2days))
    print("This number includes all cases for all the different territories of this country")


def deaths(country):
    today = datetime.datetime.now()
    datey = datetime.datetime(today.year, today.month, today.day - 1)
    dateb = datetime.datetime(today.year, today.month, today.day - 2, 23, 59, 59)
    date2daysago = datetime.datetime(today.year, today.month, today.day - 3, 23, 59, 59)

    temp = CountryAllStatus(country, dateb, datey)
    r = CountryAllStatus.request(temp)
    response = urlcleanup(r)

    casesyest = response["Deaths"]

    temp = CountryAllStatus(country, date2daysago, dateb)
    r = CountryAllStatus.request(temp)
    response = urlcleanup(r)

    cases2days = response["Deaths"]

    print("Deaths Confirmed Yesterday:\t", int(casesyest) - int(cases2days))


def worldcases():
    today = datetime.datetime.now()
    datey = datetime.datetime(today.year, today.month, today.day - 1)
    dateb = datetime.datetime(today.year, today.month, today.day - 2, 23, 59, 59)

    temp = WorldCases(dateb, datey)
    r = WorldCases.request(temp)
    response = urlcleanup(r)

    cases = response["NewConfirmed"]
    deaths = response["NewDeaths"]
    recovered = response["NewRecovered"]

    print("New Cases:\t" + cases + "\nNew Deaths:\t" + deaths + "\nNew Recoveries:\t" + recovered)


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


welcomescreen()
