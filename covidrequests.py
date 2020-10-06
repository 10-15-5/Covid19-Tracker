import requests


class ByCountryTotal:

    def __init__(self, country, date1, date2):
        """
        :param country: The country that the user has chosen
        :param date1:   The from date that will be sent to the Covid19 API
        :param date2:   The to date that will be sent to the Covid19 API
        """
        self.country = country
        self.date1 = date1
        self.date2 = date2

    def request(self):
        """
        Sends the country, from date and to date to the API and gets back a list object as a response.
        :return list:   Returns a list response got from the API
        """
        url = "https://api.covid19api.com/total/country/" + self.country + "/status/confirmed" + "?from=" + \
              str(self.date1) + "&to=" + str(self.date2)
        response = requests.get(url).json()

        return response


class CountryAllStatus:

    def __init__(self, country, date1, date2):
        """
        :param country: The country that the user has chosen
        :param date1:   The from date that will be sent to the Covid19 API
        :param date2:   The to date that will be sent to the Covid19 API
        """
        self.country = country
        self.date1 = date1
        self.date2 = date2

    def request(self):
        """
        Sends the country, from date and to date to the API and gets back a list object as a response.
        :return list:   Returns a list response got from the API
        """
        url = "https://api.covid19api.com/country/" + self.country + "?from=" + str(self.date1) + \
              "&to=" + str(self.date2)
        response = requests.get(url).json()

        return response


class DayOne:

    def __init__(self, country):
        """
        :param country: The country that the user has chosen
        """
        self.country = country

    def request(self):
        """
        Sends the country to the API and gets back a list object as a response.
        :return list:   Returns a list response got from the API
        """
        url = "https://api.covid19api.com/dayone/country/" + self.country + "/status/confirmed"
        response = requests.get(url).json()

        return response


class WorldCases:

    def __init__(self, date1, date2):
        """
        :param date1:   The from date that will be sent to the Covid19 API
        :param date2:   The to date that will be sent to the Covid19 API
        """
        self.date1 = date1
        self.date2 = date2

    def request(self):
        """
        Sends the from date and to date to the API and gets back a list object as a response.
        :return list:   Returns a list response got from the API
        """
        url = "https://api.covid19api.com/world?from=" + str(self.date1) + "&to=" + str(self.date2)
        response = requests.get(url).json()

        return response
