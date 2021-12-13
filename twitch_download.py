from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import subprocess
import argparse
import os
import sys

# Settings
chrome_driver_path = ''
path_to_downloads_dir = ''

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--range', help="[24hr, 7d, 30d, all]")
parser.add_argument('-l', '--limit', help="limit of downloaded clips")
args = parser.parse_args()

# Set names of twitch_creators
twitch_creators = []
s=Service(chrome_driver_path)
browser = webdriver.Chrome(service=s)

for t_creator in twitch_creators:
    # Navigate to downloads dir
    os.chdir(path_to_downloads_dir)
    dir_content = os.listdir()
    if t_creator not in dir_content:
        os.mkdir(os.path.join(os.getcwd(), t_creator))

    os.chdir(os.path.join(os.getcwd(), t_creator))

    # Fetch links of clips and download
    url = 'https://www.twitch.tv/' + t_creator + '/clips' + '?filter=clips&range=' + args.range
    browser.get(url)
    all_elements = browser.find_elements(By.XPATH, '//a[@data-a-target="preview-card-image-link"]')
    limited_elements = all_elements[:int(args.limit)]

    for element in limited_elements:
        subprocess.run([sys.executable, '../../twitch-dl.pyz', 'download', '-q', 'source', element.get_attribute("href")])
