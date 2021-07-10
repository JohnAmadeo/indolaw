#!/usr/bin/env python3
from pprint import pprint
import json
from typing import Any, Dict, List, Optional, Union
import re
from os import path
import sys
from datetime import datetime
import webbrowser

import requests
from bs4 import BeautifulSoup
from termcolor import colored


USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
BPK_BASE_URL = 'https://peraturan.bpk.go.id'
BPK_SEARCH_URL_PATH = '/Home/Search'


'''
-----------------

SCRAPER

-----------------
'''


def scrape_all_law_details_page():
    directory = open_json('directory.json')

    for year in directory:
        # if int(year) >= 2014:
        #     continue

        save_and_version_directory(directory)
        for entry in directory[year]:
            # if entry['number'] != 6:
            #     continue

            if all(k in entry for k in ['puu', 'status', 'theme']):
                yellow(
                    f"Already scraped BPK law details page of UU {year} No. {entry['number']}")
                continue

            if 'bpkLink' not in entry:
                red(f"UU {year} No. {entry['number']} has no BPK law details page URL")
                continue

            try:
                soup = get_html_soup(entry['bpkLink'])
                data = scrape_law_details_page(soup)

                entry['status'] = data['status']
                entry['theme'] = data['theme']
                entry['puu'] = data['puu']

                green(
                    f"Scraped BPK law details page of UU {year} No. {entry['number']}")
            except Exception as e:
                print(e)
                red(
                    f"Failed to scrape BPK law details page of UU {year} No. {entry['number']}")
                # webbrowser.open(entry['bpkLink'])

        save_json('directory.json', directory)


def scrape_law_details_page(soup: BeautifulSoup):

    data: Dict[str, Any] = {}
    for section in soup.find_all(class_='portlet'):
        section_title = section.find(class_="caption-subject").string
        section_title = " ".join(section_title.split())

        if section_title == "Detail Peraturan":
            theme_data: List[dict] = []
            s = section.find_all(class_='m-grid-row')[-1]
            s = section.find_all(class_='m-grid-col')[-1]
            for theme_span in s.find_all('span'):
                theme_span.text
                theme_data.append({
                    'theme': theme_span.text,
                    'link': f"{BPK_BASE_URL}{theme_span.find('a')['href']}"
                })
            data['theme'] = theme_data

        elif section_title == "Status":
            status_data = scrape_law_details_page_status(section)
            data['status'] = status_data

        elif section_title == 'Uji Materi Mahkamah Konstitusi':
            puu_data = scrape_law_details_page_puu(section)
            data['puu'] = puu_data

    return data


def scrape_law_details_page_status(section) -> dict:
    status_data: Dict[str, List[dict]] = {
    }
    section_body = section.find(class_='portlet-body')

    def clean_whitespace(str):
        return ' '.join(str.split())

    for status_heading_p in section_body.find_all('p'):
        status_heading = status_heading_p.find('span').string
        status_heading = " ".join(status_heading.split()[:-1]).lower()

        status_data[status_heading] = []

        for change in status_heading_p.find_all('li'):
            context = ''
            if change.find(class_='font-blue-oleo') != None:
                context = clean_whitespace(
                    change.find(class_='font-blue-oleo').text)

            law = clean_whitespace(change.text).replace(context, '')

            link = ''
            if change.find('a') != None:
                link = f"{BPK_BASE_URL}{change.find('a')['href']}"

            number = ''
            year = ''
            law_tokens = change.text.split()

            for i, substr in enumerate(law_tokens):
                if substr == 'No.':
                    number = law_tokens[i+1]
                elif substr == 'Tahun':
                    year = law_tokens[i+1]

            status_data[status_heading].append({
                'year': year,
                'number': number,
                'law': law,
                'link': link,
                'context': context,
            })

    return status_data


def scrape_law_details_page_puu(section) -> List[dict]:
    puu_data: List[dict] = []
    for puu_li in section.find_all('li'):
        link = f"{BPK_BASE_URL}{puu_li.find('a')['href']}"
        id = puu_li.find('a').text
        context = ' '.join(puu_li.find('i').text.split())

        puu_data.append({
            'id': id,
            'link': link,
            'context': context,
        })

    return puu_data


