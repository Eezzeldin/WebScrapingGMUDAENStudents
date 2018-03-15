# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 21:25:15 2017

@author: emadezzeldin

This code is supposed to go through GMU people finder
and retrive the emails and name of student registered
in the DEAN program.

example:
in people finder for the letter 'a' if you press the button last, you will find
1298 pages, but if you go ahead and you press the button 100 to display 100 per page
you will find the last page to be 325
"""
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import lxml.html
import time
import sqlite3
from bs4 import BeautifulSoup
#import urllib
#import certifi
#import requests
import re
#from requests.packages.urllib3.exceptions import InsecureRequestWarning

import certifi
import urllib3
#http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
#http.request('GET', 'https://google.com')
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def OpenBrowser () : 
    global browser
    current_directory = os.getcwd()
    path_to_chromedriver = current_directory + '/chromedriver'
    browser = webdriver.Chrome(executable_path = path_to_chromedriver)

def update_root ():
    global root
    root = lxml.html.fromstring(browser.page_source)
    print (root)
    
OpenBrowser ()
ilink     = 'https://peoplefinder.gmu.edu/index.php?page='+str(1)+ '&results=100&search='+ 'a' +'&group=students&x=0&y=0&mode=standard'
browser.get (ilink)
ilink2   = 'https://eagle.gmu.edu/people_finder/login.php?search=&group=students&x=0&y=0&mode=standard'
browser.get (ilink2)
button = browser.find_element_by_xpath('//*[@id="add-links"]/li[1]/a')
button.click()

username = browser.find_element_by_xpath('//*[@id="login"]')
password = browser.find_element_by_xpath('//*[@id="password"]')
login    = browser.find_element_by_xpath('//*[@id="login-form"]/form/input[1]')

#last page for a :1298
firstnames = []
mypages    = []
myletters  = []
mails      = []
def run():
    conn = sqlite3.connect ('myDEANstudents.sqlite')
    cur  = conn.cursor ()
    cur.execute ('''DROP TABLE IF EXISTS myDEANstudents   ''')
    cur.execute ('''CREATE TABLE IF NOT EXISTS myDEANstudents (Last STRING ,First STRING)  ''')
    
    Lengthes = {}
    Lengthes ['a'] = 317
    Lengthes ['b'] = 84
    Lengthes ['c'] = 117
    Lengthes ['d'] = 123
    Lengthes ['e'] = 261
    Lengthes ['f'] = 38
    Lengthes ['g'] = 88
    Lengthes ['h'] = 176
    Lengthes ['i'] = 239
    Lengthes ['j'] = 75
    Lengthes ['k'] = 89
    Lengthes ['l'] = 194
    Lengthes ['m'] = 161
    Lengthes ['n'] = 253
    Lengthes ['o'] = 180
    Lengthes ['p'] = 55
    Lengthes ['q'] = 9
    Lengthes ['r'] = 231
    Lengthes ['s'] = 189
    Lengthes ['t'] = 143
    Lengthes ['u'] = 104
    Lengthes ['v'] = 42
    Lengthes ['w'] = 51
    Lengthes ['x'] = 11
    Lengthes ['y'] = 101
    Lengthes ['z'] = 41
    counter = 0
    for letter in ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','u','v','r','s','t','w','x','y','z']:
    #page   = 1298
        for page in range (1,Lengthes[letter]+1):
            try:
                #http     = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
                link     = 'https://peoplefinder.gmu.edu/index.php?page='+str(page)+ '&results=100&search='+ letter +'&group=students&x=0&y=0&mode=standard'
                #uh       = http.request ('GET',link)
                #uh       = requests.get(link, allow_redirects=False, timeout=5, verify = False)
                browser.get (link)
                DEANSoup = BeautifulSoup (browser.page_source)
                #DEANSoup = BeautifulSoup (uh.content)
                #DEANSoup.prettify()
                DEAN     = [div for div in DEANSoup.findAll ("div") if 'DAEN' in str(div) and len (str(div)) < 1000]
                for record in DEAN :
                    Last = re.findall ('([A-Z]\w+)',str(record)) [0]
                    First= re.findall ('([A-Z]\w+)',str(record)) [1]
                    mail = str(record('a')[0].get ('href',None))
                    mail = mail.split (':') [1]
                    print (Last,First)
                    firstnames.append(First)
                    mypages.append (page)
                    myletters.append (letter)
                    mails.append (mail)
                    counter = counter + 1
                    cur.execute (''' INSERT INTO myDEANstudents (Last,First) VALUES (?,?)  ''',(Last,First))
                print (page,letter,counter)
                
                #time.sleep(2)
            except:
                print ('Crap')
                continue
    conn.commit()
    cur.close()

run()

#uh.read()
#len(str(div)) for div in DEANSoup.findAll ("div") if 'Neuroscience' in str(div) ]
#[div for div in DEANSoup.findAll ("div") if 'Neuroscience' in str(div) and len (str(div)) < 1000]
#letters = soup.find_all("div", class_="ec_statements")
#re.findall('href=".*">c',str(myNeuro))
#myNeuro ('a')[0].get ('href',None)
#[div('a')[0].get ('href',None) for div in DEANSoup.findAll ("div") if 'Neuroscience' in str(div) and len (str(div)) < 1000]
#Out[172]: ['mailto:cabad@masonlive.gmu.edu', 'mailto:aabbas5@masonlive.gmu.edu']
#
