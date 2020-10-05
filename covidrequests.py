import requests


class CountryAllStatus:

    def __init__(self, url, date1, date2):
        self.url = url
        self.date1 = date1
        self.date2 = date2

    def request(self):
        url = self.url + "?from=" + str(self.date1) + "&to=" + str(self.date2)
        response = requests.get(url).json()

        return response
