"""Dynamically pull down links to all universities in Iran

There is a website at https://www.4icu.org which comprises a list of 
Universities and rankings based within countries.  

This standalone tool pulls down the rankings page for Iran - this gives
a list of links that point to the individual university rank.  From there,
those pages are navigated to and the URL to the school is retrieved.

The links are then written to a .csv file with fiels: University Name, 
City, and the URL.

The URLs 'should' be good - I spot checked a few to confirm retrieved 
results. I also re-confirmed some links via wikipedia entries and 
other tracing.  It's not 100% confirmed but what I think is close enough
to be indicative of a correct URL.
"""
import argparse
import re
import csv
import bs4 as bs
import requests


BASE_URL = 'https://www.4icu.org/ir'


local_store = {}


def main():
    data = requests.get(BASE_URL, timeout=10)
    soup = bs.BeautifulSoup(data.text, 'html.parser')
    tds = soup.select("td")
    for i in range(1, len(tds), 3):
        try:
            # TODO: clean this up. + indices demonstrate lack of
            #       control            
            if 'button' in str(tds[i+2]):
                break
            # TODO: clean this up. + indices demonstrate lack of
            #       control
            local_store[i] = [str(tds[i+2])[4:-5], tds[i+1]]
        except IndexError:
            pass

    for index in local_store.keys():
        town, link = local_store[index]

        # I am never proud of code that takes too many
        # lines to parse anything.
        # TODO: clean it up
        name = link.text
        match = re.search(r'/reviews(.)*\"', str(link))
        review_link = match.group(0)[:-1]
        modified_url = BASE_URL[:-3]+review_link
        page = requests.get(modified_url, timeout=10)
        soup = bs.BeautifulSoup(page.text, 'html.parser')
        rows = soup.select('td')
        for row in rows:
            if 'itemprop="url"' in str(row):
                # TODO: clean up the matching - subsequent parsing
                #       for handling quotes should not be needed
                match = re.search(r'\"([a-zA-Z0-9\.\/\:]+)\"', str(row))
                URL = match.group(0)[1:-1]
                local_store[index] = [name, town, URL]

        # TODO: specify location via command line argument?
        with open('university_list.csv', 'w', newline='', encoding="utf-8") as csvfile:
            row_writer = csv.writer(csvfile, delimiter=';',
                                    quotechar='|',
                                    quoting=csv.QUOTE_MINIMAL)
            for index in local_store.keys():
                row_writer.writerow(local_store[index])


if __name__ == "__main__":
    main()