def scrape_law_details_page_url(year: int, number: int):
    soup = get_html_soup(build_exact_match_search_url(year, number))

    law_details_page_url_path = soup.find(class_='lead').find("a")["href"]

    # check if URL obtained was correct
    paths = law_details_page_url_path.split('/')[-1].split('-')
    if str(year) not in paths or str(number) not in paths:
        red(
            f'Cannot find BPK law details page URL for UU {year} No. {number} using [EXACT MATCH HEURISTIC]')

        soup = get_html_soup(build_broad_match_search_url(year, number))

        found_url = False
        for div in soup.find_all(class_='portlet'):
            url_path = div.find("a")["href"]

            # check if URL obtained was correct
            path = url_path.split('/')[-1]
            if path == f'uu-no-{number}-tahun-{year}':
                law_details_page_url_path = url_path
                found_url = True
                break

        if not found_url:
            red(
                f'Cannot find BPK law details page URL for UU {year} No. {number} using [BROAD MATCH HEURISTIC]')
            return None

    return f'{BPK_BASE_URL}{law_details_page_url_path}'


def scrape_all_law_details_page_urls():
    directory = open_json('directory.json')
    save_and_version_directory(directory)

    for year in directory:
        for entry in directory[year]:
            number = entry['number']

            if 'bpkLink' in entry:
                yellow(
                    f'BPK law details page URL for UU {year} No. {number} already exists')
                continue

            law_details_page_url = scrape_law_details_page_url(year, number)
            entry['bpkLink'] = law_details_page_url

            green(
                f'Scraped BPK law details page URL for UU {year} No. {number}: {law_details_page_url}')

    save_json('directory.json', directory)


def build_exact_match_search_url(year: int, number: int) -> str:
    params = [
        'filter=1',  # enable filter
        f'search=[{year}|{number}]',  # search term
        'jenis=8',  # filter to only UU
    ]
    return f'{BPK_BASE_URL}{BPK_SEARCH_URL_PATH}?{"&".join(params)}'


def build_broad_match_search_url(year: int, number: int) -> str:
    params = [
        'filter=0',  # disable filter
        f'search=undang+undang+{number}+tahun+{year}',  # search term
    ]
    return f'{BPK_BASE_URL}{BPK_SEARCH_URL_PATH}?{"&".join(params)}'


'''
-----------------

UTILS

-----------------
'''


def get_html_soup(url: str) -> BeautifulSoup:
    resp = requests.get(
        url,
        headers={'User-Agent': USER_AGENT}
    )
    return BeautifulSoup(resp.content, 'html.parser')


def blue(text: str):
    print_color(text, 'blue')


def green(text: str):
    print_color(text, 'green')


def yellow(text: str):
    print_color(text, 'yellow')


def red(text: str):
    print_color(text, 'red')


def print_color(text: str, color: str):
    print(colored(text, color))


def save_and_version_directory(directory: dict):
    # save current directory in case something goes wrong
    timestamp = datetime.today().strftime('%Y-%m-%d-%H-%M')
    save_json(f'versioned_directory/directory-{timestamp}.json', directory)


def open_json(filepath) -> dict:
    return json.load(open(filepath, mode='r'))


def save_json(filepath: str, json_object):
    with open(filepath, 'w') as f:
        f.write(json.dumps(json_object, indent=2))

    green('Saving directory.json')


def print_json(obj: dict):
    print(json.dumps(obj, indent=2))


def open_html(filepath):
    with open(filepath, 'r') as f:
        return f.read()


'''
-----------------

MAIN

-----------------
'''


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('e.g ./bpk_extract.py [FLAG]')
        exit()

    flag = sys.argv[1]

    if flag == '--ldp-url-all':
        blue(f'Scraping BPK law details page URL for all UUs...')
        scrape_all_law_details_page_urls()

    elif flag == '--ldp-url':
        if len(sys.argv) < 3:
            print('e.g ./bpk_extract.py --ldp [YEAR] [NUMBER]')
            exit()

        year = int(sys.argv[2])
        number = int(sys.argv[3])

        if year < 1945:
            print(f'{year} is not a valid year')
            exit()
        if number >= 100:
            print(f'{number} is not a valid UU number')
            exit()

        blue(
            f'Scraping BPK law details page URL for UU {year} No. {number}...')

    elif flag == '--ldp-all':
        scrape_all_law_details_page()
