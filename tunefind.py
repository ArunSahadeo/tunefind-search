#!/usr/bin/env python3 -u

import requests, sys, urllib
from time import sleep
try:
	from BeautifulSoup import BeautifulSoup
except ImportError:
	from bs4 import BeautifulSoup
from fake_useragent import UserAgent
ua = UserAgent()
headers = {'User-Agent': ua.random}
found_entries = []
tunefind_search_uri = 'https://www.tunefind.com'

def getSelectedEntry(entries):
    minEntryIndex = int(min(range(len(entries))) + 1)
    maxEntryIndex = int(max(range(len(entries))) + 1)

    if minEntryIndex == maxEntryIndex:
        return entries[0]

    select_number = input("Please select a number from %d to %d: " % (minEntryIndex, maxEntryIndex))

    while not select_number:
        select_number = input("Please select a number from %d to %d: " % (minEntryIndex, maxEntryIndex))

    while not int(select_number) >= minEntryIndex:
        select_number = input("Please select a number from %d to %d: " % (minEntryIndex, maxEntryIndex))

    while not int(select_number) <= maxEntryIndex:
        select_number = input("Please select a number from %d to %d: " % (minEntryIndex, maxEntryIndex))

    selected_entry = found_entries[int(select_number) - 1]

    return selected_entry



search_param = input('Please enter the name of the TV show, movie or artist: ')

while not search_param:
    search_param = input('Please enter the name of the TV show, movie or artist: ')

search_param = urllib.parse.quote(search_param).lower()

search_results = requests.get('%s/search/site?q=%s' % (tunefind_search_uri, search_param), headers)

if 'no results found' in search_results.text.lower():
    print('No results found for your query')
    sys.exit(1)

soup = BeautifulSoup(search_results.text, 'html.parser')

results_table = soup.find(class_='tf-search-results')

results_columns = results_table.find_all(class_='col-md-4')

for results_column in results_columns:
    if not results_column.find('a'): continue
    results_items = results_column.find_all('li')
    for results_item in results_items:
        title = results_column.find('h2').text.lower()
        if title == "shows":
            title = "show"
        elif title == "movies":
            title = "movie"
        elif title == "artists":
            title = "artist"
        link = results_item.find('a')['href']
        name = results_item.find('a').text
        found_content = { 'type': title, 'name': name, 'uri': link }
        found_entries.append(found_content)

print("We have found the following results for your search query:")

for index, found_entry in enumerate(found_entries):
    print("Type of content: %s" % (found_entry['type']))
    print("Name of show, movie, artist: %s" % (found_entry['name']))
    print("Number: %d" % (int(index + 1)))
    print("\n")

selected_entry = getSelectedEntry(found_entries)

request_content_page = requests.get(tunefind_search_uri + selected_entry['uri'], headers)
