#!/usr/bin/env python3 -u

import requests, sys, urllib, webbrowser
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

def openLink(externalURI):
    externalURI = tunefind_search_uri + externalURI
    webbrowser.open(externalURI, new=0)

def getSeasonPage(seasonLink):
    selected_episode = None
    request_season_page = requests.get(seasonLink, headers=headers)
    soup = BeautifulSoup(request_season_page.text, 'html.parser')
    seasonEpisodes = soup.find_all(class_='EpisodeListItem__title___32XUR')
    minEntryIndex = int(min(range(len(seasonEpisodes))) + 1)
    maxEntryIndex = int(max(range(len(seasonEpisodes))) + 1)
    for index, seasonEpisode in enumerate(seasonEpisodes):
        print(seasonEpisode.text)
        print('Index : %d' % (index + 1))

    select_number = input('Please select a number from %d to %d for the desired episode: ' % (minEntryIndex, maxEntryIndex))

    while not select_number:
        select_number = input('Please select a number from %d to %d for the desired episode: ' % (minEntryIndex, maxEntryIndex))

    while not int(select_number) >= minEntryIndex:
        select_number = input('Please select a number from %d to %d for the desired episode: ' % (minEntryIndex, maxEntryIndex))

    while not int(select_number) <= maxEntryIndex:
        select_number = input('Please select a number from %d to %d for the desired episode: ' % (minEntryIndex, maxEntryIndex))

    episodeURI = seasonEpisodes[int(select_number) - 1].find('a')

    getEpisodeSong(episodeURI['href'])

def getEpisodeSong(episode):
    selectedTrack = None
    get_episode_page = requests.get(str(tunefind_search_uri + episode), headers)
    soup = BeautifulSoup(get_episode_page.text, 'html.parser')
    allSongs = soup.find_all(class_='SongRow__container___3eT_L')
    minEntryIndex = int(min(range(len(allSongs))) + 1)
    maxEntryIndex = int(max(range(len(allSongs))) + 1)

    if minEntryIndex == maxEntryIndex:
        extractMediaLink(allSongs[0])
        return

    for index, song in enumerate(allSongs):
        song_title = song.find(class_='SongTitle__link___2OQHD')
        song_author = song.find(class_='SongEventRow__subtitle___3Qli4')
        print('Title: %s' % (song_title.text))
        print('Artist: %s' % (song_author.text))
        print('Index: %d' % (int(index) + 1))

    select_number = input('Please select a number from %d to %d for the desired song: ' % (minEntryIndex, maxEntryIndex))

    while not select_number:
        select_number = input('Please select a number from %d to %d for the desired song: ' % (minEntryIndex, maxEntryIndex))

    while not int(select_number) >= minEntryIndex:
        select_number = input('Please select a number from %d to %d for the desired song: ' % (minEntryIndex, maxEntryIndex))

    while not int(select_number) <= maxEntryIndex:
        select_number = input('Please select a number from %d to %d for the desired song: ' % (minEntryIndex, maxEntryIndex))

    selectedTrack = allSongs[int(select_number) - 1]
    playbackLink = extractMediaLink(selectedTrack)
    openLink(playbackLink)

def extractMediaLink(song):
    chosenLink = None
    mediaBtns = song.find(class_='StoreLinks__container___2NqeJ')
    mediaLinks = mediaBtns.find_all('a')
    minEntryIndex = int(min(range(len(mediaLinks))) + 1)
    maxEntryIndex = int(max(range(len(mediaLinks))) + 1)

    if minEntryIndex == maxEntryIndex:
        return mediaLinks[0]['href']

    for index, mediaLink in enumerate(mediaLinks):
        print(mediaLink['alt'])
        print('index: %d' % (int(index) + 1))

    select_number = input('Please select a number from %d to %d for the desired service: ' % (minEntryIndex, maxEntryIndex))

    while not select_number:
        select_number = input('Please select a number from %d to %d for the desired service: ' % (minEntryIndex, maxEntryIndex))

    while not int(select_number) >= minEntryIndex:
        select_number = input('Please select a number from %d to %d for the desired service: ' % (minEntryIndex, maxEntryIndex))

    while not int(select_number) <= maxEntryIndex:
        select_number = input('Please select a number from %d to %d for the desired service: ' % (minEntryIndex, maxEntryIndex))

    return mediaLinks[int(select_number) - 1]['href']

