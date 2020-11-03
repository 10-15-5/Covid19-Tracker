import datetime
import re
import pycountry
import numpy as np
import matplotlib.pyplot as plt
from covidrequests import *
from matplotlib.dates import drange


def welcomescreen():
    """
    This is the welcome screen, user chooses what they want to see and then chooses the country they want the data for.

    At the moment the country input only supports the ISO-3 country codes.
    If the user chooses option 5 they don't get to choose a country as that is the world case option.
    Once they have chosen a country they get sent to the coresponding fucntion with their chosen country
    :return None:
    """
    print("Welcome to the Covid-19 Tracker App")

    ans = input("What would you like to see?\n"
                "1) Total Numbers for country (Confirmed, Recoveries, Deaths & Active cases)\n"
                "2) Deaths\t\t\t\t\t\t\t"
                "3) Days since first confirmed case\n"
                "4) Yesterday's Confirmed Cases\t\t"
                "5) World Cases\n"
                "6) Cases Betweem Specific Dates\t\t"
                "7) Plot a country's cases (In Progress...)\n")

    if ans != "5":
        try:
            print("Please enter the country you would like to see (Using their 3 letter country codes)")
            country = input("eg. IRL = Ireland, GBR = United Kingdom, USA = USA\n").upper()
            c = pycountry.countries.get(alpha_3=country).name

            for i in range(len(c)):
                if c[i] == ' ':
                    c = c.replace(c[i], '-')

            if ans == "1":
                totalnumbers(c)
            elif ans == "2":
                newdeaths(c)
            elif ans == "3":
                dayssincefirst(c)
            elif ans == "4":
                newcases(c)
            elif ans == "6":
                specificdates(c)
            elif ans == "7":
                plotcases(c)
        except AttributeError:
            print("ERROR!\t" + country + " is not a valid 3 letter code")

    else:
        worldcases()


def totalnumbers(country):
    """
    This function displays the total numbers for the user's chosen country.

    It gets the current date and also yesterday's date.
    Pushes them, and the country, to the CountryAllStatus class and gets back a list.
    It sends the list to urlcleanup and gets a dictionary back.
    It then prints out the Total Cases, Deaths, Recoveries and Active Cases for that country
    :param country:
    :return prints to console:
    """
    temp = ByCountryTotalAllStatus(country)
    r = ByCountryTotalAllStatus.request(temp)
    lastitem = r[-1]

    print("Total numbers for " + country)
    print("Total Cases:\t\t", f"{lastitem['Confirmed']:,d}",
          "\nTotal Deaths:\t\t", f"{lastitem['Deaths']:,d}",
          "\nTotal Recoveries:\t", f"{lastitem['Recovered']:,d}",
          "\nTotal Active Cases:\t", f"{lastitem['Active']:,d}")


def newcases(country):
    """
    This function shows the user the amount of new cases in their chosen country.

    It gets todays date and the dates all the way back until 3 days ago.
    It passes todays date and yesterdays date into ByCountryTotal and gets the total cases yesterday
    It passes 2 days ago's date and 3 days ago's date into ByCountryTotal and gets the total cases 2 days ago.
    It calculates the total new cases by subtracting the total cases from 2 days ago to the total cases yesterday.
    It then prints this info to the console.
    :param country:
    :return prints to console:
    """
    today = datetime.datetime.now()
    datey = today - datetime.timedelta(days=1)
    dateb = today - datetime.timedelta(days=2)
    date3daysago = today - datetime.timedelta(days=3)

    temp = ByCountryTotal(country, dateb, datey)
    r = ByCountryTotal.request(temp)
    response = urlcleanup(r)

    casesyest = response["Cases"]

    temp = ByCountryTotal(country, date3daysago, dateb)
    r = ByCountryTotal.request(temp)
    response = urlcleanup(r)

    cases2days = response["Cases"]

    print("Cases Confirmed Yesterday in " + country + ":\t", f"{int(casesyest) - int(cases2days):,d}")
    print("This number includes all cases for all the different territories of this country")


