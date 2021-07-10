#!/usr/bin/env python3
import json
from typing import Any, Dict, List, Optional, Union
import re
import requests
from bs4 import BeautifulSoup
from os import path

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
DPR_URL = 'https://www.dpr.go.id'


def scrape_year_html():
    directory: Dict[int, Any] = {}

    for year in range(1970, 2021):
        # if year != 2011:
        #     continue

        filepath = f'year_html/{year}.html'
        if not path.isfile(filepath):
            resp = requests.get(
                f'https://www.dpr.go.id/jdih/uu/year/{year}',
                headers={'User-Agent': USER_AGENT}
            )
            soup = BeautifulSoup(resp.content, 'html.parser')

            with open(filepath, 'w') as f:
                f.write(str(soup))

        # --------------------- SCRAPE UU HTML PAGE ---------------------

        metadata_year: List[Dict[str, Any]] = []

        with open(filepath, 'r') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        for i, tr in enumerate(soup.find('table').find_all('tr')):
            if i == 0:
                continue

            metadata_uu: Dict[str, Union[str, int]] = {
                'number': 0,
                'topic': '',
                'metadataPagelink': '',
                'pdfLink': '',
            }
            for j, td in enumerate(tr.find_all('td')):
                if j == 0:
                    metadata_uu['number'] = int(td.find('div').string)
                elif j == 1:
                    metadata_uu['topic'] = td.find("a").string
                    metadata_uu['metadataPagelink'] = f'{DPR_URL}{td.find("a")["href"]}'
                elif j == 2:
                    metadata_uu['pdfLink'] = f'{DPR_URL}{td.find("a")["href"]}'

            metadata_year.append(metadata_uu)

            # if metadata_uu['number'] != 6:
            #     continue

            scrape_uu_html(year, metadata_uu)

        directory[year] = metadata_year

    with open('directory.json', 'w') as f:
        f.write(json.dumps(directory, indent=2))


def scrape_uu_html(year: int, metadata_uu: Dict[str, Union[str, int]]):

    filepath = f'uu_html/uu-{year}-{metadata_uu["number"]}.html'
    if not path.isfile(filepath):
        link = metadata_uu['metadataPagelink']

        assert isinstance(link, str)
        resp = requests.get(link, headers={'User-Agent': USER_AGENT})
        uu_soup = BeautifulSoup(resp.content, 'html.parser')

        with open(filepath, 'w') as f:
            f.write(str(uu_soup))

    with open(filepath, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    scrape_uu_metadata(year, int(metadata_uu['number']), soup)


def scrape_uu_metadata(year: int, number: int, soup: BeautifulSoup):
    filepath = f'uu_json/uu-{year}-{number}.json'

    if path.isfile(filepath):
        print(f'Skipping UU {year} {number}...')
        return

    print(f'Scraping UU {year} {number}...')
    # --------------------- EXTRACT METADATA FROM HTML ---------------------
    metadata: Dict[str, Any] = {
        'status': [],
        'topic': '',
        'year': 0,
        'number': 0,
        'perkara': [],
        'lembaranNegaraNumber': '',
        'tambahanLembaranNegaraNumber': '',
        'peraturanPelaksanaan': [],
    }

    # --------------------- EXTRACT METADATA FROM HTML [TOPIC] ---------------------

    metadata['topic'] = soup.find('div', class_='name-anggota').string

    # --------------------- EXTRACT METADATA FROM HTML [YEAR & NUMBER] ---------------------

    parent = soup.find(class_='group-title', text='PROFIL UU').parent

    metadata['year'] = int(
        parent.find('div', text='Tahun')
        .find_next_siblings('div')[0]
        .string
    )
    metadata['number'] = int(
        parent.find('div', text='Nomor')
        .find_next_siblings('div')[0]
        .string
    )

    # --------------------- EXTRACT METADATA FROM HTML [STATUS] ---------------------

    tags = soup.find_all('div', class_='stitle')
    for tag in tags:
        if tag.string == 'Status':
            ul = tag.parent.ul
            for li in ul.find_all('li'):
                metadata['status'].append(li.string)
        elif tag.string == 'Peraturan Pelaksanaan (Perlak)':
            # print(tag)
            pass

    # --------------------- EXTRACT METADATA FROM HTML [PERKARA] ---------------------

    perkara = soup.find('a', text="Perkara").parent.find('ul').find_all('a')
    for pengujian_uu in perkara:
        metadata['perkara'].append(pengujian_uu.string)

    # --------------------- EXTRACT METADATA FROM HTML [LN & TLN] ---------------------
    metadata['lembaranNegaraNumber'] = soup.find('div', text='LN')\
        .find_next_siblings('div')[0]\
        .string\
        .split()[1]
    metadata['tambahanLembaranNegaraNumber'] = soup.find('div', text='TLN')\
        .find_next_siblings('div')[0]\
        .string\
        .split()[1]

    # --------------------- EXTRACT METADATA FROM HTML [PERATURAN PELAKSANAAN] ---------------------
    table = soup.find('table')
    if table != None:
        for i, tr in enumerate(soup.find('table').find_all('tr')):
            if i == 0:
                continue

            metadata_peraturan = {
                'pasal': '',
                'ayat': '',
                'peraturan': '',
                'keterangan': '',
            }

            for j, td in enumerate(tr.find_all('td')):
                if j == 0:
                    continue
                elif j == 1:
                    [pasal, _, ayat] = td.find('div').contents

                    metadata_peraturan['pasal'] = pasal.split()[1]
                    metadata_peraturan['ayat'] = ayat.split()[1]
                elif j == 2:
                    metadata_peraturan['peraturan'] = td.string
                elif j == 3:
                    metadata_peraturan['keterangan'] = td.string

            metadata['peraturanPelaksanaan'].append(metadata_peraturan)

    # --------------------- SAVE METADATA AS JSON ---------------------

    with open(filepath, 'w') as f:
        f.write(json.dumps(metadata, indent=2))


scrape_year_html()
