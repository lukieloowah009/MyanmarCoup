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

    #Using Regex to find number of arrests
    r2 = str(re.findall(r"([1-9]|[1-9][0-9]|[1-9][0-9][0-9]|[1-9][0-9][0-9][0-9])\sarbitrarily detained", soupText))

    #Formatting
    r2 = formatText(r2)

    #Uing Regex to find last edited date
    r3 = re.search(r"This page was last edited on \d\d? (March|April) \d\d\d\d", soupText).group(0)
    r4 = re.search(r"\d\d? (March|April) \d\d\d\d", r3).group(0)

    #Create and return json object
    result = {
        'Arrests': int(r2),
        'lastUpdated': r4
    }

    return func.HttpResponse(
        json.dumps(result),
        mimetype="application/json",
    )


def formatText(input):
    input = input.replace('[', '')
    input = input.replace(']', '')
    input = input.replace('\'', '')
    input = input.replace('\'', '')

    return input