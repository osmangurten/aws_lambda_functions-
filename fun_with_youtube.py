from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from pytube import YouTube
import time

class FetchMedia:
    @classmethod
    def init_driver(cls):
        '''If private browsing is not set, youtube prompts for a login'''
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
        url = 'https://www.youtube.com/'
        driver = Firefox(executable_path="/Users/si3mshady/geckodriver",firefox_profile=firefox_profile)
        driver.get(url)
        driver.implicitly_wait(5)
        return driver

    @classmethod
    def fetch_from_yt(cls,search_string,time_interval):
        #easier to use seleniu￿m when the element id is known
        driver = cls.init_driver()
        search_field = driver.find_element(By.XPATH,"//input[@id='search']")
        search_field.send_keys(search_string)
        search_button  = driver.find_element(By.XPATH,"//button[@id='search-icon-legacy']")
        search_button.click()
        filter_button = driver.find_element(By.XPATH,"//paper-button[@id='button']/yt-icon")
        filter_button.click()
        select_filter = driver.find_element(By.XPATH,cls.time_frame(time_interval))
        select_filter.click()
        media = driver.find_element(By.XPATH,"(//div[@id='contents']//a[@id='video-title' and @href])[1]")
        media.click()
        time.sleep(10)
        current_url = driver.current_url
        print(current_url)
        YouTube(current_url).streams.first().download()


    @classmethod
    def time_frame(cls, timeframe):
        '''values: "Last hour, Today, This week, This year'''
        split_string = timeframe.lower().split()
        if len(split_string) == 0:
            exit(1)
        elif len(split_string) == 1:
            timeframe = split_string[0].title()
            return f"//yt-formatted-string[contains(text(),'{timeframe}')]"
        else:
            timeframe = split_string[0].title() + ' ' + split_string[1]
            return f"//yt-formatted-string[contains(text(),'{timeframe}')]"

    @classmethod
    def download_media(cls,mediaLink):
        pass


#Python Selenium Pytube practice
#Small exercise to search for and download media from youtube
#Elliott Arnold 11-7-19

if __name__ == '__main__':
    ss = input('Please enter your search string: ')
    print("Please enter a time frame filter for your search:\nAcceptable values are:")
    tff = input('''"Last hour", "Today", "This week", "This year"\n''')
    FetchMedia.fetch_from_yt(ss,tff)