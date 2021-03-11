import logging
import requests
from bs4 import BeautifulSoup
import azure.functions as func
import re
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    #wikipedia URL and making a request
    URL = "https://en.wikipedia.org/wiki/2021_Myanmar_coup_d%27%C3%A9tat"
    page = requests.get(URL)

    #Web Scraping the wikipedia page
    soup = BeautifulSoup(page.content, 'html.parser')
    soupText = str(soup.text)

    #Using Regex to find number of deaths
    r1 = re.findall(r"[0-9][0-9]\speople\shave\sbeen\skilled", soupText)
    r2 = str(re.findall(r"[0-9][0-9]", r1[0]))

    #Formatting
    r2 = r2.replace('[', '')
    r2 = r2.replace(']', '')
    r2 = r2.replace('\'', '')
    r2 = r2.replace('\'', '')

    #Create and return json object
    result = {
        'Deaths': int(r2)
    }

    return func.HttpResponse(
        json.dumps(result),
        mimetype="application/json",
    )