def newdeaths(country):
    """
    Very similar to the last function, this function shows the user the amount of new deaths in their chosen country.

    It gets todays date and the dates all the way back until 3 days ago.
    It passes todays date and yesterdays date into CountryAllStatus and gets the total cases yesterday
    It passes 2 days ago's date and 3 days ago's date into CountryAllStatus and gets the total cases 2 days ago.
    It calculates the total new deaths by subtracting the total deaths from 2 days ago to the total deaths yesterday.
    It then prints this info to the console.
    :param country:
    :return prints to console:
    """
    today = datetime.datetime.now()
    datey = today - datetime.timedelta(days=1)
    dateb = today - datetime.timedelta(days=2)
    date3daysago = today - datetime.timedelta(days=3)

    temp = CountryAllStatus(country, dateb, datey)
    r = CountryAllStatus.request(temp)
    response = urlcleanup(r)

    casesyest = response["Deaths"]

    temp = CountryAllStatus(country, date3daysago, dateb)
    r = CountryAllStatus.request(temp)
    response = urlcleanup(r)

    cases2days = response["Deaths"]

    print("Deaths Confirmed Yesterday in " + country + ":\t", f"{int(casesyest) - int(cases2days):,d}")


def dayssincefirst(country):
    """
    Shows the user how long it's been since their chosen country's first confirmed case.

    Passes the country through to DayOne and gets back a list of all the days since the first confimred case.
    List at index 0 is the first day's details and that's all we need so we get rid of the rest of the list.
    Index 0 is a dictionary and we can refernece the Date to get a string version of the first date a case was confirmed.
    It then converts the string date object into it's corresponding datetime object.
    In order to print it to the screen it has to be reformatted to the European convention of dd/mm/yyyy.
    This data is then printed to the console.
    :param country:
    :return prints to console:
    """
    today = datetime.datetime.now().date()
    temp = DayOne(country)
    r = DayOne.request(temp)
    dets = r[0]
    date = dets["Date"]
    date = date.split("T")

    date = datetime.datetime.strptime(date[0], "%Y-%m-%d").date()
    delta = today - date
    print("The first reported case for " + country + " was on: " + str(date.day) +
          "/" + str(date.month) + "/" + str(date.year) + "\nIt has been " + str(delta.days) + " days since the first "
                                                                                              "confirmed case!")


def worldcases():
    """
    Shows the user the new numbers of cases, deaths & recoveries on a worldwide scale.

    Gets the date of today and yesterday.
    Passes both of these dates into WorldCases and gets back a list.
    Passes this list into urlcleanup to get back a dictionary.
    It then prints the details of new cases, deaths and recoveries to the console.
    :return prints to console:
    """
    today = datetime.datetime.now()
    datey = today - datetime.timedelta(days=1)

    temp = WorldCases(datey, today)
    r = WorldCases.request(temp)
    response = urlcleanup(r)

    print("Total Cases:\t\t" + f"{int(response['TotalConfirmed']):,d}" + "\nTotal Deaths:\t\t" +
          f"{int(response['TotalDeaths']):,d}" +
          "\nTotal Recoveries:\t" + f"{int(response['TotalRecovered']):,d}\n")

    print("New Cases:\t\t\t" + f"{int(response['NewConfirmed']):,d}" + "\nNew Deaths:\t\t\t" +
          f"{int(response['NewDeaths']):,d}" +
          "\nNew Recoveries:\t\t" + f"{int(response['NewRecovered']):,d}")


