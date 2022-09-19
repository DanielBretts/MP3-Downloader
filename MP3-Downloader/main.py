import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pytube import YouTube


video_title = ''


def open_browser():
    global driver
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


def download_song(songs_source, output_path, is_link_related):
    global video_title
    if is_link_related:
        link_to_mp3(songs_source, output_path, is_link_related=is_link_related)
    else:
        open_browser()
        songs_list = open(songs_source, "r")
        url_prefix = "https://www.youtube.com/results?search_query="
        for song in songs_list:
            convert_to_mp3(output_path, song, url_prefix)


def convert_to_mp3(output_path, song, url_prefix):
    global video_title
    full_url = url_prefix + song
    full_url = full_url.replace(" ", "")
    print(full_url)
    driver.get(full_url)
    time.sleep(5)
    web_element = driver.find_element(By.CSS_SELECTOR,
                                      'div#contents ytd-item-section-renderer>div#contents a#thumbnail')
    music_link = web_element.get_attribute('href')
    print(music_link)
    link_to_mp3(music_link, output_path, song)


def link_to_mp3(music_link, output_path, song=None, is_link_related=False):
    global video_title
    yt = YouTube(music_link)
    video_title = yt.title
    print(video_title)
    yt.streams.filter(only_audio=True)
    stream = yt.streams.get_by_itag(251)
    if is_link_related:  # checking if the music source is from a single link
        filename = video_title
    else:
        filename = song.replace("\n", "")

    stream.download(filename=filename + ".mp3", output_path=output_path)

