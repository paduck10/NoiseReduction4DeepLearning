#! python3
# test.py - Launches a map in the browser using an address from the
# Windows execute(Win+R)  or command line. (https://mp3juices.cc)

import os, sys, pyperclip

from time import sleep
import re

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotSelectableException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.action_chains import ActionChains

def openWebsite(mp3Link):
     
     # Open chrome using webdriver module
     global browser
     browser = webdriver.Chrome()
     browser.get(mp3Link)

def downFunc():

     mp3_links = open('yang_radio.txt', 'w+')
     

     for i in range(page_num-1):
          nextElem = browser.find_elements_by_css_selector('img[alt="다음"]')[i]
          nextElem.click()
          sleep(1)

     for i in range(page_num-2, -1, -1):
          prevElem = browser.find_elements_by_css_selector('img[alt="이전"]')[i]
          prevElem.click()
          sleep(1)
     
     episode_count = 0
     for col in range(page_num):
          
          for row in range(10):
               # Click download button
               #songElem = browser.find_element_by_id('query')
               sleep(1)
               songElem = browser.find_elements_by_css_selector('p.download')[episode_count]
               sleep(1)
               songElem.click()

               print('Opened new tab\n')

               # Used for keyboard operation!
               actions = ActionChains(browser)

               # Switch to second tab, and then download .mp3 files
               browser.switch_to_window(browser.window_handles[1])
               sleep(3)
               '''
               actions.key_down(Keys.CONTROL)
               actions.send_keys(Keys.CONTROL + 's')
               actions.key_up(Keys.CONTROL)
               actions.send_keys(Keys.ENTER)
               sleep(1)
               '''

               # Store mp3 links to use wget command in linux machine
               findMp3Link = browser.find_element_by_css_selector('source[type="audio/mpeg"]')
               mp3_link = findMp3Link.get_attribute('src')
               #print(mp3_link)
               mp3_links.write(mp3_link + '\n')
               browser.close()

               # Switch back to the original window(or link, whatever)
               browser.switch_to_window(browser.window_handles[0])

               print('Download %sth episode complete...\n' % episode_count)
               episode_count += 1
               sleep(1)
          
          nextElem = browser.find_elements_by_css_selector('img[alt="다음"]')[col]
          nextElem.click()
          print('Moved to the next page!')
     
     mp3_links.close()

def debugging2():
     for i in range(2):
          nextElem = browser.find_elements_by_css_selector('img[alt="다음"]')[i]
          nextElem.click()
          sleep(1)

     for i in range(1, -1, -1):
          prevElem = browser.find_elements_by_css_selector('img[alt="이전"]')[i]
          prevElem.click()
          sleep(1)

     nextElem = browser.find_elements_by_css_selector('img[alt="다음"]')[0]
     nextElem.click()
     
     songElem = browser.find_elements_by_css_selector('p.download')[10]
     sleep(1)
     songElem.click()
     

def debugging():

     nextElem = browser.find_element_by_css_selector('img[alt="다음"]')
     nextElem.click()
     sleep(1)
     prevElem = browser.find_element_by_css_selector('img[alt="이전"]')
     prevElem.click()
     sleep(1)
     nextElem = browser.find_element_by_css_selector('img[alt="다음"]')
     nextElem.click()

     sleep(1)
     songElem = browser.find_elements_by_css_selector('p.download')[11]
     print(songElem)
     sleep(1)
     print('songElem Element is here : \n')
     print(songElem)
     songElem.click()

     print('Opened new tab\n')

     # Used for keyboard operation!
     actions = ActionChains(browser)

     # Switch to second tab, and then download .mp3 files
     browser.switch_to_window(browser.window_handles[1])
     sleep(10)
     browser.close()

     # Switch back to the original window(or link, whatever)
     browser.switch_to_window(browser.window_handles[0])

     print('Download complete... Move on to the next!\n')
     sleep(1)


# Change the mp3Link, any radio you like to get
# mp3 downloading website
mp3Link = 'http://www.podbbang.com/ch/88'
global page_num = 100

# Make user Input and store in the list
keywordList = []

# Enter the song info, seperated by newline, slash or comma
# If you enter 'quit', close the browser

if __name__ == "__main__":
        
    # Welcoming ascii art!
    print("""


                        /|
        =  =  =      / |
    ____| || || |____/  | -_-_-_-_-_-_
    |)----| || || |____   |     
    ((  | || || |  ))\  | _-_-_-_-_-_-
    \\_|_||_||_|_//  \ |
        \___________/    \|
        
    """)

    openWebsite(mp3Link)
    sleep(5) # wait for browser to be loaded
    downFunc()
    #debugging()
    #debugging2()



'''
while True:
     
     print('What song do you want to download?')
     print("""Downloading multiple files :
Type keywords seperated by slash, comma.
Or, if you copied song names with multiple newlines, Just press enter! :) """)
     print('If you want to quit, enter "quit" or type nothing.')
     

     userInput = input()
     if userInput == 'quit':
          browser.quit()
          sys.exit()
     else:
          if userInput == '':
               userInput = pyperclip.paste()
               print('Ok, so you typed the following :')
               print(userInput)
          keywordRegex = re.compile(r'[^,\r\n]+')
          keywordList = keywordRegex.findall(userInput)
          
          while (len(keywordList) > 0):
                    downFunc(keywordList[0])
                    del keywordList[0]

'''





