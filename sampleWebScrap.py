from bs4 import BeautifulSoup
import requests
import xlsxwriter
import re
import pandas as pd
import random
from collections import OrderedDict
import time
import webScrap as web
import json
from urllib.parse import unquote


baseUrl = "https://www.domain.com"
csvFileName = r"F:\domain.csv"

#number of pages
n = 12

for counter in pageNumber:
    webUrl = baseUrl
    webContent = web.getWebPageContent(webUrl)
    #Get alll the links from landing page.
    linkList = web.soupContentSelect(webContent,'h3[class*="results__title"]')
    #Parse the link. It will return all the links in the page.
    companyLinks = web.getAllHrefLinks(linkList,"a", False)
    pageData = []
    #Loop the each links 
    for contactPage in companyLinks:
        #Get all the contents from next page.ie landing page.
        companyDetailsPage = web.getWebPageContent(contactPage)
        # temp list to stor the address data.
        contactInfoDetails = []
        #Company Heading
        try:
            companyHeading = web.soupContentSelect(companyDetailsPage,'h2 > span')
            companyHeading = web.formatAddressContent(companyHeading[0].text)
        except:
            companyHeading = "N/A"
        contactInfoDetails.append(companyHeading)
        #Address Details
        try:
            Address = web.soupContentSelect(companyDetailsPage,'div[class*="location"]')
            Address = web.formatAddressContent(Address[0].text)
        except:
            Address = "N/A"
        contactInfoDetails.append(Address)    
        #Phone number
        try:
            phone = web.soupContentSelect(companyDetailsPage,'meta[name*="Telephone"]')
            phone = web.formatAddressContent(phone[0].get("content"))
        except:
            phone = "N/A"
        contactInfoDetails.append(phone)
        #Fax
        try:
            fax = web.soupContentSelect(companyDetailsPage,'meta[name*="Fax"]')
            fax = web.formatAddressContent(fax[0].get("content"))
        except:
            fax = "N/A"
        contactInfoDetails.append(fax)
        #Email address
        try:
            email = web.soupContentSelect(companyDetailsPage,'meta[name*="Email Address"]')
            email = web.formatAddressContent(email[0].get("content"))
        except:
            email = "N/A"
        contactInfoDetails.append(email)
        #web site url
        try:
            website = web.soupContentSelect(companyDetailsPage,'meta[name*="Website URL"]')
            website = web.formatAddressContent(website[0].get("content"))
        except:
            website = "N/A"        
        contactInfoDetails.append(website)
        print(contactInfoDetails)
        #Append list to main list. We are going to append this list in CSV file.
        pageData.append(contactInfoDetails)
    # Write the main list contents in CSV file. 
    web.writeResultsToCSV(pageData, csvFileName)