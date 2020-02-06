#! python3
# test.py - Launches a map in the browser using an address from the
# Windows execute(Win+R)  or command line. (https://mp3juices.cc)

import os, sys

from time import sleep
import re

import selenium
from selenium import webdriver

def openWebsite(mp3Link):
     
     # Open chrome using webdriver module
     global browser
     browser = webdriver.Chrome()
     browser.get(mp3Link)
     sleep(10)

def downFunc(keyword):

     # Find searchbar and type keyword
     songElem = browser.find_element_by_id('query')
     songElem.send_keys(keyword)

     # Find and push search button
     searchElem = browser.find_element_by_id('button')
     searchElem.click()

     # Find download button and push it (2 download buttons)
     # use this when you use keyword search
     #sleep(5)
     #downElem = browser.find_element_by_class_name('download')
     #downElem.click()

     # use this when you use links to download
     sleep(30)
     #browser.implicitly_wait(10)
     down2Elem = browser.find_element_by_css_selector('a.url')
     down2Elem.click()
     
     # Clear serchbar for next song
     songElem.clear()

     # diplay text while downloading mp3 file, give some time to browser!
     print('Downloading ' + keyword + '! please wait for 30 sec...')
     i = 0
     while i >= 0:
          print(i, end = '..')
          i -= 1
          sleep(1)
     print('\r\n')


# mp3 downloading website
mp3Link = 'https://mp3juices.cc'


# Make user Input and store in the list
# Read pengsu_youtube.txt
f = open('pengsu_youtube.txt', 'r')
userInput = f.read()
keywordRegex = re.compile(r'[^,\r\n]+')
keywordList = keywordRegex.findall(userInput)
print(keywordList)

# Enter the song info, seperated by newline, slash or comma
# If you enter 'quit', close the browser

openWebsite(mp3Link)

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

while (len(keywordList) > 0):
     downFunc(keywordList[0])
     del keywordList[0]

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






