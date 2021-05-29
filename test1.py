# -*- coding: utf-8 -*-
import requests
import time
import os.path
import datetime
now = datetime.datetime.now()
""" TBD:
1) Check for more possible unexpected errors
2) Add another agency. Perhaps mmreality.cz
3) more optimization
"""
class simpleCrawler:
    def __init__(self):
        self.available = 0
        self.data = 0
        self.url = "https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&locality_district_id=51&locality_region_id=11&per_page=999"
        self.new_hashes = []

    def get_hashes(self):
        try:
            response = requests.get(self.url)
            json_data = response.json()
            data = json_data.get("_embedded", None).get("estates", None)
            return data

        except requests.exceptions.RequestException:
            data = "broken"  # o_o !!!!
            return data

    def compare(self):
        data = self.get_hashes()
        if data == "broken":
            print(now.strftime("[%H:%M] Oops, něco se pokazilo. :/ Zkontroluj připojení k Internetu."))
        else:
            for estate in data:
                self.new_hashes.append(str(estate.get("hash_id", None)))

            print(now.strftime("[%H:%M] Kontroluji..."))

            with open('hash.txt', 'r') as oldHash:
                b = set(oldHash.read().splitlines())
                set_difference = set(self.new_hashes) - set(b)
                list_difference = list(set_difference)

            if not list_difference:
                print(now.strftime("[%H:%M] Žádna změna nenastala <3"))
            else:
                for line in list_difference:
                    print(now.strftime(f"[%H:%M] Nové byty! https://www.sreality.cz/detail/prodej/byt/a/b/{line}"))
            os.remove("hash.txt")
            save_hashes()

    def check_hashes(self):
        if os.path.isfile('hash.txt'):
            self.compare()
        else:
            print(now.strftime("[%H:%M] Nejspíš je program zapnut poprvé, stáhu nejnovější byty. Budu informovat při zmeně"))
            save_hashes()


def save_hashes():
    data = gD.get_hashes()
    if data != "broken":
        for estate in data:
            with open("hash.txt", 'a') as file:
                hashids = (estate.get("hash_id", None))
                if hashids is None:
                    print(now.strftime("[%H:%M] Oops, něco se pokazilo. :/ Seznam API update?"))
                else:
                    if isinstance(hashids, int):
                        file.writelines(str(hashids) + "\n")
                    else:
                        print(now.strftime("[%H:%M] Oops, něco se pokazilo. :/ Seznam API update?"))

    else:
        print(now.strftime("[%H:%M] Oops, něco se pokazilo. :/ Zkontroluj připojení k Internetu."))

gD = simpleCrawler()
while True:
    gD.check_hashes()
    time.sleep(600) #kontroluje každých 10minut.