def specificdates(country):
    """
    Returns all the info for a specific country between certain dates.

    The UK and US aren't available yet as these countries have many different provinces and territories and I still
    have yet to cater for that.
    If you don't choose the US or UK you are then asked to enter a from date and a to date in the form dd/mm/yyyy.
    It then converts these two dates to datetime objects so they can be passed through to the API.
    It then passes the country, from date and to date through to the API and gets back a list of all the info between
    the two specified dates.
    Then it takes the first item form the list and the last item from the list as this is all we'll need to get the
    info that will be shown to the user.
    It then prints all the necessary info to the screen for the user.
    :param country:
    :return prints to console:
    """
    if country == "United-Kingdom" or country == "United-States":
        print("This function is not available for " + country + " yet as I haven't configured all the different "
                                                                "provinces, check back soon!")
    else:
        date1 = input("Please enter a start date in the form dd/mm/yyyy:\n")
        date2 = input("Please enter an end date in the form dd/mm/yyyy:\n")
        date1 = date1.split("/")
        date2 = date2.split("/")

        date1 = datetime.datetime(int(date1[2]), int(date1[1]), int(date1[0]))
        date2 = datetime.datetime(int(date2[2]), int(date2[1]), int(date2[0]))

        temp = CountryAllStatus(country, date1, date2)
        r = CountryAllStatus.request(temp)

        firstitem = r[0]
        lastitem = r[-1]

        print("These are the results for " + country + " between", date1.date(), "and", date2.date(), ":\n")
        print("Amount of New Cases:\t\t" + f"{int(lastitem['Confirmed']) - int(firstitem['Confirmed']):,d}" +
              "\nAmount of New Deaths:\t\t" + f"{int(lastitem['Deaths']) - int(firstitem['Deaths']):,d}" +
              "\nAmount of New Recoveries:\t" + f"{int(lastitem['Recovered']) - int(firstitem['Recovered']):,d}" +
              "\nAmount of New Active Cases:\t" + f"{int(lastitem['Active']) - int(firstitem['Active']):,d}" +
              "\nTotal amount of cases by", date1.date(), ":\t\t" + f"{int(firstitem['Confirmed']):,d}" +
              "\nTotal amount of cases by", date2.date(), ":\t\t" + f"{int(lastitem['Confirmed']):,d}")


def plotcases(country):
    if country == "United-Kingdom" or country == "United-States":
        print("This function is not available for " + country + " yet as I haven't configured all the different "
                                                                "provinces, check back soon!")
    else:
        cases = []
        date1 = input("Please enter a start date in the form dd/mm/yyyy:\n")
        date2 = input("Please enter an end date in the form dd/mm/yyyy:\n")
        date1 = date1.split("/")
        date2 = date2.split("/")

        date1 = datetime.datetime(int(date1[2]), int(date1[1]), int(date1[0]))
        date2 = datetime.datetime(int(date2[2]), int(date2[1]), int(date2[0])) + datetime.timedelta(days=1)
        delta = datetime.timedelta(hours=24)
        dates = drange(date1, date2, delta)

        temp = CountryAllStatus(country, date1, date2)
        r = CountryAllStatus.request(temp)
        cleaned = cleanup(r)

        for i in range(len(cleaned)):
            if cleaned[i] == "Confirmed":
                cases.append(int(cleaned[i+1]))

        y = np.array(cases)

        plt.plot_date(dates, y)
        plt.title("Cases between " + str(date1) + " and " + str(date2), fontweight="bold")
        plt.show()


def urlcleanup(r):
    """
    Takes in a list and returns a dictionary equivalent so it is easier to access.

    It changes the list into a string.
    Then it removes all the unnecessary punctuation marks from the string.
    It then splits the string at every comma.
    Then it cycles through the new list that is split at every comma and splits it again at the first instance of a
    colon it come across, this stop it from splitting time objects multiple times.
    It updates the dictionary with each key and valut it gets from splitting at the colons.
    Then returns the dicitonary to the calling function.
    :param r:
    :return dicitonary:
    """
    mydict = {}
    strR = str(r)
    newstring = (strR.replace('"', '').replace(' ', '').replace("'", '').replace('{', '').replace('}',
                 '').replace('[','').replace(']', ''))
    new = re.split(",", newstring)
    for item in range(len(new)):
        temp = new[item].split(":", 1)
        for i in range(len(temp)):
            mydict.update({temp[0]: temp[1]})

    return mydict


def cleanup(r):
    strR = str(r)
    newstring = (strR.replace('"', '').replace(' ', '').replace("'", '').replace('{', '').replace('}',
                               '').replace('[', '').replace("]", ""))
    list = re.split("[:,]", newstring)

    return list


welcomescreen()