def getSelectedEntry(entries):
    minEntryIndex = int(min(range(len(entries))) + 1)
    maxEntryIndex = int(max(range(len(entries))) + 1)

    if minEntryIndex == maxEntryIndex:
        return entries[0]

    select_number = input('Please select a number from %d to %d: ' % (minEntryIndex, maxEntryIndex))

    while not select_number:
        select_number = input('Please select a number from %d to %d: ' % (minEntryIndex, maxEntryIndex))

    while not int(select_number) >= minEntryIndex:
        select_number = input('Please select a number from %d to %d: ' % (minEntryIndex, maxEntryIndex))

    while not int(select_number) <= maxEntryIndex:
        select_number = input('Please select a number from %d to %d: ' % (minEntryIndex, maxEntryIndex))

    selected_entry = found_entries[int(select_number) - 1]

    return selected_entry

def getSeason(content):
    selectedSeason = None
    request_content_page = requests.get(tunefind_search_uri + content['uri'], headers)
    soup = BeautifulSoup(request_content_page.text, 'html.parser')
    allSeasons = soup.find_all(class_='MainList__item___2MKl8')

    minEntryIndex = int(min(range(len(allSeasons))) + 1)
    maxEntryIndex = int(max(range(len(allSeasons))) + 1)

    if minEntryIndex == maxEntryIndex:
        seasonLink = tunefind_search_uri + allSeasons[0].find('a')['href']
        getSeasonPage(seasonLink)
        return

    for index, season in enumerate(allSeasons):
        season_link = season.find('a')
        print('Title: %s' % (season_link.text))
        print('Index: %d' % (int(index) + 1))

    select_number = input('Please select a number from %d to %d: ' % (minEntryIndex, maxEntryIndex))

    while not select_number:
        select_number = input('Please select a number from %d to %d: ' % (minEntryIndex, maxEntryIndex))

    while not int(select_number) >= minEntryIndex:
        select_number = input('Please select a number from %d to %d: ' % (minEntryIndex, maxEntryIndex))

    while not int(select_number) <= maxEntryIndex:
        select_number = input('Please select a number from %d to %d: ' % (minEntryIndex, maxEntryIndex))

    selectedSeason = allSeasons[int(select_number) - 1]
    seasonLink = str(tunefind_search_uri + selectedSeason.find('a')['href'])
    getSeasonPage(seasonLink)

def getTrack(content):
    selected_track = None
    request_content_page = requests.get(tunefind_search_uri + content['uri'], headers)
    soup = BeautifulSoup(request_content_page.text, 'html.parser')
    all_tracks = soup.find_all(class_='AppearanceRow__container___XH3q9') if content['type'] == 'artist' else soup.find_all(class_='SongRow__container___3eT_L')

    minEntryIndex = int(min(range(len(all_tracks))) + 1)
    maxEntryIndex = int(max(range(len(all_tracks))) + 1)

    if minEntryIndex == maxEntryIndex:
        playback_link = extractMediaLink(all_tracks[0])
        openLink(playback_link)
        return

    for index, track_single in enumerate(all_tracks):
        song_title = track_single.find(class_='AppearanceRow__songInfoTitle___3nWel') if content['type'] == 'artist' else track_single.find(class_='SongTitle__link___2OQHD')
        print('Title: %s' % (song_title.text))
        print('Index: %d' % (int(index) + 1))

    select_number = input('Please select a number from %d to %d for the track you want: ' % (minEntryIndex, maxEntryIndex))

    while not select_number:
        select_number = input('Please select a number from %d to %d: ' % (minEntryIndex, maxEntryIndex))

    while not int(select_number) >= minEntryIndex:
        select_number = input('Please select a number from %d to %d: ' % (minEntryIndex, maxEntryIndex))

    while not int(select_number) <= maxEntryIndex:
        select_number = input('Please select a number from %d to %d: ' % (minEntryIndex, maxEntryIndex))

    selected_track = all_tracks[int(select_number) - 1]
    playback_link = extractMediaLink(selected_track)
    openLink(playback_link)

search_param = input('Please enter the name of the TV show, movie or artist: ')

while not search_param:
    search_param = input('Please enter the name of the TV show, movie or artist: ')

while not search_param.strip():
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
        if title == 'shows':
            title = 'show'
        elif title == 'movies':
            title = 'movie'
        elif title == 'artists':
            title = 'artist'
        link = results_item.find('a')['href']
        name = results_item.find('a').text
        found_content = { 'type': title, 'name': name, 'uri': link }
        found_entries.append(found_content)

print('We have found the following results for your search query:')

for index, found_entry in enumerate(found_entries):
    print('Type of content: %s' % (found_entry['type']))
    print('Name of show, movie, artist: %s' % (found_entry['name']))
    print('Number: %d' % (int(index + 1)))
    print('\n')

selected_entry = getSelectedEntry(found_entries)

if selected_entry['type'] == 'artist' or selected_entry['type'] == 'movie':
    getTrack(selected_entry)
else:
    getSeason(selected_entry)
