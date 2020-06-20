from lxml import html, etree
import lxml.html
import re
import requests
import boto3
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import json
session = HTMLSession()
s3 = boto3.client('s3')
import hashlib



class Scraper:
    def __init__(self, url):
        self.headers = None
        self.json = None
        self.mode = None
        if "glassdoor" in url:
            self.mode = "glassdoor"
        elif "indeed" in url:
            self.mode = "indeed"
        print(self.mode)
        if self.mode == "glassdoor":
            self.json = self.glassdoor(url)
            self.send_data(self.json)
            # data = self.receive_data(self.json)
            # print(data)
        elif self.mode == "indeed":
            print("here")
            self.json = self.indeed(url)
            self.send_data(self.json)

    def glassdoor(self, url):
        self.headers = {	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'accept-encoding': 'gzip, deflate, sdch, br',
                        'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
                        'referer': 'https://www.glassdoor.com/',
                        'upgrade-insecure-requests': '1',
                        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive'
        }

        page = session.get(url, headers=self.headers, stream=True)

        soup = BeautifulSoup(page.content, 'html.parser')
        # print(soup)
        # print(page.content)
        company_name =  (soup.find('div', attrs={'class', 'css-16nw49e e11nt52q1'}).text.strip()).split(".")[0]
        title = (soup.find('div', attrs={'class', 'css-17x2pwl e11nt52q5'}).text.strip()).split(".")[0]
        location = (soup.find('div', attrs={'class':'css-13et3b1 e11nt52q2'}).text.strip()).split(".")[0]
        job_description = (soup.find('div', attrs={'class':'desc css-58vpdc ecgq1xb3'}).text)
        empId = hashlib.md5(url.encode("utf-8")).hexdigest()
        file_name = empId + ".json"
        data = {"title" : title, "company_name" : company_name, "location" : location, "job_description": job_description, "empId": empId}
        with open(file_name, 'w') as outfile:
            json.dump(data, outfile)
        return file_name

    def indeed(self, url):
        self.headers = {'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
        page = session.get(url, headers=self.headers, stream=True)
        soup = BeautifulSoup(page.content, 'html.parser')
        company_name = (soup.find('div', attrs={'class', 'icl-u-lg-mr--sm icl-u-xs-mr--xs'})).find('a').text
        title =  (soup.find('div', attrs={'class', 'jobsearch-JobInfoHeader-title-container'})).find('h3', attrs={'class', "icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title"}).text
        job_description = (soup.find('div', attrs={'class', 'jobsearch-jobDescriptionText'})).text
        location = "None"
        empId = hashlib.md5(url.encode("utf-8")).hexdigest()
        file_name = empId + ".json"
        print(file_name)
        data = {"title" : title, "company_name" : company_name, "location" : location, "job_description": job_description, "empId": empId}
        print(data)
        with open(file_name, 'w') as outfile:
            json.dump(data, outfile)
        return file_name


    def send_data(self, key):
        # serializedData = json.dumps(data)
        # print(serializedData)
        print(key)
        s3.upload_file(Bucket='job01', Key=key, Filename=key)


    def receive_data(self, key):
        print(key)
        object = s3.get_object(Bucket='job01',Key=key)
        serializedObject = object['Body'].read()

        myData = json.loads(serializedObject)
        return myData
        

        # return {"title" : title, "company_name" : company_name, "location" : location, "job_description": job_description}









