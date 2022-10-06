"""Dynamically pull down links to all universities in Iran

"""
import re
import csv
import bs4 as bs
import requests


BASE_URL = 'https://www.4icu.org/ir'


local_store = {}

if __name__ == "__main__":
    data = requests.get(BASE_URL, timeout=10)
    soup = bs.BeautifulSoup(data.text, 'html.parser')
    tds = soup.select("td")
    for i in range(1, len(tds), 3):
        try:
            if 'button' in str(tds[i+2]):
                break
            local_store[i] = [str(tds[i+2])[4:-5], tds[i+1]]
        except IndexError:
            pass

for index in local_store.keys():
    town, link = local_store[index]

    name = link.text
    match = re.search(r'/reviews(.)*\"', str(link))
    review_link = match.group(0)[:-1]
    modified_url = BASE_URL[:-3]+review_link
    page = requests.get(modified_url, timeout=10)
    soup = bs.BeautifulSoup(page.text, 'html.parser')
    rows = soup.select('td')
    for row in rows:
        if 'itemprop="url"' in str(row):
            match = re.search(r'\"([a-zA-Z0-9\.\/\:]+)\"', str(row))
            URL = match.group(0)[1:-1]
            local_store[index] = [name, town, URL]

with open('university_list.csv', 'w', newline='', encoding="utf-8") as csvfile:
    row_writer = csv.writer(csvfile, delimiter=';',
                            quotechar='|',
                            quoting=csv.QUOTE_MINIMAL)
    for index in local_store.keys():
        row_writer.writerow(local_store[index])
