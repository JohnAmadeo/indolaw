import sys
import os
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

from drive import DriveUploader

import shutil
import json
import requests
import re

search_box_xpath = '//*[@id="search"]/div[1]/div[1]/div[1]/div[1]/div[1]//a'
USER_AGENT = 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25'
CURR_PATH = os.path.dirname(__file__)

def crawl_webpage(uu_name: str) -> None:
    opts = uc.ChromeOptions()
    opts.add_argument('--no-sandbox')
    opts.add_argument('--headless')
    opts.add_argument('--window-size=1920,1080')
    driver = uc.Chrome(options=opts)

    logs = open("logs.txt", "a")
    logs.write(uu_name + '\n')

    uu_link_components = uu_name.split('-')
    uu_link = uu_link_components[0] + '+' + uu_link_components[1] + '+' + uu_link_components[2]

    driver.get('https://www.google.com/search?q=hukumonline+' + uu_link + '+site%3Ahukumonline.com')

    element = driver.find_element(By.XPATH, search_box_xpath)
    hj_url = element.get_dom_attribute('href')

    logs.write(hj_url + '\n')
    print(hj_url)

    driver.close()

    res = requests.get(hj_url, headers={'User-Agent': USER_AGENT})

    soup = BeautifulSoup(res.content, 'html.parser')
    props = soup.find(id='__NEXT_DATA__')
    propsJson = json.loads(props.contents[0])

    if 'activeCatalogFile' not in propsJson['props']['pageProps']:
        logs.write('File probably not the expected UU file\n')
        logs.close()
        return

    fileName: str = propsJson['props']['pageProps']['activeCatalogFile']['title']
    logs.write(fileName + '\n')
    print(fileName)

    regex = 'undang.*undang.*(no.*[\.]|nomor)\s*' + uu_link_components[2] + '\s*tahun.*' + uu_link_components[1]

    if not re.match(regex, fileName.lower()):
        logs.write('File probably not the expected UU file\n')
        logs.close()
        return

    pdf_url = propsJson['props']['pageProps']['downloadLink']['link_download']
    logs.write(pdf_url + '\n')
    print(pdf_url)

    pdf_res = requests.get(pdf_url, headers={'User-Agent': USER_AGENT})

    f = open(uu_name + ".pdf", "wb")
    f.write(pdf_res.content)
    f.close()

    drive_uploader = DriveUploader()
    drive_uploader.drive_upload(uu_name, fileName)

    current_txt_path = CURR_PATH + uu_name + '.txt';
    current_pdf_path = CURR_PATH + uu_name + '.pdf';
    target_txt_path = CURR_PATH + '../unparsed-laws/' + uu_name + '.txt';

    shutil.move(current_txt_path, target_txt_path)
    os.remove(current_pdf_path)   
    logs.close()

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print('e.g. python3 crawler_uu_webpage.py 10 (use -f instead to crawl every pdf)')

    num = None
    
    if sys.argv[1] != '-f':
        num = int(sys.argv[1])

    missing_laws_path = os.path.join(CURR_PATH, '../missing-laws.txt')
    
    f = open(missing_laws_path, "r")
    iterable = [line.strip('\n') for line in f]
    f.close()

    iterable = iterable if num == None else iterable[0:num]

    for uu_name in iterable:
        crawl_webpage(uu_name)

    print(iterable)
    print('Successfully retrieved all UUs above')