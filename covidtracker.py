import datetime
import re
import pycountry
from covidrequests import *


def welcomescreen():
    print("Welcome to the Covid-19 Tracker App")

    ans = input("What would you like to see?\n"
                "1) Confirmed Cases\t*N/A\t\t\t2) Recovered\t*N/A\n"
                "3) Deaths\t\t\t\t\t\t\t4) Days since first confirmed case\t*N/A\n"
                "5) Today's Confirmed Cases\t\t\t6) World Cases\n"
                "7) Cases Betweem Specific Dates\n")
    
    if ans != "6":
        print("Please enter the country you would like to see (Using their 3 letter country codes)")
        country = input("eg. IRL = Ireland, GBR = United Kingdom, USA = USA\n").upper()
        if country != "WOR":
            c = pycountry.countries.get(alpha_3=country).name

        for i in range(len(c)):
            if c[i] == ' ':
                c = c.replace(c[i], '-')

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
        elif ans == "7":
            specificdates(c)
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


def specificdates(country):
    date1 = input("Please enter a start date in the form dd/mm/yyyy:\n")
    date2 = input("Please enter an end date in the form dd/mm/yyyy:\n")
    date1 = date1.split("/")
    date2 = date2.split("/")

    date1 = datetime.datetime(int(date1[2]), int(date1[1]), int(date1[0]))
    date2 = datetime.datetime(int(date2[2]), int(date2[1]), int(date2[0]))

    temp = CountryAllStatus(country, date1, date2)
    r = CountryAllStatus.request(temp)




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
