from bs4 import BeautifulSoup
import requests
import xlsxwriter
import re
import pandas as pd
import random
from collections import OrderedDict
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Get browser header 
def getDynamicHeader():
    # This data was created by using the curl method explained above
    headers_list = [
        # Firefox 77 Mac
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.google.com/",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        },
        # Firefox 77 Windows
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.google.com/",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        },
        # Chrome 83 Mac
        {
            "Connection": "keep-alive",
            "DNT": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "Referer": "https://www.google.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
        },
        # Chrome 83 Windows 
        {
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": "https://www.google.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9"
        }
    ]
    # Create ordered dict from Headers above
    ordered_headers_list = []
    for headers in headers_list:
        h = OrderedDict()
        for header,value in headers.items():
            h[header]=value
        ordered_headers_list.append(h)
    headers = random.choice(headers_list)
    return headers

#Get web page contents using request.
def getWebPageContent(webUrl):
    headers = getDynamicHeader()
    webpage = requests.get(webUrl, headers=headers,verify=False).text # url source
    soup = BeautifulSoup(webpage, "lxml")
    return soup

#Get email from content.
def getEmail(emailContent):
    emailRegEx = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
    m = emailRegEx.search(emailContent)
    if m:
        email = m.group(0)
    return email

def getWebSite(webContent):
    webRegex = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
    m = webRegex.search(webContent)
    if m:
        website = m.group(0)
    return website
#Remove tab and white spaces.
def formatAddressContent(companyAddress):
    companyAddress = companyAddress.replace('\t','')
    companyAddress = companyAddress.replace('\r','')
    companyAddress = companyAddress.replace('\n','')
    companyAddress = companyAddress.strip()
    return companyAddress

def soupContentSelect(soupContent, htmlDom):
    contactInfo = soupContent.select(htmlDom)
    return contactInfo

#Get all the a href links in the webpage.
def getAllHrefLinks(soupContent,linkPathPrefix,findFromContent = False):
    if findFromContent == True:
        filtered = soupContent.select(linkPathPrefix)
    else:
        filtered = []
        for linkContent in soupContent:
            if linkPathPrefix:
                filtered.append(linkContent.find('a', href= re.compile(linkPathPrefix)))
            else:
                filtered.append(linkContent.find('a'))
        #print(soup)

    newList = []
    for link in filtered:
        try:
            newList.append(link.get('href'))
        except:
            continue

    newList = list(dict.fromkeys(newList))
    return newList
# It will return href value from the dom.
def getHrefText(link):
    if(link):
        link.get('href')
        return link

#convert data into CSV
def writeResultsToCSV(pageData,fileName):
    df = pd.DataFrame(pageData)
    df.to_csv(fileName ,mode='a', encoding='utf-8', index=False,header=False)

# Remove specfic html tag from the dom.
def removeDomElement(pageData,tagName):
    pageData.tagName.decompose()

