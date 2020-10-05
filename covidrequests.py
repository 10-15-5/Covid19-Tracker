import requests


class ByCountryTotal:

    def __init__(self, country, date1, date2):
        self.country = country
        self.date1 = date1
        self.date2 = date2

    def request(self):
        url = "https://api.covid19api.com/total/country/" + self.country + "/status/confirmed" + "?from=" + \
              str(self.date1) + "&to=" + str(self.date2)
        response = requests.get(url).json()

        return response


class CountryAllStatus:

    def __init__(self, country, date1, date2):
        self.country = country
        self.date1 = date1
        self.date2 = date2

    def request(self):
        url = "https://api.covid19api.com/country/" + self.country + "?from=" + str(self.date1) + \
              "&to=" + str(self.date2)
        response = requests.get(url).json()

        return response


class WorldCases:

    def __init__(self, date1, date2):
        self.date1 = date1
        self.date2 = date2

    def request(self):
        url = "https://api.covid19api.com/world?from=" + str(self.date1) + "&to=" + str(self.date2)
        response = requests.get(url).json()

        return response
