from selenium import webdriver
import time
from urlextract import URLExtract
from urllib import parse
import os
from pytube import YouTube
from vimeo_downloader import Vimeo

PASSWORD = os.environ.get("PASSWORD")
USER = os.environ.get("USER")
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'}
driver = webdriver.Chrome('C:\Program Files (x86)\chromedriver.exe')
extractor = URLExtract()


def autorize(user, password):
    driver.get('https://smartclassicalpiano.com/login/')
    driver.find_element_by_xpath('//*[@id="user"]').send_keys(user)
    driver.find_element_by_xpath('//*[@id="pass"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="wp-submit"]').click()


def youtube_downloader(youtube_video, folder, file_name):
    video = YouTube(str(youtube_video))
    print(f"Downloading {file_name} from YouTube")
    video.streams.get_by_itag(18).download(f"d://piano_tutors/{folder}", f"{file_name}.mp4")
    print(f"Downloading of the {file_name} is completed!")


def vimeo_downloader(vimeo_video, page_url, folder, file_name):
    video = Vimeo(f"{vimeo_video}", embedded_on=page_url)  # page_url for embedded links
    video.streams[-2].download(download_directory=f"d://piano_tutors/{folder}", filename=f"{file_name}")


def get_videos(link, name):
    playlist = driver.find_elements_by_class_name("singlevideo-playlist")
    index = 0
    for video in playlist:
        video_link = extractor.find_urls(video.get_attribute("innerHTML"))
        for v in video_link:
            if "youtube" in v:
                if os.path.exists(f'd://piano_tutors/{name}/{name + "_part" + str(index) + ".mp4"}'):
                    index += 1
                youtube_downloader(v, name, f'{name + "_part" + str(index)}')
            elif "vimeo" in v:
                if os.path.exists(f'd://piano_tutors/{name}/{name + "_part" + str(index) + ".mp4"}'):
                    index += 1
                    vimeo_downloader(v, link, name, name + f"_part{index}")


autorize(USER, PASSWORD)
driver.get('https://smartclassicalpiano.com/videos')
page = 2
while True:
    time.sleep(10)
    posts = driver.find_elements_by_class_name("vs-video-wrapper")
    links = []
    for post in posts:
        print(post.get_attribute("innerHTML"))
        links.extend(extractor.find_urls(post.get_attribute("innerHTML"))[0].split())
    print(links)
    for link in links:
        print(link)
        name = parse.urlparse(link).path[6:].strip("/")
        try:
            os.mkdir(f"d://piano_tutors/{name}")
        except FileExistsError:
            continue
        print(f"Currently working on {name}")
        driver.get(link)
        driver.implicitly_wait(10)
        get_videos(link, name)
        driver.implicitly_wait(10)
        driver.get('https://smartclassicalpiano.com/videos')
    driver.implicitly_wait(10)
    driver.find_element_by_xpath(f'//*[@id="page{page}"]').click()
    page += 1
    if page == 16:
        break
