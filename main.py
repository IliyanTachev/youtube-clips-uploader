from selenium import webdriver

import requests
import wget
import zipfile
import os
import time

from selenium.webdriver.common.by import By

def findElement(by=By.CSS_SELECTOR, value=None, number_of_sec_before_fail=60):
    for i in range(0, number_of_sec_before_fail, 1):
        try:
            element = driver.find_element(by, value)
            return element
        except:
            time.sleep(1)

    # if we are outside the loop this means we didn't find the element so the line below is going to throw an exception
    element = driver.find_element(by, value)


def install_latest_chromedriver():
    # delete already existing chromedriver and then install the latest one to ensure no version issues
    if os.path.exists("chromedriver.exe"):
        os.remove("chromedriver.exe")

    # get the latest chrome driver version number
    url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
    response = requests.get(url)
    version_number = response.text

    # build the donwload url
    download_url = "https://chromedriver.storage.googleapis.com/" + version_number +"/chromedriver_win32.zip"

    # download the zip file using the url built above
    latest_driver_zip = wget.download(download_url,'chromedriver.zip')

    # extract the zip file
    with zipfile.ZipFile(latest_driver_zip, 'r') as zip_ref:
        zip_ref.extractall(path="./")  # you can specify the destination folder path here
    # delete the zip file downloaded above
    os.remove(latest_driver_zip)


# initialize the webdriver
def initialize_webdriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
    return webdriver.Chrome(executable_path="./chromedriver.exe", chrome_options=chrome_options)


def upload_yt_video(file_to_upload='none', video_description='none', tumbnail_path='none', video_visibility='hidden', for_kids=False, for_mature_audience=False):
    # navigate to the screen where a YouTube video is uploaded from
    driver.get("https://studio.youtube.com/")
    try:
        findElement(value="#dismiss-button", number_of_sec_before_fail=5).click()
    except:
        pass
    findElement(value="#menu-item-1").click()
    findElement(value="#create-icon").click()
    findElement(value="#text-item-0").click()

    # selects which video file will be uploaded to YouTube
    findElement(value="#content > input[type=file]").send_keys(file_to_upload)

    # fills in the video description given by the user
    findElement(value=".style-scope:nth-child(2) > #container > #outer > #child-input #textbox").send_keys(video_description)

    # upload a thumbnail photo for the video
    if tumbnail_path != 'none' and tumbnail_path != '':
        findElement(value="#file-loader").send_keys(tumbnail_path)


    # select if the video is for kids or not
    if for_kids:
        findElement(value="#audience > ytkc-made-for-kids-select > div.made-for-kids-rating-container.style-scope.ytkc-made-for-kids-select > tp-yt-paper-radio-group > tp-yt-paper-radio-button:nth-child(1)").click()
    else:
        findElement(value="#audience > ytkc-made-for-kids-select > div.made-for-kids-rating-container.style-scope.ytkc-made-for-kids-select > tp-yt-paper-radio-group > tp-yt-paper-radio-button:nth-child(2)").click()

        # select if the video is for 18+ or not (this feature is here (in this else) because the video can be for 18+ only if it's not for kids)
        if for_mature_audience:
            findElement(value="#audience > button").click()
            findElement(value="#age-restriction-group > tp-yt-paper-radio-button:nth-child(1)").click()

    # click 'next' 3 times (change that in the future when we want cards(to sub and check out other videos) at the end of our videos)
    for i in range(3):
        findElement(value="#next-button > div").click()
        time.sleep(0.5)

    # select video visibility (private, hidden, public)
    video_visibility = video_visibility.lower()
    if video_visibility == "public":
        findElement(by=By.XPATH, value="//*[@id=\"privacy-radios\"]/tp-yt-paper-radio-button[3]").click()
    elif video_visibility == "private":
        findElement(value="#private-radio-button").click()
    elif video_visibility == "hidden":
        findElement(by=By.XPATH, value="//*[@id=\"privacy-radios\"]/tp-yt-paper-radio-button[2]").click()

    # click upload video btn
    time.sleep(1)
    findElement(value="#done-button > div").click()
    #print(f"Video '{driver.find_element(By.CSS_SELECTOR, '#watch-url').get_attribute('innerText')}' was uploaded successfully.")
    findElement(value="#close-button > div").click()


# install the latest chrome driver and open the Chrome window instance with a cmd command
install_latest_chromedriver()
localhost_dir_path = os.path.join(os.getcwd(), "localhost")
os.system(f'start cmd /c "c: & cd C:\Program Files (x86)\Google\Chrome\Application & chrome.exe --remote-debugging-port=9222 --user-data-dir="{localhost_dir_path}""')
os.system('start cmd /c "Taskkill /IM cmd.exe /f"')

driver = initialize_webdriver()

try:
    upload_yt_video(
        file_to_upload = "D://COMPUTER/Хр фаилове/valorant/videos/Desktop/Desktop 2021.01.16 - 17.43.25.03.DVR.mp4",
        video_description = 'Sample Descrition',
        video_visibility = 'hidden',
        for_kids = False,
        for_mature_audience = False
    )
except Exception as e:
    print(e)
    driver.close()
    os.system('start cmd /c "Taskkill /IM chromedriver.exe /f"')